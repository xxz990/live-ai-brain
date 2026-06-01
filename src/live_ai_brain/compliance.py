from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceRisk:
    category: str
    phrase: str
    reason: str
    safer_rewrite: str


@dataclass(frozen=True)
class ComplianceReport:
    risks: list[ComplianceRisk]

    @property
    def passed(self) -> bool:
        return not self.risks


RISKY_PHRASES = {
    "保证提分": "效果承诺风险",
    "一定有效": "效果承诺风险",
    "稳拿分": "效果承诺风险",
    "永久有效": "权益时效风险",
    "无理由退款": "售后口径风险",
}


def check_compliance(text: str) -> ComplianceReport:
    risks: list[ComplianceRisk] = []
    for phrase, category in RISKY_PHRASES.items():
        if phrase in text:
            risks.append(
                ComplianceRisk(
                    category=category,
                    phrase=phrase,
                    reason="该表达可能构成绝对化承诺或与当前官方口径不一致。",
                    safer_rewrite="建议改为：帮助孩子建立方法、提升理解能力，具体效果因孩子基础和学习投入而异。",
                )
            )
    return ComplianceReport(risks=risks)
