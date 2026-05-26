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

# ── 脚本调用 ──────────────────────────────────────────
scripts:
  generate:
    command: python scripts/generate_pdf.py --input {input_path} --output {output_path}
    input_format: json
    output_format: pdf
    output_extension: .pdf
    description: 根据结构化 JSON 数据生成客诉单 PDF 文件

  interactive:
    command: python scripts/complaint_cli.py new
    description: 以交互式问答方式创建客诉单（不依赖 AI Agent 时使用）

# ── AI Agent 工作流 ───────────────────────────────────
workflow:
  description: AI Agent 应按照以下步骤引导用户完成客诉单的填写和 PDF 生成

  steps:
    - id: 1
      name: 收集投诉基本信息
      fields: [complaint_id, received_date, source]
      prompt: |
        首先收集投诉基本信息：
        - 客诉编号（如无则自动生成）
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

    - id: 4
      name: 收集投诉内容
      fields: [category, description, patient_harm, frequency]
      prompt: |
        收集详细的投诉内容：
        - 投诉类别
        - 医生投诉的详细描述
        - 是否涉及患者伤害
        - 发生频率

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

    - id: 7
      name: 收集风险评估
      fields: [severity, occurrence, detection]
      prompt: |
        收集风险评分（1-5分）：
        - 严重性 S
        - 发生概率 O
        - 可检测性 D
        - RPN 值将自动计算

    - id: 8
      name: 收集监管报告信息
      fields: [regulatory_reportable, regulatory_status]
      prompt: |
        确认是否需要向监管机构报告及当前报告状态。

    - id: 9
      name: 确认并生成 PDF
      action: generate_pdf
      prompt: |
        向用户展示所有字段的汇总，请用户确认无误。
        确认后，将所有字段组装为 JSON 文件，
        调用 `python scripts/generate_pdf.py --input <json> --output <pdf>` 生成 PDF。

# ── 行为准则 ──────────────────────────────────────────
rules:
  - 客诉编号如未提供，使用 COMP-YYYYMMDD-NNN 格式自动生成
  - 涉及患者伤害的投诉应在流程中重点提示，建议优先处理
  - 必填字段（required: true）必须确认用户已提供
  - 报告监管机构字段若为"是"，应提醒用户注意法规时限要求
  - 生成 PDF 时，RPN（S x O x D）由脚本自动计算，无需用户输入
---

# 医疗器械客诉单

## 简介

根据医生对医疗器械产品的投诉，生成符合 **ISO 13485** / **FDA 21 CFR Part 820** 要求的客诉单 PDF。适用于研发工程师记录、调查和追踪产品质量投诉。

## 输出

- **文件格式**: PDF (A4 纵向)
- **存放路径**: `output/` 目录
- **文件名格式**: `COMP-YYYYMMDD-NNN.pdf`
- **页面布局**: 8 个分区（A-H），表格布局，自动分页

## 使用方法

### 方式一：AI Agent 驱动

AI Agent 读取此 SKILL.md，按照 `workflow` 中的步骤引导用户逐项填写信息，收集完毕后调用生成脚本输出 PDF。

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
  "category": "产品质量"
}

// 调用脚本
python scripts/generate_pdf.py --input data.json --output output/COMP-20260525-001.pdf
```

### 方式二：独立 CLI 交互

```bash
# 交互式创建
python scripts/complaint_cli.py new

# 从已有 JSON 修改后生成
python scripts/complaint_cli.py new --json data.json
```

## 文件结构

```
myskill/
├── SKILL.md                       # Skill 定义文件（本文件）
├── scripts/
│   ├── model.py                   # 数据模型
│   ├── generate_pdf.py            # PDF 生成脚本
│   └── complaint_cli.py           # 交互式 CLI
├── output/                        # 输出目录
└── requirements.txt               # Python 依赖
```

## 依赖

- Python 3.10+
- fpdf2 >= 2.5.0
- Windows 系统自带中文字体（微软雅黑）

## 合规参考

- ISO 13485:2016 医疗器械质量管理体系
- FDA 21 CFR Part 820 质量体系法规
- 《医疗器械监督管理条例》（国务院令第739号）
- 《医疗器械不良事件监测和再评价管理办法》（国家药监局令第1号）
