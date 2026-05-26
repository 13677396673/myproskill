---
name: medical-device-complaint
display_name: 医疗器械客诉单
description: 根据医生对医疗器械产品的投诉，生成符合 ISO 13485 / FDA 21 CFR 820 要求的客诉单 PDF
version: 1.0.0
author: ""
tags:
  - medical-device
  - complaint-handling
  - CAPA
  - quality-management
  - regulatory-compliance
  - pdf-generation

# ── 输入参数 ──────────────────────────────────────────
parameters:
  # A. 投诉基本信息
  - name: complaint_id
    display: 客诉编号
    type: string
    required: false
    description: 客诉编号，未指定则按 COMP-YYYYMMDD-NNN 自动生成

  - name: received_date
    display: 接收日期
    type: date
    required: false
    description: 投诉接收日期，默认为当天

  - name: source
    display: 投诉来源
    type: enum
    required: true
    enum: [电话, 邮件, 现场, 经销商, 其他]
    description: 投诉的接收渠道

  # B. 投诉人信息
  - name: reporter_name
    display: 报告人
    type: string
    required: false
    description: 投诉人（医生/医院联系人）姓名

  - name: hospital
    display: 医院/机构
    type: string
    required: false
    description: 投诉人所属医院或机构名称

  - name: department
    display: 科室
    type: string
    required: false
    description: 投诉人所在科室

  - name: contact
    display: 联系方式
    type: string
    required: false
    description: 电话或邮箱

  - name: report_date
    display: 报告日期
    type: date
    required: false
    description: 投诉人报告的日期，默认为当天

  # C. 产品信息
  - name: product_name
    display: 产品名称
    type: string
    required: true
    description: 被投诉的医疗器械产品名称

  - name: model
    display: 型号规格
    type: string
    required: true
    description: 产品型号规格

  - name: lot_number
    display: 批号/序列号
    type: string
    required: true
    description: 产品批号或序列号，用于追溯

  - name: manufacture_date
    display: 生产日期
    type: date
    required: false
    description: 产品生产日期

  - name: expiry_date
    display: 有效期
    type: date
    required: false
    description: 产品有效期

  # D. 投诉内容
  - name: category
    display: 投诉类别
    type: enum
    required: true
    enum: [产品质量, 包装问题, 标签问题, 性能问题, 外观问题, 其他]
    description: 投诉问题的类别

  - name: description
    display: 投诉详细描述
    type: text
    required: true
    description: 医生的详细投诉内容，包括问题现象、使用场景等

  - name: patient_harm
    display: 涉及患者伤害
    type: enum
    required: true
    enum: [是, 否, 未知]
    description: 投诉问题是否已对患者造成伤害

  - name: frequency
    display: 发生频率
    type: enum
    required: false
    enum: [单次, 偶发, 经常, 持续]
    description: 问题发生的频率

  # E. 研发调查
  - name: investigation_date
    display: 调查日期
    type: date
    required: false
    description: 调查日期，默认为当天

  - name: investigator
    display: 调查人
    type: string
    required: false
    description: 执行调查的工程师姓名

  - name: investigation_method
    display: 调查方法
    type: enum
    required: false
    enum: [现场调查, 实验室分析, 文件审查, 回访客户, 其他]
    description: 调查采用的方法

  - name: investigation_findings
    display: 调查发现
    type: text
    required: false
    description: 研发工程师调查后的具体发现

  - name: root_cause
    display: 根本原因分析
    type: text
    required: false
    description: 根本原因分析描述

  - name: root_cause_category
    display: 根本原因分类
    type: enum
    required: false
    enum: [设计问题, 制造问题, 原材料问题, 运输问题, 使用不当, 其他]
    description: 根本原因所属类别

  # F. 纠正措施
  - name: immediate_action
    display: 紧急处理措施
    type: text
    required: false
    description: 针对投诉采取的紧急处理措施

  - name: capa_action
    display: 长期纠正预防措施
    type: text
    required: false
    description: 长期纠正与预防措施计划

  - name: responsible_person
    display: 责任人
    type: string
    required: false
    description: 纠正措施执行责任人

  - name: completion_date
    display: 计划完成日期
    type: date
    required: false
    description: 纠正措施计划完成日期

  # G. 风险评估
  - name: severity
    display: 严重性 (S)
    type: integer
    required: false
    min: 1
    max: 5
    description: 风险严重性评分

  - name: occurrence
    display: 发生概率 (O)
    type: integer
    required: false
    min: 1
    max: 5
    description: 风险发生概率评分

  - name: detection
    display: 可检测性 (D)
    type: integer
    required: false
    min: 1
    max: 5
    description: 风险可检测性评分

  # H. 监管报告
  - name: regulatory_reportable
    display: 需要报告监管机构
    type: enum
    required: false
    enum: [是, 否]
    description: 该投诉是否需要向监管机构报告

  - name: regulatory_status
    display: 报告状态
    type: enum
    required: false
    enum: [未报告, 已报告, 不适用]
    description: 监管报告提交状态

  # I. 语言
  - name: language
    display: 语言/Language
    type: enum
    required: false
    enum: [zh, en]
    description: PDF 输出语言（zh=中文, en=英文）

