#!/usr/bin/env python3
"""
医疗器械客诉单 PDF 生成器
Medical Device Complaint Form PDF Generator

用法:
  python scripts/generate_pdf.py --input data.json --output complaint.pdf
"""

import argparse
import json
import os
import sys
from math import ceil
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fpdf import FPDF
from model import ComplaintForm

# ── 调色板 ─────────────────────────────────────────────
PRIMARY = (0, 82, 136)
HEADER_BG = (230, 242, 250)
BORDER = (180, 190, 200)
TEXT_DARK = (30, 30, 30)
TEXT_GRAY = (100, 100, 100)
LIGHT_ROW = (248, 249, 250)


def _find_font() -> str | None:
    """在 Windows 上查找可用的中文字体。"""
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\Deng.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


class ComplaintPDF(FPDF):
    """客诉单 PDF 渲染类。"""

    L_H = 7  # 行高 mm

    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(True, 20)

        fp = _find_font()
        if fp:
            self.add_font("zh", "", fp, uni=True)
            self.add_font("zh", "B", fp, uni=True)
        else:
            # 无中文字体时的降级 —— 仅支持英文 / 拼音
            self.add_font("zh", "", "", uni=True)
            self.add_font("zh", "B", "", uni=True)

    # ── 页面元素 ──────────────────────────────────────

    def header(self):
        if self.page_no() == 1:
            self._title_block()
        else:
            self._page_header_bar()

    def _title_block(self):
        self.set_font("zh", "B", 16)
        self.set_text_color(*PRIMARY)
        y0 = max(self.t_margin, 10)
        self.set_y(y0)
        self.cell(0, 10, "医疗器械客诉单", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("zh", "", 9)
        self.set_text_color(*TEXT_GRAY)
        self.cell(0, 6, "Medical Device Complaint Form", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_draw_color(*PRIMARY)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(5)

    def _page_header_bar(self):
        self.set_font("zh", "B", 8)
        self.set_text_color(*TEXT_GRAY)
        self.cell(0, 6, "医疗器械客诉单 (续)", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("zh", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"第 {self.page_no()} 页", align="C")

    # ── 内容渲染 ──────────────────────────────────────

    def section_title(self, letter: str, title: str):
        """带背景色的分区标题。"""
        self.ln(2)
        self._check_space(9)
        self.set_fill_color(*HEADER_BG)
        self.set_text_color(*PRIMARY)
        self.set_font("zh", "B", 11)
        self.cell(0, 8, f"  {letter}. {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT_DARK)
        self.ln(1)

    def field_row(self, label: str, value: object):
        """绘制一个字段行（自动处理换行）。"""
        value = str(value) if value is not None else ""
        label_w = 42
        usable = self.w - self.l_margin - self.r_margin
        val_w = usable - label_w
        self.set_font("zh", "", 9)

        sw = self.get_string_width(value)
        lines = max(1, ceil(sw / max(val_w - 2, 1)))
        row_h = max(self.L_H + 1, self.L_H * lines + 2)

        self._check_space(row_h)

        y = self.get_y()
        x = self.get_x()

        # 边框
        self.set_draw_color(*BORDER)
        self.rect(x, y, label_w, row_h)
        self.rect(x + label_w, y, val_w, row_h)

        # 标签
        self.set_font("zh", "B", 9)
        self.set_text_color(*TEXT_DARK)
        self.set_xy(x + 1, y + 1)
        self.multi_cell(label_w - 2, self.L_H, label)

        # 值
        self.set_font("zh", "", 9)
        self.set_xy(x + label_w + 1, y + 1)
        self.multi_cell(val_w - 2, self.L_H, value)

        self.set_xy(x, y + row_h)

    def rpn_row(self, s: Optional[int], o: Optional[int], d: Optional[int]):
        """风险评分专用行——显示三项评分 + 自动计算 RPN。"""
        if s is not None and o is not None and d is not None:
            rpn = s * o * d
            self.field_row("严重性 (S)", str(s))
            self.field_row("发生概率 (O)", str(o))
            self.field_row("可检测性 (D)", str(d))
            self.set_font("zh", "B", 9)
            self.field_row("RPN (S x O x D)", str(rpn))
        else:
            self.field_row("严重性 (S)", str(s or ""))
            self.field_row("发生概率 (O)", str(o or ""))
            self.field_row("可检测性 (D)", str(d or ""))
            self.field_row("RPN (S x O x D)", "")

    # ── 辅助 ──────────────────────────────────────────

    def _check_space(self, needed: float):
        """空间不足时自动翻页。"""
        if self.get_y() + needed > self.h - self.b_margin:
            self.add_page()

    # ── 完整生成 ─────────────────────────────────────

    def generate(self, form: ComplaintForm):
        self.add_page()

        # 编号 / 日期行
        self.set_font("zh", "", 9)
        self.cell(0, 6, f"客诉编号: {form.complaint_id}    接收日期: {form.received_date}",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        # A ──────
        self.section_title("A", "投诉基本信息")
        self.field_row("客诉编号", form.complaint_id)
        self.field_row("接收日期", form.received_date)
        self.field_row("投诉来源", form.source)

        # B ──────
        self.section_title("B", "投诉人信息")
        self.field_row("报告人", form.reporter_name)
        self.field_row("医院/机构", form.hospital)
        self.field_row("科室", form.department)
        self.field_row("联系方式", form.contact)
        self.field_row("报告日期", form.report_date)

        # C ──────
        self.section_title("C", "产品信息")
        self.field_row("产品名称", form.product_name)
        self.field_row("型号规格", form.model)
        self.field_row("批号/序列号", form.lot_number)
        self.field_row("生产日期", form.manufacture_date)
        self.field_row("有效期", form.expiry_date)

        # D ──────
        self.section_title("D", "投诉内容")
        self.field_row("投诉类别", form.category)
        self.field_row("投诉详细描述", form.description)
        self.field_row("涉及患者伤害", form.patient_harm)
        self.field_row("发生频率", form.frequency)

        # E ──────
        self.section_title("E", "研发调查")
        self.field_row("调查日期", form.investigation_date)
        self.field_row("调查人", form.investigator)
        self.field_row("调查方法", form.investigation_method)
        self.field_row("调查发现", form.investigation_findings)
        self.field_row("根本原因分析", form.root_cause)
        self.field_row("根本原因分类", form.root_cause_category)

        # F ──────
        self.section_title("F", "纠正措施")
        self.field_row("紧急处理措施", form.immediate_action)
        self.field_row("长期纠正预防措施", form.capa_action)
        self.field_row("责任人", form.responsible_person)
        self.field_row("计划完成日期", form.completion_date)

        # G ──────
        self.section_title("G", "风险评估")
        self.rpn_row(form.severity, form.occurrence, form.detection)

        # H ──────
        self.section_title("H", "监管报告")
        self.field_row("需要报告监管机构", form.regulatory_reportable)
        self.field_row("报告状态", form.regulatory_status)


# ── CLI 入口 ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="生成医疗器械客诉单 PDF")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 PDF 文件路径")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    form = ComplaintForm.from_dict(data)
    pdf = ComplaintPDF()
    pdf.generate(form)
    pdf.output(args.output)
    print(f"PDF 已生成: {args.output}")


if __name__ == "__main__":
    main()
