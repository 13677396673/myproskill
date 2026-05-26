# 医疗器械客诉单 Skill — 设计方案

## 1. 概述

创建一个**标准化的 Skill**，以 `SKILL.md` 为核心定义文件 + `scripts/` 作为执行脚本。任何 AI agent（Claude、其他 LLM 平台等）只要读取 `SKILL.md`，就能理解这个客诉单工具的能力和调用方式。

**本质**：一份 AI agent 能读懂的说明书（SKILL.md）+ 背后跑得动的 Python 脚本。

---

## 2. 什么是 SKILL.md 标准化

`SKILL.md` 是一个结构化的 Markdown 文件，包含：

- **Frontmatter 元数据** — 名称、描述、版本、作者、标签
- **参数声明** — 技能所需的输入字段（名称、类型、是否必填、说明）
- **能力描述** — AI agent 读取后知道该技能能做什么、不能做什么
- **工作流定义** — AI agent 应遵循的对话/操作流程
- **输出声明** — 技能产出的文件格式和位置

任何兼容的 AI agent 都可以解析这份 `SKILL.md`，理解技能的能力边界和调用方式。

---

## 3. 两种使用模式

### 模式 A：AI Agent 驱动（主要模式）
AI agent 读取 `SKILL.md` → 按工作流引导工程师填写 → 拼 JSON → 调用 Python 脚本生成 PDF

```
工程师描述投诉 → Agent 理解 SKILL.md → 按流程引导收集信息 → 调用脚本 → 输出 PDF
```

### 模式 B：独立 CLI 执行（兜底模式）
工程师直接运行 Python 脚本，以交互式问答方式填写

```
python scripts/complaint_cli.py new
```

两种模式共享同一套数据模型和 PDF 渲染引擎。

---

## 4. 项目结构

```
myskill/
├── SKILL.md                      # ⭐ 标准 Skill 定义文件（核心入口）
├── scripts/
│   ├── generate_pdf.py           # PDF 生成脚本（被 agent 或 CLI 调用）
│   │   调用方式: python generate_pdf.py --input data.json --output out.pdf
│   ├── complaint_cli.py          # 独立交互式 CLI（可选，兜底用）
│   └── model.py                  # 数据模型 + 字段定义（被上述脚本共用）
├── output/                       # PDF 输出目录
├── requirements.txt
└── README.md                     # 人类使用说明
```

---

## 5. SKILL.md 结构设计

```markdown
---
name: medical-device-complaint
display_name: 医疗器械客诉单
description: 根据医生对医疗器械产品的投诉，生成格式规范的客诉单 PDF
version: 1.0.0
tags: [医疗器械, 客诉, CAPA, 质量, 监管合规]
parameters:
  - name: complaint_id
    display: 客诉编号
    type: string
    required: false
    description: 自动生成或手动指定
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
    description: 产品批号或序列号
  - name: complaint_description
    display: 投诉描述
    type: text
    required: true
    description: 医生的详细投诉内容
  - name: reporter_name
    display: 报告人
    type: string
    required: false
    description: 医生或医院联系人的姓名
  - name: hospital
    display: 医院/机构
    type: string
    required: false
    description: 投诉人所属医院或机构
  - name: department
    display: 科室
    type: string
    required: false
  - name: contact
    display: 联系方式
    type: string
    required: false
  - name: report_date
    display: 报告日期
    type: date
    required: false
    description: 默认为当天
  - name: category
    display: 投诉类别
    type: enum
    required: true
    enum: [产品质量, 包装问题, 标签问题, 性能问题, 外观问题, 其他]
    description: 投诉问题的类别
  - name: patient_harm
    display: 是否涉及患者伤害
    type: enum
    required: true
    enum: [是, 否, 未知]
  - name: frequency
    display: 发生频率
    type: enum
    required: false
    enum: [单次, 偶发, 经常, 持续]
  - name: investigation_findings
    display: 调查发现
    type: text
    required: false
    description: 研发工程师的调查结果
  - name: root_cause
    display: 根本原因分析
    type: text
    required: false
  - name: root_cause_category
    display: 根本原因分类
    type: enum
    required: false
    enum: [设计问题, 制造问题, 原材料问题, 运输问题, 使用不当, 其他]
  - name: immediate_action
    display: 紧急处理措施
    type: text
    required: false
  - name: capa_action
    display: 长期纠正预防措施
    type: text
    required: false
  - name: severity
    display: 严重性
    type: integer
    required: false
    min: 1
    max: 5
    description: 风险评分
  - name: occurrence
    display: 发生概率
    type: integer
    required: false
    min: 1
    max: 5
  - name: detection
    display: 可检测性
    type: integer
    required: false
    min: 1
    max: 5
  - name: regulatory_reportable
    display: 需要报告监管机构
    type: boolean
    required: false
  - name: regulatory_status
    display: 监管报告状态
    type: enum
    required: false
    enum: [未报告, 已报告, 不适用]
script:
  command: python scripts/generate_pdf.py
  input_format: json
  output_format: pdf
  output_path: output/
---

# 医疗器械客诉单

## 简介
根据医生对产品的投诉，生成符合 ISO 13485 / FDA 21 CFR 820 要求的医疗器械客诉单 PDF。适用于研发工程师记录、调查和追踪产品质量投诉。

## 工作流

### Step 1: 收集投诉基本信息
- 客诉编号（可选，未指定则自动生成）
- 接收日期（默认当天）
- 投诉来源（电话/邮件/现场/经销商/其他）

### Step 2: 收集投诉人信息
- 报告人姓名、医院、科室、联系方式
- 报告日期

### Step 3: 收集产品信息
- 产品名称、型号规格、批号/序列号
- 生产日期、有效期（可选）

### Step 4: 收集投诉内容
- 投诉类别、详细描述
- 是否涉及患者伤害
- 发生频率

### Step 5: 收集研发调查结果
- 调查日期、调查人、调查方法
- 调查发现
- 根本原因分析和分类

### Step 6: 收集纠正措施
- 紧急处理措施
- 长期 CAPA 计划
- 责任人和完成日期

### Step 7: 收集风险评估
- 严重性、发生概率、可检测性评分（1-5）
- RPN 自动计算

### Step 8: 收集监管报告信息
- 是否需要报告监管机构
- 报告状态

### Step 9: 确认并生成 PDF
- 展示所有信息给工程师确认
- 调用脚本生成 PDF

## 输出
- 文件格式: PDF (A4)
- 存放路径: output/ 目录
- 文件名: COMP-{YYYYMMDD}-{序号}.pdf

## 注意事项
- 客诉编号如未提供，按 COMP-YYYYMMDD-NNN 格式自动生成
- 涉及患者伤害的投诉需优先处理
- PDF 生成失败时检查日志获取详细错误信息
```
