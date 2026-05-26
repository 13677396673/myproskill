"""
医疗器械客诉单 - 数据模型
Medical Device Complaint Form - Data Model
"""

import re
from dataclasses import dataclass, asdict, field, MISSING
from datetime import date
from pathlib import Path
from typing import Optional


# ── 枚举定义 ──────────────────────────────────────────

COMPLAINT_SOURCES = ["电话", "邮件", "现场", "经销商", "其他"]
COMPLAINT_CATEGORIES = ["产品质量", "包装问题", "标签问题", "性能问题", "外观问题", "其他"]
ROOT_CAUSE_CATEGORIES = ["设计问题", "制造问题", "原材料问题", "运输问题", "使用不当", "其他"]
REGULATORY_STATUSES = ["未报告", "已报告", "不适用"]
FREQUENCIES = ["单次", "偶发", "经常", "持续"]
INVESTIGATION_METHODS = ["现场调查", "实验室分析", "文件审查", "回访客户", "其他"]
YES_NO_UNKNOWN = ["是", "否", "未知"]
YES_NO = ["是", "否"]
LANGUAGES = ["zh", "en"]
RISK_LEVELS = ["低", "中", "高", "紧急"]

# 签批角色
SIGNATURE_ROLES = [
    {"key": "investigator", "label_zh": "调查人", "label_en": "Investigator"},
    {"key": "reviewer", "label_zh": "审核人", "label_en": "Reviewer"},
    {"key": "approver", "label_zh": "批准人", "label_en": "Approver"},
]


# ── 主数据模型 ────────────────────────────────────────

