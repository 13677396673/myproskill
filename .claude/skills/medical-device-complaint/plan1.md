# 改进方案：医疗器械客诉单 Skill 增强计划

---

## 1. 上下文感知与追问逻辑

### 目标

当用户输入模糊信息（如"刀片不好用"），AI Agent 能主动追问，引导用户从模糊描述逐步明确到具体类别和细节，而非直接填入"其他"或跳过关键信息。

### 改动范围

仅修改 `SKILL.md`，不涉及 Python 脚本。

### 设计方案

在 workflow 中新增 `probing_strategy` 四级追问策略，Agent 必须内化此逻辑：

| 级别 | 触发条件 | 行为 |
|------|----------|------|
| L1 模糊检测 | 用户输入"不好用""有问题""坏了""异常"等泛泛描述 | 触发追问，不直接提交 |
| L2 分类引导 | 信息模糊但可归大类 | 用选择题而非开放题引导用户选择具体类别 |
| L3 细节深挖 | 用户选择了具体类别 | 按类别追问该类别特有的细节 |
| L4 完整记录 | 细节已明确 | 补全患者伤害、频率、批号等可追溯字段 |

为关键 workflow step 追加 `probing` 字段：
- **Step 4（投诉内容）**：完整的追问话术 + 类别追问对照表（6 类别 × 子选项）
- **Step 7（风险评估）**：评分参考标准
- **Step 3/6/8**：各自场景下的追问指引

### 预期效果

用户说"刀片不好用" → Agent 用选择题引导分类 → 追问位置和细节 → 确认患者伤害 → 完整记录。

---

## 2. 自动识别高风险投诉

### 目标

当 `patient_harm == "是"` 或 `severity >= 4` 时，AI 自动高亮提示，引导用户优先处理，并在 PDF 中醒目标注。

### 改动范围

`SKILL.md` + `generate_pdf.py`（可选）

### 设计方案

**SKILL.md workflow 规则增强：**
- 在 Step 4（收集投诉内容）和 Step 7（风险评估）中追加条件判断逻辑
- 当 `patient_harm == "是"` 时，Agent 自动输出高亮警告："⚠️ **此投诉涉及患者伤害，请优先处理！**"
- 当 `severity >= 4` 时，同样触发高风险提示
- 提示内容应包括：建议加急调查、提醒法规报告时限、建议填写紧急处理措施

**PDF 可选增强：**
- 高风险投诉在 PDF 顶部或页眉处自动添加红色警示条
- 在封面或显著位置显示"高风险"标记

---

## 3. 自动生成 RPN 与风险矩阵图

### 目标

RPN 已在 `model.py` 中自动计算，但在 PDF 中以纯文本展示。改进为在 PDF 中生成可视化的风险矩阵图（热力图），直观展示 S/O/D 评分位置。

### 改动范围

`generate_pdf.py`

### 设计方案

在 PDF 的 G 区（风险评估）中增加一个 **5×5 风险矩阵热力图**：
- X 轴：严重性 S（1-5）
- Y 轴：发生概率 O（1-5）
- 每个格子根据 RPN 值填充颜色（绿 → 黄 → 红）
- 在矩阵上标记当前投诉的坐标点
- 同时保留现有的文字 RPN 展示

实现方式：使用 fpdf2 的 `set_fill_color` + `rect` 绘制彩色格子网格。

---

## 4. 添加电子签名区域

### 目标

在 PDF 中添加正式的电子签名栏，包含调查人、审核人、批准人的签名和日期，满足 ISO 13485 对文档签批的要求。

### 改动范围

`model.py` + `generate_pdf.py` + `SKILL.md` + `complaint_cli.py`

### 设计方案

**数据模型新增字段（model.py）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `investigator_signature` | str | 调查人签名（姓名） |
| `investigator_sign_date` | str | 调查人签名日期 |
| `reviewer_name` | str | 审核人姓名 |
| `reviewer_signature` | str | 审核人签名 |
| `reviewer_sign_date` | str | 审核人签名日期 |
| `approver_name` | str | 批准人姓名 |
| `approver_signature` | str | 批准人签名 |
| `approver_sign_date` | str | 批准人签名日期 |

**PDF 增强：**
- 在 PDF 末尾新增"签批栏"分区（I 区）
- 表格形式：角色 | 姓名 | 签名 | 日期
- 签名以印刷体姓名 + 日期代替手写（如需手写签名图片需额外处理）

