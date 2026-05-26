# 医疗器械客诉单生成器

根据医生对医疗器械产品的投诉，生成符合 ISO 13485 / FDA 21 CFR 820 要求的客诉单 PDF。

## 快速开始

```bash
# 安装依赖
pip install fpdf2

# 交互式创建客诉单
python scripts/complaint_cli.py new
```

## 使用方法

### 方式一：交互式 CLI

按步骤填写各个模块的信息，最后自动生成 PDF。

```bash
python scripts/complaint_cli.py new
```

从已有 JSON 文件继续编辑：

```bash
python scripts/complaint_cli.py new --json existing_data.json
```

### 方式二：直接调用 PDF 生成

准备好 JSON 数据后直接生成：

```bash
python scripts/generate_pdf.py --input data.json --output output/complaint.pdf
```

### 方式三：AI Agent 驱动

支持 SKILL.md 标准的 AI Agent 可读取本项目的 `SKILL.md`，按定义的工作流引导用户填写并自动调用脚本生成 PDF。

## 项目结构

```
myskill/
├── SKILL.md                 # AI Agent Skill 定义
├── scripts/
│   ├── model.py             # 数据模型
│   ├── generate_pdf.py      # PDF 生成
│   └── complaint_cli.py     # 交互式 CLI
├── output/                  # 生成的 PDF 和 JSON
└── requirements.txt
```

## 客诉单内容

PDF 包含以下 8 个模块：

| 分区 | 内容 |
|------|------|
| A | 投诉基本信息（编号、日期、来源） |
| B | 投诉人信息（报告人、医院、科室） |
| C | 产品信息（名称、型号、批号） |
| D | 投诉内容（类别、描述、患者伤害） |
| E | 研发调查（调查人、发现、根本原因） |
| F | 纠正措施（紧急措施、CAPA） |
| G | 风险评估（S/O/D 评分、RPN） |
| H | 监管报告（是否报告监管机构） |

## 输出

- 格式：PDF (A4 纵向)
- 命名：`COMP-YYYYMMDD-NNN.pdf`
- 存放：`output/` 目录

## 依赖

- Python 3.10+
- fpdf2 >= 2.5.0

## 合规参考

- ISO 13485:2016
- FDA 21 CFR Part 820
- 医疗器械监督管理条例
