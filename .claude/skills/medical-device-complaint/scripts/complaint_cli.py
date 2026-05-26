#!/usr/bin/env python3
"""
医疗器械客诉单 - 交互式 CLI
Medical Device Complaint Form - Interactive CLI

用法:
  python scripts/complaint_cli.py new              # 交互式创建
  python scripts/complaint_cli.py new --json data.json  # 从 JSON 导入并编辑
"""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import ComplaintForm, COMPLAINT_SOURCES, COMPLAINT_CATEGORIES
from model import ROOT_CAUSE_CATEGORIES, REGULATORY_STATUSES, FREQUENCIES
from model import INVESTIGATION_METHODS, YES_NO_UNKNOWN, YES_NO

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
SCRIPT_DIR = Path(__file__).resolve().parent


# ── 交互辅助 ───────────────────────────────────────────

def prompt_str(label: str, default: str = "", required: bool = False) -> str:
    """输入字符串。"""
    prompt = f"  {label}"
    if default:
        prompt += f" [{default}]"
    if required:
        prompt += " *"
    prompt += ": "

    while True:
        val = input(prompt).strip()
        if not val and default:
            return default
        if not val and required:
            print("  ⚠ 此字段必填")
            continue
        return val


def prompt_enum(label: str, options: list[str], default: str = "") -> str:
    """选择枚举值。"""
    print(f"\n  ── {label} ──")
    for i, opt in enumerate(options, 1):
        m = " (默认)" if opt == default else ""
        print(f"    {i}. {opt}{m}")

    while True:
        raw = input(f"  请选择 (1-{len(options)}): ").strip()
        if not raw and default:
            return default
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("  输入无效，请重新选择")


def prompt_int(label: str, mini: int = 1, maxi: int = 5, default: int | None = None) -> int | None:
    """输入整数（可空）。"""
    prompt = f"  {label} ({mini}-{maxi})"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "

    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        if not raw:
            return None
        try:
            v = int(raw)
            if mini <= v <= maxi:
                return v
        except ValueError:
            pass
        print(f"  请输入 {mini}-{maxi} 之间的整数")


def prompt_date(label: str, default: str = "") -> str:
    """输入日期 (YYYY-MM-DD)。"""
    prompt = f"  {label}"
    if default:
        prompt += f" [{default}]"
    prompt += " (YYYY-MM-DD): "

    while True:
        raw = input(prompt).strip()
        if not raw and default:
            return default
        if not raw:
            return ""
        try:
            parts = raw.split("-")
            date(int(parts[0]), int(parts[1]), int(parts[2]))
            return raw
        except (ValueError, IndexError):
            print("  日期格式无效，请使用 YYYY-MM-DD")


# ── 分区输入 ───────────────────────────────────────────

SECTION_LABELS = {
    "A": "投诉基本信息",
    "B": "投诉人信息",
    "C": "产品信息",
    "D": "投诉内容",
    "E": "研发调查",
    "F": "纠正措施",
    "G": "风险评估",
    "H": "监管报告",
}