@dataclass
class ComplaintForm:
    """医疗器械客诉单完整数据模型。"""

    # ── A. 投诉基本信息 ──
    complaint_id: str = ""
    received_date: str = ""
    source: str = "其他"

    # ── B. 投诉人信息 ──
    reporter_name: str = ""
    hospital: str = ""
    department: str = ""
    contact: str = ""
    report_date: str = ""

    # ── C. 产品信息 ──
    product_name: str = ""
    model: str = ""
    lot_number: str = ""
    manufacture_date: str = ""
    expiry_date: str = ""

    # ── D. 投诉内容 ──
    category: str = "其他"
    description: str = ""
    patient_harm: str = "未知"
    frequency: str = ""

    # ── E. 研发调查 ──
    investigation_date: str = ""
    investigator: str = ""
    investigation_method: str = ""
    investigation_findings: str = ""
    root_cause: str = ""
    root_cause_category: str = ""

    # ── F. 纠正措施 ──
    immediate_action: str = ""
    capa_action: str = ""
    responsible_person: str = ""
    completion_date: str = ""

    # ── G. 风险评估 ──
    severity: Optional[int] = None
    occurrence: Optional[int] = None
    detection: Optional[int] = None

    # ── H. 监管报告 ──
    regulatory_reportable: str = "否"
    regulatory_status: str = "不适用"

    # ── I. 电子签名 ──
    investigator_signature: str = ""
    investigator_sign_date: str = ""
    reviewer_name: str = ""
    reviewer_signature: str = ""
    reviewer_sign_date: str = ""
    approver_name: str = ""
    approver_signature: str = ""
    approver_sign_date: str = ""

    # ── 语言 ──
    language: str = "zh"

    # ── 版本控制 ──
    version: int = 1
    change_log: list[str] = field(default_factory=list)

    def __post_init__(self):
        """自动填充默认值。"""
        today_iso = date.today().isoformat()
        today_ymd = date.today().strftime("%Y%m%d")

        if not self.received_date:
            self.received_date = today_iso
        if not self.report_date:
            self.report_date = today_iso
        if not self.investigation_date:
            self.investigation_date = today_iso

        if not self.complaint_id:
            self.complaint_id = f"COMP-{today_ymd}-001"

    # ── 风险评估派生 ──

    @property
    def rpn(self) -> Optional[int]:
        """风险优先数 = S × O × D"""
        if self.severity is not None and self.occurrence is not None and self.detection is not None:
            return self.severity * self.occurrence * self.detection
        return None

    @property
    def risk_level(self) -> str:
        """风险等级。"""
        s = self.severity or 1
        o = self.occurrence or 1
        risk = s * o
        if risk <= 4:
            return "低"
        elif risk <= 9:
            return "中"
        elif risk <= 16:
            return "高"
        return "紧急"

    @property
    def is_high_risk(self) -> bool:
        """是否为高风险投诉。"""
        if self.patient_harm == "是":
            return True
        if self.severity is not None and self.severity >= 4:
            return True
        if self.occurrence is not None and self.occurrence >= 4 and self.severity is not None and self.severity >= 3:
            return True
        return False

    # ── 编号生成 ──

    @classmethod
    def generate_next_id(cls, output_dir: str | Path = "output") -> str:
        """扫描 output 目录，生成下一个可用的客诉编号。"""
        output_path = Path(output_dir)
        today_ymd = date.today().strftime("%Y%m%d")
        prefix = f"COMP-{today_ymd}-"
        max_num = 0

        if output_path.exists():
            for f in output_path.iterdir():
                if f.suffix in (".json", ".pdf") and f.stem.startswith(prefix):
                    # 匹配 COMP-YYYYMMDD-NNN 或 COMP-YYYYMMDD-NNN_vN
                    match = re.match(rf"^{re.escape(prefix)}(\d+)(?:_v\d+)?$", f.stem)
                    if match:
                        num = int(match.group(1))
                        max_num = max(max_num, num)

        return f"{prefix}{max_num + 1:03d}"

    # ── 序列化 ──

    def to_dict(self) -> dict:
        """转为可 JSON 序列化的字典。"""
        d = {}
        for k, v in asdict(self).items():
            if v is None:
                d[k] = ""
            else:
                d[k] = v
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ComplaintForm":
        """从字典恢复对象。"""
        cleaned = {}
        field_types = cls.__dataclass_fields__
        for k, field_def in field_types.items():
            if k in data and data[k] is not None:
                raw = data[k]
                if raw is None or (isinstance(raw, str) and raw.strip() == ""):
                    cleaned[k] = cls._get_default(field_def)
                else:
                    cleaned[k] = raw
            else:
                cleaned[k] = cls._get_default(field_def)
        return cls(**cleaned)

    @staticmethod
    def _get_default(field_def) -> object:
        """获取字段的默认值（支持 default_factory）。"""
        if field_def.default is not MISSING:
            return field_def.default
        if field_def.default_factory is not MISSING:
            return field_def.default_factory()
        return ""

    @classmethod
    def get_field_meta(cls) -> list[dict]:
        """获取所有字段的元信息,供SKILL.md或CLI使用。"""
        return [
            # A
            {"key": "complaint_id",      "section": "A", "label": "客诉编号",      "type": "string", "required": False},
            {"key": "received_date",     "section": "A", "label": "接收日期",      "type": "date",   "required": False},
            {"key": "source",            "section": "A", "label": "投诉来源",      "type": "enum",   "required": True,  "options": COMPLAINT_SOURCES},
            # B
            {"key": "reporter_name",     "section": "B", "label": "报告人",        "type": "string", "required": False},
            {"key": "hospital",          "section": "B", "label": "医院/机构",     "type": "string", "required": False},
            {"key": "department",        "section": "B", "label": "科室",          "type": "string", "required": False},
            {"key": "contact",           "section": "B", "label": "联系方式",      "type": "string", "required": False},
            {"key": "report_date",       "section": "B", "label": "报告日期",      "type": "date",   "required": False},
            # C
            {"key": "product_name",      "section": "C", "label": "产品名称",      "type": "string", "required": True},
            {"key": "model",             "section": "C", "label": "型号规格",      "type": "string", "required": True},
            {"key": "lot_number",        "section": "C", "label": "批号/序列号",   "type": "string", "required": True},
            {"key": "manufacture_date",  "section": "C", "label": "生产日期",      "type": "date",   "required": False},
            {"key": "expiry_date",       "section": "C", "label": "有效期",        "type": "date",   "required": False},
            # D
            {"key": "category",          "section": "D", "label": "投诉类别",      "type": "enum",   "required": True,  "options": COMPLAINT_CATEGORIES},
            {"key": "description",       "section": "D", "label": "投诉详细描述",  "type": "text",   "required": True},
            {"key": "patient_harm",      "section": "D", "label": "涉及患者伤害",  "type": "enum",   "required": True,  "options": YES_NO_UNKNOWN},
            {"key": "frequency",         "section": "D", "label": "发生频率",      "type": "enum",   "required": False, "options": FREQUENCIES},
            # E
            {"key": "investigation_date","section": "E", "label": "调查日期",      "type": "date",   "required": False},
            {"key": "investigator",      "section": "E", "label": "调查人",        "type": "string", "required": False},
            {"key": "investigation_method","section":"E","label": "调查方法",      "type": "enum",   "required": False, "options": INVESTIGATION_METHODS},
            {"key": "investigation_findings","section":"E","label":"调查发现",     "type": "text",   "required": False},
            {"key": "root_cause",        "section": "E", "label": "根本原因分析",  "type": "text",   "required": False},
            {"key": "root_cause_category","section":"E","label": "根本原因分类",   "type": "enum",   "required": False, "options": ROOT_CAUSE_CATEGORIES},
            # F
            {"key": "immediate_action",  "section": "F", "label": "紧急处理措施",  "type": "text",   "required": False},
            {"key": "capa_action",       "section": "F", "label": "长期纠正预防措施","type":"text",  "required": False},
            {"key": "responsible_person","section": "F", "label": "责任人",        "type": "string", "required": False},
            {"key": "completion_date",   "section": "F", "label": "计划完成日期",  "type": "date",   "required": False},
            # G
            {"key": "severity",          "section": "G", "label": "严重性 (S)",    "type": "integer","required": False, "min": 1, "max": 5},
            {"key": "occurrence",        "section": "G", "label": "发生概率 (O)",  "type": "integer","required": False, "min": 1, "max": 5},
            {"key": "detection",         "section": "G", "label": "可检测性 (D)",  "type": "integer","required": False, "min": 1, "max": 5},
            # H
            {"key": "regulatory_reportable","section":"H","label":"需要报告监管机构","type":"enum", "required": False, "options": YES_NO},
            {"key": "regulatory_status",   "section":"H","label":"报告状态",       "type":"enum",   "required": False, "options": REGULATORY_STATUSES},
            # I
            {"key": "language",            "section": "I", "label": "语言",         "type": "enum",   "required": False, "options": LANGUAGES},
            {"key": "version",             "section": "I", "label": "版本号",       "type": "integer","required": False},
        ]

    @classmethod
    def get_sections(cls) -> list[dict]:
        """获取分区定义。"""
        return [
            {"letter": "A", "title_zh": "投诉基本信息", "title_en": "Complaint Information"},
            {"letter": "B", "title_zh": "投诉人信息",   "title_en": "Reporter Information"},
            {"letter": "C", "title_zh": "产品信息",     "title_en": "Product Information"},
            {"letter": "D", "title_zh": "投诉内容",     "title_en": "Complaint Details"},
            {"letter": "E", "title_zh": "研发调查",     "title_en": "Investigation"},
            {"letter": "F", "title_zh": "纠正措施",     "title_en": "Corrective Actions"},
            {"letter": "G", "title_zh": "风险评估",     "title_en": "Risk Assessment"},
            {"letter": "H", "title_zh": "监管报告",     "title_en": "Regulatory Reporting"},
            {"letter": "I", "title_zh": "电子签名",     "title_en": "Electronic Signatures"},
        ]