# ── 脚本调用 ──────────────────────────────────────────
scripts:
  generate:
    command: python scripts/generate_pdf.py --input {input_path} --output {output_path} --lang {language}
    input_format: json
    output_format: pdf
    output_extension: .pdf
    description: 根据结构化 JSON 数据生成客诉单 PDF 文件

  interactive:
    command: python scripts/complaint_cli.py new
    description: 以交互式问答方式创建客诉单（不依赖 AI Agent 时使用）

  export:
    command: python scripts/export.py --input {input_path} --output {output_path} --format {format}
    description: 导出客诉单数据为 Excel (.xlsx) 或 CSV 格式
    formats: [xlsx, csv, all]

# ── AI Agent 工作流 ───────────────────────────────────
workflow:
  description: |
    AI Agent 应按照以下步骤引导用户完成客诉单的填写和 PDF 生成。
    核心原则：当用户输入模糊、笼统或信息不足时，必须主动追问细节，
    使用分级追问策略（先宽后窄），直到信息足以明确分类和记录。
    Agent 必须内化 probing_strategy 中的四级追问逻辑，并融入每个步骤的对话中。

  # ── 追问策略 ──────────────────────────────────
  probing_strategy:
    level_1_模糊检测:
      触发条件: 用户输入包含"不好用""有问题""坏了""异常""不对劲"等泛泛描述
      行为: 不直接提交或填入"其他"，立即触发追问
    level_2_分类引导:
      触发条件: 信息模糊但可归为大类
      行为: 用选择题而非开放题引导用户选择具体类别
      示例: "请问具体是以下哪种情况？① 性能问题（切割不顺畅）② 外观问题（有毛刺）③ 包装问题..."
    level_3_细节深挖:
      触发条件: 用户选择了具体类别
      行为: 按类别追问该类别的特有细节
      对照表:
        产品质量: 部件脱落、断裂、变形、涂层脱落、异物、其他
        性能问题: 精度不准、响应慢、噪音大、过热、漏水漏气、其他
        包装问题: 破损、密封不严、受潮、缺少配件、标识不符、其他
        标签问题: 字迹模糊、信息错误、信息遗漏、贴错位置、其他
        外观问题: 毛刺、划痕、变色、变形、异物、其他
    level_4_完整记录:
      触发条件: 细节已明确
      行为: 补全患者伤害、频率、批号/序列号等可追溯字段

  steps:
    - id: 0
      name: 选择语言
      fields: [language]
      prompt: |
        选择客诉单输出语言：
        - zh: 中文（默认）
        - en: English
      如果用户未指定，默认使用 zh。

    - id: 1
      name: 收集投诉基本信息
      fields: [complaint_id, received_date, source]
      prompt: |
        首先收集投诉基本信息：
        - 客诉编号（未指定则自动生成，调用 generate_next_id 避免冲突）
        - 接收日期（默认当天）
        - 投诉来源（电话/邮件/现场/经销商/其他）

    - id: 2
      name: 收集投诉人信息
      fields: [reporter_name, hospital, department, contact, report_date]
      prompt: |
        收集投诉人/报告人信息：
        - 报告人姓名、医院、科室、联系方式
        - 报告日期

    - id: 3
      name: 收集产品信息
      fields: [product_name, model, lot_number, manufacture_date, expiry_date]
      prompt: |
        收集被投诉的产品信息（产品名称、型号、批号为必填）：
        - 产品名称
        - 型号规格
        - 批号/序列号
        - 生产日期、有效期（可选）
      probing: |
        当产品名称模糊时追问完整注册证名称，而非俗称。
        如用户只说"导丝""刀片""导管"，追问完整产品名称和型号规格。

    - id: 4
      name: 收集投诉内容
      fields: [category, description, patient_harm, frequency]
      prompt: |
        收集详细的投诉内容。这是整个客诉单最核心的步骤，
        Agent 必须运用 probing_strategy 引导用户从模糊到具体。
      probing: |
        【模糊检测】
        用户描述泛泛（如"不好用""有问题""不行"）时，用选择题引导分类。

        示例话术：
        "请问您说的『不好用』具体属于以下哪种情况？
        ① 性能问题 — 切割不顺畅、精度不准、响应慢、噪音大
        ② 外观问题 — 有毛刺、划痕、变形、变色、异物
        ③ 包装问题 — 包装破损、密封不严、受潮、缺少配件
        ④ 标签问题 — 字迹模糊、信息错误、遗漏、贴错位置
        ⑤ 产品质量 — 部件脱落、断裂、变形、涂层脱落
        ⑥ 其他 — 以上都排除的其它情况"

        【类别深挖】根据用户选择的类别追问细节：
        - 产品质量 → 脱落？断裂？变形？涂层脱落？异物？
        - 性能问题 → 精度不准？响应慢？噪音大？过热？漏水漏气？
        - 包装问题 → 破损？密封不严？受潮？缺少配件？标识不符？
        - 标签问题 → 字迹模糊？信息错误？遗漏？贴错位置？
        - 外观问题 → 毛刺？划痕？变色？变形？异物？

        【患者伤害】如果 patient_harm 为"是"，必须追问：
        - 具体伤害表现（如划伤、感染、过敏反应等）
        - 是否已采取医疗处理措施
        - 当前患者状况

        【频率】用户说"好几次"等模糊描述时，明确追问：
        - 单次：仅发生一次 | 偶发：2-3次 | 经常：反复发生 | 持续：每次使用都存在

    - id: 5
      name: 收集研发调查结果
      fields: [investigation_date, investigator, investigation_method,
              investigation_findings, root_cause, root_cause_category]
      prompt: |
        收集研发工程师的调查结果：
        - 调查日期、调查人、调查方法
        - 调查发现
        - 根本原因分析及分类

    - id: 6
      name: 收集纠正措施
      fields: [immediate_action, capa_action, responsible_person, completion_date]
      prompt: |
        收集纠正措施信息：
        - 紧急处理措施
        - 长期纠正预防措施
        - 责任人和计划完成日期
      probing: |
        如果 patient_harm 为"是"，建议用户优先填写紧急处理措施。
        如果 root_cause_category 明确，建议针对根因制定对应的纠正措施。

    - id: 7
      name: 收集风险评估
      fields: [severity, occurrence, detection]
      prompt: |
        收集风险评分（1-5分）。提供评分参考标准：
        - S（严重性）：1=无影响 2=轻微 3=中等 4=严重 5=灾难
        - O（发生概率）：1=极低 2=低 3=中等 4=高 5=极高
        - D（可检测性）：1=可检出 2=较易检出 3=中等 4=不易检出 5=无法检出
        RPN = S x O x D 将由脚本自动计算。
      probing: |
        如果 patient_harm 为"是"，提醒严重性评分应 ≥ 3。
        评分后自动判断风险等级：RPN≤4 低、5-9 中、10-16 高、>16 紧急。
        如果 severity ≥ 4 或 patient_harm 为"是"，标记为高风险投诉。

    - id: 8
      name: 收集监管报告信息
      fields: [regulatory_reportable, regulatory_status]
      prompt: |
        确认是否需要向监管机构报告及当前报告状态。
      probing: |
        如果 patient_harm 为"是"，提醒此投诉可能涉及不良事件，
        需要评估是否按《医疗器械不良事件监测和再评价管理办法》报告。
        如需报告，提醒用户注意法规时限要求。

    - id: 9
      name: 收集电子签名
      fields: [investigator_signature, investigator_sign_date,
              reviewer_name, reviewer_signature, reviewer_sign_date,
              approver_name, approver_signature, approver_sign_date]
      prompt: |
        收集电子签名信息（可选，可直接跳过）：
        - 调查人签名及日期
        - 审核人姓名、签名及日期
        - 批准人姓名、签名及日期

    - id: 10
      name: 确认并生成
      action: generate_and_export
      prompt: |
        向用户展示所有字段的汇总预览。预览中应包含：
        - 8 个分区的所有字段内容
        - 自动计算的 RPN 值
        - 风险等级（低/中/高/紧急）
        - 高风险投诉标记（如有）

        确认前检查是否已有同编号的历史版本（扫描 output/ 目录）。
        如果存在历史版本，提示用户：
        "已存在 v{N}，是否基于此修改后生成 v{N+1}？"
        如果是修改后重新生成，询问变更说明并记录到 change_log。

        让用户选择操作：
        [c] 确认生成 PDF
        [e] 导出 Excel/CSV（询问格式：xlsx / csv / 全部）
        [r] 重新填写
        [q] 取消

        确认后，组装 JSON 并调用脚本生成 PDF：
        `python scripts/generate_pdf.py --input <json> --output <pdf> --lang <language>`
        如需额外导出：
        `python scripts/export.py --input <json> --output <path> --format <format>`

