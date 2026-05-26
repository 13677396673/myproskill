#!/usr/bin/env python3
"""
医疗器械客诉单 PDF 生成器
Medical Device Complaint Form PDF Generator

用法:
  python scripts/generate_pdf.py --input data.json --output complaint.pdf
  python scripts/generate_pdf.py --input data.json --output complaint.pdf --lang en
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

# 风险矩阵颜色
RISK_GREEN = (200, 230, 200)
RISK_YELLOW = (255, 255, 200)
RISK_RED = (255, 180, 180)
RISK_DARK_RED = (220, 80, 80)

# 高风险警示色
WARN_BG = (255, 235, 235)
WARN_BORDER = (200, 50, 50)
WARN_TEXT = (180, 0, 0)


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

    def __init__(self, lang: str = "zh"):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(True, 20)
        self.lang = lang

        fp = _find_font()
        if fp:
            self.add_font("zh", "", fp)
            self.add_font("zh", "B", fp)
        else:
            self.add_font("zh", "", "", "")
            self.add_font("zh", "B", "", "")

    # ── 双语辅助 ──────────────────────────────────────

    def _t(self, zh: str, en: str) -> str:
        """根据当前语言返回文本。"""
        return zh if self.lang == "zh" else en

    def _maybe_bilingual(self, zh: str, en: str) -> str:
        """双语模式返回 'zh / en'，单语返回对应语言的文本。"""
        if self.lang == "zh":
            return zh
        elif self.lang == "en":
            return en
        return f"{zh} / {en}"

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
        title = self._t("医疗器械客诉单", "Medical Device Complaint Form")
        self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("zh", "", 9)
        self.set_text_color(*TEXT_GRAY)
        subtitle = self._t(
            "Medical Device Complaint Form",
            "医疗器械客诉单"
        )
        self.cell(0, 6, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_draw_color(*PRIMARY)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(5)

    def _page_header_bar(self):
        self.set_font("zh", "B", 8)
        self.set_text_color(*TEXT_GRAY)
        label = self._t("医疗器械客诉单 (续)", "Medical Device Complaint (cont.)")
        self.cell(0, 6, label, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("zh", "", 7)
        self.set_text_color(128, 128, 128)

        # 版本号（如果存在）
        if hasattr(self, '_form_version') and self._form_version:
            ver_text = f"v{self._form_version}"
            self.cell(0, 10, ver_text, align="L")

        self.cell(0, 10, f"{self._t('第', 'Page')} {self.page_no()} {self._t('页', '')}", align="C")

    # ── 高风险警示条 ──────────────────────────────────

    def _high_risk_banner(self, form: ComplaintForm):
        """如果投诉涉及患者伤害或严重性高，显示红色警示条。"""
        if not form.is_high_risk:
            return

        self.ln(2)
        self._check_space(14)

        self.set_fill_color(*WARN_BG)
        self.set_draw_color(*WARN_BORDER)
        self.set_text_color(*WARN_TEXT)
        y = self.get_y()
        usable = self.w - self.l_margin - self.r_margin

        # 外框
        self.rect(self.l_margin, y, usable, 12, style="DF")

        reasons = []
        if form.patient_harm == "是":
            reasons.append(self._t("涉及患者伤害", "Patient harm involved"))
        if form.severity is not None and form.severity >= 4:
            reasons.append(self._t(f"严重性评分 {form.severity}/5", f"Severity score {form.severity}/5"))

        self.set_font("zh", "B", 10)
        warn_label = self._t("[!] 高风险投诉", "[!] HIGH RISK")
        self.set_xy(self.l_margin + 3, y + 1)
        self.cell(usable - 6, 5, warn_label)

        self.set_font("zh", "", 8)
        reason_text = " | ".join(reasons)
        priority_text = self._t("请优先处理！", "PRIORITY REQUIRED!")
        self.set_xy(self.l_margin + 3, y + 6)
        self.cell(usable - 6, 5, f"{reason_text} — {priority_text}")

        self.set_xy(self.l_margin, y + 12)
        self.ln(3)

    # ── 内容渲染 ──────────────────────────────────────

    def section_title(self, letter: str, title_zh: str, title_en: str = ""):
        """带背景色的分区标题。"""
        self.ln(2)
        self._check_space(9)
        self.set_fill_color(*HEADER_BG)
        self.set_text_color(*PRIMARY)
        self.set_font("zh", "B", 11)
        title = title_zh if self.lang == "zh" else (title_en or title_zh)
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
            self.field_row(self._t("严重性 (S)", "Severity (S)"), str(s))
            self.field_row(self._t("发生概率 (O)", "Occurrence (O)"), str(o))
            self.field_row(self._t("可检测性 (D)", "Detection (D)"), str(d))
            self.set_font("zh", "B", 9)
            self.field_row(self._t("RPN (S x O x D)", "RPN (S x O x D)"), str(rpn))
        else:
            self.field_row(self._t("严重性 (S)", "Severity (S)"), str(s or ""))
            self.field_row(self._t("发生概率 (O)", "Occurrence (O)"), str(o or ""))
            self.field_row(self._t("可检测性 (D)", "Detection (D)"), str(d or ""))
            self.field_row(self._t("RPN (S x O x D)", "RPN (S x O x D)"), "")

    # ── 风险矩阵图 ────────────────────────────────────

    def draw_risk_matrix(self, s_val: Optional[int], o_val: Optional[int], d_val: Optional[int]):
        """绘制 5×5 风险矩阵热力图 (S vs O)。"""
        cell = 10
        gap = 1.5
        label_w = 42
        left = self.l_margin + label_w + 5
        top = self.get_y()

        self._check_space(8 + 5 * (cell + gap) + 20)

        # 标题
        self.set_font("zh", "B", 9)
        self.set_text_color(*TEXT_DARK)
        title = self._t("风险矩阵 (S x O):", "Risk Matrix (S x O):")
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        top = self.get_y()

        # 绘制热力图
        for ox in range(5):  # O (row, Y axis)
            for sx in range(5):  # S (col, X axis)
                risk = (sx + 1) * (ox + 1)
                x = left + sx * (cell + gap)
                y = top + (4 - ox) * (cell + gap)

                # 根据风险等级着色
                if risk <= 4:
                    self.set_fill_color(*RISK_GREEN)
                elif risk <= 9:
                    self.set_fill_color(*RISK_YELLOW)
                elif risk <= 16:
                    self.set_fill_color(*RISK_RED)
                else:
                    self.set_fill_color(*RISK_DARK_RED)

                self.set_draw_color(*BORDER)
                self.rect(x, y, cell, cell, style="DF")

                # 格子中的数值
                self.set_font("zh", "", 6)
                self.set_text_color(*TEXT_GRAY)
                self.set_xy(x, y + (cell - 4) / 2)
                self.cell(cell, 4, str(risk), align="C")

        # 标记当前 S,O 位置
        if s_val is not None and o_val is not None and 1 <= s_val <= 5 and 1 <= o_val <= 5:
            sx = s_val - 1
            ox = o_val - 1
            cx = left + sx * (cell + gap) + cell / 2
            cy = top + (4 - ox) * (cell + gap) + cell / 2
            self.set_draw_color(200, 0, 0)
            self.set_line_width(0.6)
            d = 3.5
            self.line(cx - d, cy - d, cx + d, cy + d)
            self.line(cx + d, cy - d, cx - d, cy + d)
            self.set_line_width(0.2)

        # X 轴标签（S）
        self.set_font("zh", "", 7)
        self.set_text_color(*TEXT_GRAY)
        for sx in range(5):
            x = left + sx * (cell + gap) + cell / 2
            self.set_xy(x - 4, top + 5 * (cell + gap) + 1)
            self.cell(8, 4, str(sx + 1), align="C")

        # Y 轴标签（O）
        for ox in range(5):
            y = top + (4 - ox) * (cell + gap) + cell / 2 - 2
            self.set_xy(left - 8, y)
            self.cell(6, 4, str(ox + 1), align="C")

        # 轴标题
        s_label = self._t("S (严重性)", "S (Severity)")
        o_label = self._t("O (概率)", "O (Probability)")
        self.set_xy(left + 2.5 * (cell + gap) - 12, top + 5 * (cell + gap) + 6)
        self.cell(24, 4, s_label, align="C")
        self.set_xy(left - 22, top + 2.5 * (cell + gap) - 2)
        self.cell(12, 4, o_label, align="C")

        self.set_xy(left, top + 5 * (cell + gap) + 12)

    # ── 电子签名区域 ──────────────────────────────────

    def signature_section(self, form: ComplaintForm):
        """绘制电子签名签批栏。"""
        self.ln(3)
        self._check_space(45)

        self.set_draw_color(*BORDER)
        self.set_text_color(*TEXT_DARK)

        # 表头
        usable = self.w - self.l_margin - self.r_margin
        col_w = [10, 32, 32, 32, 24]  # 序号, 角色, 姓名, 签名, 日期
        col_w[0] = 8
        remaining = usable - sum(col_w) - 4  # 4 = borders
        col_w[1] += remaining // 2
        col_w[2] += remaining // 2

        self.set_font("zh", "B", 9)
        self.set_fill_color(*HEADER_BG)

        headers = self._t(
            ["序号", "签批角色", "姓名", "签名", "日期"],
            ["#", "Role", "Name", "Signature", "Date"]
        )
        x_start = self.l_margin
        y = self.get_y()
        for i, (w, h) in enumerate(zip(col_w, headers)):
            self.rect(x_start, y, w, 7, style="DF")
            self.set_xy(x_start + 1, y + 1)
            self.cell(w - 2, 5, h, align="C")
            x_start += w + 1

        # 数据行
        signers = [
            ("1", self._t("调查人", "Investigator"),
             form.investigator, form.investigator_signature, form.investigator_sign_date),
            ("2", self._t("审核人", "Reviewer"),
             form.reviewer_name, form.reviewer_signature, form.reviewer_sign_date),
            ("3", self._t("批准人", "Approver"),
             form.approver_name, form.approver_signature, form.approver_sign_date),
        ]

        self.set_font("zh", "", 8)
        for row_idx, (seq, role, name, sig, dt) in enumerate(signers):
            y = self.get_y()
            x_start = self.l_margin
            row_h = 7

            self._check_space(row_h)
            if self.get_y() != y:
                y = self.get_y()

            for i, w in enumerate(col_w):
                self.rect(x_start, y, w, row_h)
                if i < len(col_w) - 1:
                    pass
                x_start += w + 1

            x_start = self.l_margin
            vals = [seq, role, name or "—", sig or "—", dt or "—"]
            for i, (w, v) in enumerate(zip(col_w, vals)):
                self.set_xy(x_start + 1, y + 1.5)
                align = "C" if i in (0, 4) else "L"
                self.cell(w - 2, 4, v, align=align)
                x_start += w + 1

            self.set_xy(self.l_margin, y + row_h)

        self.ln(3)

    # ── 辅助 ──────────────────────────────────────────

    def _check_space(self, needed: float):
        """空间不足时自动翻页。"""
        if self.get_y() + needed > self.h - self.b_margin:
            self.add_page()

    # ── 完整生成 ─────────────────────────────────────

    def generate(self, form: ComplaintForm):
        self._form_version = form.version
        self.add_page()

        # 高风险警示条（在标题下方）
        self._high_risk_banner(form)

        # 编号 / 日期行
        self.set_font("zh", "", 9)
        id_label = self._t("客诉编号", "Complaint ID")
        recv_label = self._t("接收日期", "Received Date")
        self.cell(0, 6, f"{id_label}: {form.complaint_id}    {recv_label}: {form.received_date}",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        # A ──────
        self.section_title("A", self._t("投诉基本信息", "Complaint Information"))
        self.field_row(self._t("客诉编号", "Complaint ID"), form.complaint_id)
        self.field_row(self._t("接收日期", "Received Date"), form.received_date)
        self.field_row(self._t("投诉来源", "Source"), form.source)

        # B ──────
        self.section_title("B", self._t("投诉人信息", "Reporter Information"))
        self.field_row(self._t("报告人", "Reporter"), form.reporter_name)
        self.field_row(self._t("医院/机构", "Hospital"), form.hospital)
        self.field_row(self._t("科室", "Department"), form.department)
        self.field_row(self._t("联系方式", "Contact"), form.contact)
        self.field_row(self._t("报告日期", "Report Date"), form.report_date)

        # C ──────
        self.section_title("C", self._t("产品信息", "Product Information"))
        self.field_row(self._t("产品名称", "Product Name"), form.product_name)
        self.field_row(self._t("型号规格", "Model"), form.model)
        self.field_row(self._t("批号/序列号", "Lot/Serial No."), form.lot_number)
        self.field_row(self._t("生产日期", "Mfg Date"), form.manufacture_date)
        self.field_row(self._t("有效期", "Expiry Date"), form.expiry_date)

        # D ──────
        self.section_title("D", self._t("投诉内容", "Complaint Details"))
        self.field_row(self._t("投诉类别", "Category"), form.category)
        self.field_row(self._t("投诉详细描述", "Description"), form.description)
        self.field_row(self._t("涉及患者伤害", "Patient Harm"), form.patient_harm)
        self.field_row(self._t("发生频率", "Frequency"), form.frequency)

        # E ──────
        self.section_title("E", self._t("研发调查", "Investigation"))
        self.field_row(self._t("调查日期", "Investigation Date"), form.investigation_date)
        self.field_row(self._t("调查人", "Investigator"), form.investigator)
        self.field_row(self._t("调查方法", "Method"), form.investigation_method)
        self.field_row(self._t("调查发现", "Findings"), form.investigation_findings)
        self.field_row(self._t("根本原因分析", "Root Cause"), form.root_cause)
        self.field_row(self._t("根本原因分类", "Root Cause Category"), form.root_cause_category)

        # F ──────
        self.section_title("F", self._t("纠正措施", "Corrective Actions"))
        self.field_row(self._t("紧急处理措施", "Immediate Action"), form.immediate_action)
        self.field_row(self._t("长期纠正预防措施", "CAPA Action"), form.capa_action)
        self.field_row(self._t("责任人", "Responsible"), form.responsible_person)
        self.field_row(self._t("计划完成日期", "Target Date"), form.completion_date)

        # G ──────
        self.section_title("G", self._t("风险评估", "Risk Assessment"))
        self.rpn_row(form.severity, form.occurrence, form.detection)

        # 风险矩阵图
        if form.severity is not None and form.occurrence is not None:
            self.draw_risk_matrix(form.severity, form.occurrence, form.detection)

        # H ──────
        self.section_title("H", self._t("监管报告", "Regulatory Reporting"))
        self.field_row(self._t("需要报告监管机构", "Reportable"), form.regulatory_reportable)
        self.field_row(self._t("报告状态", "Status"), form.regulatory_status)

        # I ────── 电子签名
        self.section_title("I", self._t("电子签名", "Electronic Signatures"))
        self.signature_section(form)

        # 变更记录（如有）
        if form.change_log:
            self.ln(2)
            self.set_font("zh", "", 7)
            self.set_text_color(*TEXT_GRAY)
            log_title = self._t("变更记录:", "Revision History:")
            self.cell(0, 4, log_title, new_x="LMARGIN", new_y="NEXT")
            for entry in form.change_log:
                self.cell(0, 4, f"  - {entry}", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)


# ── CLI 入口 ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="生成医疗器械客诉单 PDF")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 PDF 文件路径")
    parser.add_argument("--lang", "-l", default="zh", choices=["zh", "en"], help="语言 (默认 zh)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    form = ComplaintForm.from_dict(data)
    pdf = ComplaintPDF(lang=args.lang)
    pdf.generate(form)
    pdf.output(args.output)
    print(f"PDF 已生成: {args.output}")


if __name__ == "__main__":
    main()
