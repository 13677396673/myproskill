"""
医疗器械客诉单 - 数据模型
Medical Device Complaint Form - Data Model
"""

from dataclasses import dataclass, asdict
from datetime import date
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

    def __post_init__(self):
        """自动填充默认值。"""
        today_iso = date.today().isoformat()

        if not self.received_date:
            self.received_date = today_iso
        if not self.report_date:
            self.report_date = today_iso
        if not self.investigation_date:
            self.investigation_date = today_iso

        if not self.complaint_id:
            self.complaint_id = f"COMP-{date.today().strftime('%Y%m%d')}-001"

    # ── 派生属性 ──

    @property
    def rpn(self) -> Optional[int]:
        """风险优先数 = S × O × D"""
        if self.severity is not None and self.occurrence is not None and self.detection is not None:
            return self.severity * self.occurrence * self.detection
        return None

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
                # Handle None for Optional fields
                if raw is None or (isinstance(raw, str) and raw.strip() == ""):
                    if hasattr(field_def, "default") and field_def.default is not None:
                        cleaned[k] = field_def.default
                    else:
                        cleaned[k] = "" if field_def.type == "str" else None
                else:
                    cleaned[k] = raw
            else:
                cleaned[k] = field_def.default
        return cls(**cleaned)

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
        ]

    @classmethod
    def get_sections(cls) -> list[dict]:
        """获取分区定义。"""
        return [
            {"letter": "A", "title": "投诉基本信息"},
            {"letter": "B", "title": "投诉人信息"},
            {"letter": "C", "title": "产品信息"},
            {"letter": "D", "title": "投诉内容"},
            {"letter": "E", "title": "研发调查"},
            {"letter": "F", "title": "纠正措施"},
            {"letter": "G", "title": "风险评估"},
            {"letter": "H", "title": "监管报告"},
        ]