**SKILL.md：**
- 新增 Step 10（收集签名信息）
- 更新 workflow 步骤

**CLI：**
- 新增 `input_section_i()` 签名输入

---

## 5. 多语言支持（中英双语）

### 目标

PDF 和 CLI 支持中英双语切换，满足外资医疗器械公司或出口产品的合规需求。

### 改动范围

`model.py` + `generate_pdf.py` + `SKILL.md` + `complaint_cli.py`

### 设计方案

**方案 A：参数控制（推荐）**
- 在 SKILL.md 新增 `language` 参数（`zh` / `en`）
- `model.py` 新增 `language` 字段
- `generate_pdf.py` 根据 `language` 切换标题、标签文本
- `complaint_cli.py` 根据 `language` 切换交互提示语

**方案 B：中英双语同页**
- PDF 中每个字段同时展示中英文（如"产品名称 / Product Name"）
- 无需新增参数，但 PDF 排版更紧凑

**SKILL.md 增强：**
- workflow 新增 Step 0（选择语言）
- 所有 Agent 提示语标记语言切换点

---

## 6. 导出多种格式

### 目标

除 PDF 外，支持导出为 Excel（.xlsx）和 CSV 格式，便于质量部门做数据分析与汇总。

### 改动范围

新增 `scripts/export.py` + `SKILL.md`

### 设计方案

**新增脚本 `scripts/export.py`：**
```
python scripts/export.py --input data.json --output report --format xlsx
python scripts/export.py --input data.json --output report --format csv
```

**Excel 输出格式：**
- Sheet 1: 客诉单详情（与 PDF 相同的 8 个分区，宽表布局）
- Sheet 2: 风险矩阵（S/O/D/RPN 数值）
- 带条件格式（高风险行红色高亮）

**CSV 输出格式：**
- 所有字段平铺为一行，UTF-8 BOM 编码确保 Excel 正确打开中文
- 适合批量导入数据分析工具

**SKILL.md：**
- 新增 `scripts` 条目指向 `export.py`
- workflow Step 9 支持选择导出格式（PDF / Excel / CSV / 全部）

**依赖：**
- 新增 `openpyxl`（Excel 导出）/ 或使用 `csv` 标准库（CSV 无需额外依赖）

---

## 7. 版本控制与历史保留

### 目标

当用户多次修改同一客诉单内容并重新生成时，保留所有历史版本，避免覆盖丢失，满足 FDA 21 CFR Part 11 对电子记录的要求。

### 改动范围

`model.py` + `generate_pdf.py` + `SKILL.md`

### 设计方案

**编号策略升级（model.py）：**
- 当前 `__post_init__` 固定生成 `COMP-YYYYMMDD-001`，同一天第二次会覆盖
- 改为扫描 `output/` 目录，自增序号
- 新增 `version` 字段（int），每次重新生成自动 +1

**文件命名规则：**
- 首次生成：`COMP-YYYYMMDD-001_v1.pdf` + `COMP-YYYYMMDD-001_v1.json`
- 修改后重生成：`COMP-YYYYMMDD-001_v2.pdf` + `COMP-YYYYMMDD-001_v2.json`
- 保留所有历史版本，不覆盖

**变更记录：**
- 在 PDF 末尾或页脚增加版本号 + 生成日期
- `model.py` 新增 `change_log` 字段（list[str]），记录每次修改说明

**SKILL.md workflow：**
- 在 Step 9 确认前，检查是否已存在同编号的历史版本
- 如果存在，提示用户"已生成过 v1，是否基于 v1 修改后生成 v2？"
- Agent 自动对比变更内容并写入 change_log

---

## 改动汇总

| # | 改进项 | 涉及文件 | 复杂度 |
|---|--------|----------|--------|
| 1 | 上下文感知与追问逻辑 | SKILL.md | 低 |
| 2 | 高风险投诉自动识别 | SKILL.md, generate_pdf.py | 低 |
| 3 | RPN 风险矩阵图 | generate_pdf.py | 中 |
| 4 | 电子签名区域 | model.py, generate_pdf.py, SKILL.md, complaint_cli.py | 中 |
| 5 | 多语言支持 | model.py, generate_pdf.py, SKILL.md, complaint_cli.py | 中-高 |
| 6 | 多格式导出（Excel/CSV） | scripts/export.py, SKILL.md | 中 |
| 7 | 版本控制与历史保留 | model.py, generate_pdf.py, SKILL.md | 中 |