# ── 行为准则 ──────────────────────────────────────────
rules:
  - 客诉编号如未提供，使用 `ComplaintForm.generate_next_id()` 自动生成，避免同一天重复
  - 涉及患者伤害（patient_harm == "是"）的投诉，Agent 必须在每个后续步骤中高亮提示"此投诉涉及患者伤害，请优先处理！"
  - severity >= 4 的投诉，Agent 必须在后续步骤中提示"高风险投诉，请优先处理！"
  - 必填字段（required: true）必须确认用户已提供
  - 报告监管机构字段若为"是"，应提醒用户注意法规时限要求
  - 生成 PDF 时，RPN（S x O x D）由脚本自动计算，无需用户输入
  - 语言参数默认为 zh（中文）；如果用户偏好英文，设为 en
  - 多次修改重新生成时版本号自动递增，保留所有历史版本不覆盖
---

# 医疗器械客诉单

## 简介

根据医生对医疗器械产品的投诉，生成符合 **ISO 13485** / **FDA 21 CFR Part 820** 要求的客诉单 PDF。适用于研发工程师记录、调查和追踪产品质量投诉。

## 输出

- **文件格式**: PDF (A4 纵向)，可选 Excel (.xlsx) / CSV 导出
- **存放路径**: `output/` 目录
- **文件名格式**: `COMP-YYYYMMDD-NNN_v{version}.pdf`
- **页面布局**: 9 个分区（A-I），含风险矩阵热力图、高风险警示条、电子签名栏
- **语言支持**: 中文（zh）/ 英文（en）
- **版本控制**: 每次修改自动递增版本号，保留全部历史记录