def input_section_a(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  A. 投诉基本信息")
    print(f"{'='*50}")
    form.complaint_id = prompt_str("客诉编号", form.complaint_id)
    form.received_date = prompt_date("接收日期", form.received_date)
    form.source = prompt_enum("投诉来源", COMPLAINT_SOURCES, form.source)


def input_section_b(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  B. 投诉人信息")
    print(f"{'='*50}")
    form.reporter_name = prompt_str("报告人", form.reporter_name)
    form.hospital = prompt_str("医院/机构", form.hospital)
    form.department = prompt_str("科室", form.department)
    form.contact = prompt_str("联系方式", form.contact)
    form.report_date = prompt_date("报告日期", form.report_date)


def input_section_c(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  C. 产品信息")
    print(f"{'='*50}")
    form.product_name = prompt_str("产品名称", form.product_name, required=True)
    form.model = prompt_str("型号规格", form.model, required=True)
    form.lot_number = prompt_str("批号/序列号", form.lot_number, required=True)
    form.manufacture_date = prompt_date("生产日期", form.manufacture_date)
    form.expiry_date = prompt_date("有效期", form.expiry_date)


def input_section_d(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  D. 投诉内容")
    print(f"{'='*50}")
    form.category = prompt_enum("投诉类别", COMPLAINT_CATEGORIES, form.category)
    form.description = prompt_str("投诉详细描述", form.description, required=True)
    form.patient_harm = prompt_enum("涉及患者伤害", YES_NO_UNKNOWN, form.patient_harm)
    form.frequency = prompt_enum("发生频率", FREQUENCIES)


def input_section_e(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  E. 研发调查")
    print(f"{'='*50}")
    form.investigation_date = prompt_date("调查日期", form.investigation_date)
    form.investigator = prompt_str("调查人", form.investigator)
    form.investigation_method = prompt_enum("调查方法", INVESTIGATION_METHODS)
    form.investigation_findings = prompt_str("调查发现", form.investigation_findings)
    form.root_cause = prompt_str("根本原因分析", form.root_cause)
    form.root_cause_category = prompt_enum("根本原因分类", ROOT_CAUSE_CATEGORIES)


def input_section_f(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  F. 纠正措施")
    print(f"{'='*50}")
    form.immediate_action = prompt_str("紧急处理措施", form.immediate_action)
    form.capa_action = prompt_str("长期纠正预防措施", form.capa_action)
    form.responsible_person = prompt_str("责任人", form.responsible_person)
    form.completion_date = prompt_date("计划完成日期", form.completion_date)


def input_section_g(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  G. 风险评估")
    print(f"{'='*50}")
    form.severity = prompt_int("严重性 (S)", 1, 5, form.severity)
    form.occurrence = prompt_int("发生概率 (O)", 1, 5, form.occurrence)
    form.detection = prompt_int("可检测性 (D)", 1, 5, form.detection)


def input_section_h(form: ComplaintForm):
    print(f"\n{'='*50}")
    print(f"  H. 监管报告")
    print(f"{'='*50}")
    form.regulatory_reportable = prompt_enum("需要报告监管机构", YES_NO, form.regulatory_reportable)
    form.regulatory_status = prompt_enum("报告状态", REGULATORY_STATUSES, form.regulatory_status)


# ── 预览 ───────────────────────────────────────────────

def show_preview(form: ComplaintForm):
    """以文本表格展示当前所有字段。"""
    sections = [
        ("A. 投诉基本信息", [
            ("客诉编号", form.complaint_id),
            ("接收日期", form.received_date),
            ("投诉来源", form.source),
        ]),
        ("B. 投诉人信息", [
            ("报告人", form.reporter_name),
            ("医院/机构", form.hospital),
            ("科室", form.department),
            ("联系方式", form.contact),
            ("报告日期", form.report_date),
        ]),
        ("C. 产品信息", [
            ("产品名称", form.product_name),
            ("型号规格", form.model),
            ("批号/序列号", form.lot_number),
            ("生产日期", form.manufacture_date),
            ("有效期", form.expiry_date),
        ]),
        ("D. 投诉内容", [
            ("投诉类别", form.category),
            ("投诉详细描述", form.description[:80] + ("..." if len(form.description) > 80 else "")),
            ("涉及患者伤害", form.patient_harm),
            ("发生频率", form.frequency),
        ]),
        ("E. 研发调查", [
            ("调查日期", form.investigation_date),
            ("调查人", form.investigator),
            ("调查方法", form.investigation_method),
            ("调查发现", form.investigation_findings[:60] + ("..." if len(form.investigation_findings) > 60 else "")),
            ("根本原因分析", form.root_cause[:60] + ("..." if len(form.root_cause) > 60 else "")),
            ("根本原因分类", form.root_cause_category),
        ]),
        ("F. 纠正措施", [
            ("紧急处理措施", form.immediate_action[:60] + ("..." if len(form.immediate_action) > 60 else "")),
            ("长期纠正预防措施", form.capa_action[:60] + ("..." if len(form.capa_action) > 60 else "")),
            ("责任人", form.responsible_person),
            ("计划完成日期", form.completion_date),
        ]),
        ("G. 风险评估", [
            ("严重性 (S)", str(form.severity) if form.severity else ""),
            ("发生概率 (O)", str(form.occurrence) if form.occurrence else ""),
            ("可检测性 (D)", str(form.detection) if form.detection else ""),
            ("RPN", str(form.rpn) if form.rpn is not None else ""),
        ]),
        ("H. 监管报告", [
            ("需要报告监管机构", form.regulatory_reportable),
            ("报告状态", form.regulatory_status),
        ]),
    ]

    print(f"\n{'='*60}")
    print("  📋 客诉单预览")
    print(f"{'='*60}")

    for sec_title, fields in sections:
        print(f"\n  ┌─ {sec_title} {'─' * (50 - len(sec_title))}┐")
        for label, value in fields:
            v = value if value else "—"
            print(f"  │ {label:　<12}: {v}")

    if form.rpn is not None:
        print(f"\n  ⚠  RPN = {form.rpn}")


# ── JSON 写入 + PDF 生成 ──────────────────────────────

def save_json(form: ComplaintForm, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(form.to_dict(), f, ensure_ascii=False, indent=2)
    return path


def generate_pdf(json_path: Path) -> Path:
    """调用 generate_pdf.py 生成 PDF。"""
    pdf_path = json_path.with_suffix(".pdf")
    script = SCRIPT_DIR / "generate_pdf.py"

    result = subprocess.run(
        [sys.executable, str(script), "--input", str(json_path), "--output", str(pdf_path)],
        capture_output=True, text=True, cwd=SCRIPT_DIR.parent,
    )
    if result.returncode != 0:
        print("  ❌ PDF 生成失败:")
        print(result.stderr)
        sys.exit(1)
    print(f"  ✅ {result.stdout.strip()}")
    return pdf_path


# ── 主命令 ─────────────────────────────────────────────

def cmd_new(json_input: str | None = None):
    """交互式创建客诉单。"""
    form = ComplaintForm()
    if json_input:
        with open(json_input, "r", encoding="utf-8") as f:
            data = json.load(f)
        form = ComplaintForm.from_dict(data)
        print("已加载外部数据，可在此基础上修改。")

    print(f"\n{'='*50}")
    print("  医疗器械客诉单 — 交互式创建")
    print(f"  日期: {date.today()}")
    print(f"{'='*50}")

    while True:
        input_section_a(form)
        input_section_b(form)
        input_section_c(form)
        input_section_d(form)
        input_section_e(form)
        input_section_f(form)
        input_section_g(form)
        input_section_h(form)

        show_preview(form)

        print(f"\n  {'─'*50}")
        cmd = input("  [c]确认生成  [r]重新填写  [q]取消: ").strip().lower()
        if cmd == "c":
            break
        elif cmd == "q":
            print("已取消")
            return

    # 保存 JSON + 生成 PDF
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"{form.complaint_id}.json"
    save_json(form, json_path)
    print(f"\n  数据已保存: {json_path}")

    pdf_path = generate_pdf(json_path)
    print(f"  ✅ 客诉单已生成: {pdf_path}")


# ── 入口 ───────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="医疗器械客诉单 CLI")
    sub = parser.add_subparsers(dest="command")
    new_parser = sub.add_parser("new", help="创建新的客诉单")
    new_parser.add_argument("--json", "-j", help="从 JSON 文件导入", default=None)

    args = parser.parse_args()
    if args.command == "new":
        cmd_new(args.json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