## 使用方法

### 方式一：AI Agent 驱动

AI Agent 读取此 SKILL.md，按照 `workflow` 中的步骤引导用户逐项填写信息。Agent 会自动：
- 对模糊输入（如"不好用"）进行追问分类
- 识别高风险投诉并高亮提示
- 检查历史版本并自动递增版本号
- 调用脚本生成 PDF / Excel / CSV

```json
// 收集完毕后组装 JSON（示例）
{
  "complaint_id": "COMP-20260525-001",
  "received_date": "2026-05-25",
  "source": "电话",
  "product_name": "一次性使用手术刀片",
  "model": "BC-100",
  "lot_number": "20250501",
  "description": "医生反映刀片边缘有肉眼可见毛刺...",
  "category": "产品质量",
  "language": "zh"
}

// 调用脚本生成 PDF（zh/en 可选）
python scripts/generate_pdf.py --input data.json --output output/COMP-20260525-001.pdf --lang zh

// 导出 Excel / CSV
python scripts/export.py --input data.json --output output/COMP-20260525-001 --format xlsx
python scripts/export.py --input data.json --output output/COMP-20260525-001 --format csv
```

### 方式二：独立 CLI 交互

```bash
# 交互式创建（自动生成不冲突的编号）
python scripts/complaint_cli.py new

# 从已有 JSON 修改后生成（版本号自动递增）
python scripts/complaint_cli.py new --json output/COMP-20260525-001_v1.json
```

## 文件结构

```
myskill/
├── SKILL.md                       # Skill 定义文件（本文件）
├── scripts/
│   ├── model.py                   # 数据模型
│   ├── generate_pdf.py            # PDF 生成脚本（含风险矩阵、双语）
│   ├── export.py                  # Excel/CSV 导出脚本
│   └── complaint_cli.py           # 交互式 CLI
├── output/                        # 输出目录（含所有历史版本）
└── requirements.txt               # Python 依赖
```

## 关键特性

### 智能追问
当用户输入"刀片不好用"等模糊描述时，Agent 自动用选择题引导分类，然后针对所选类别深挖细节，确保投诉记录完整可追溯。

### 高风险预警
投诉涉及患者伤害（patient_harm == "是"）或严重性评分 ≥ 4 时，Agent 会在每个步骤高亮提示，PDF 顶部显示红色警示条。

### 风险矩阵图
PDF 中自动生成 5×5 风险矩阵热力图，S × O 交叉点以不同颜色标识风险等级（绿/黄/红），并标记当前投诉位置。

### 电子签名
符合 ISO 13485 文档签批要求，支持调查人、审核人、批准人三级签名。

### 版本控制
每次修改重新生成时版本号自动 +1，变更说明记录在 change_log 中，所有历史文件均保留不被覆盖。

## 依赖

- Python 3.10+
- fpdf2 >= 2.5.0
- openpyxl（可选，Excel 导出需要）
- Windows 系统自带中文字体（微软雅黑）

## 合规参考

- ISO 13485:2016 医疗器械质量管理体系
- FDA 21 CFR Part 820 质量体系法规
- FDA 21 CFR Part 11 电子记录/电子签名
- 《医疗器械监督管理条例》（国务院令第739号）
- 《医疗器械不良事件监测和再评价管理办法》（国家药监局令第1号）
