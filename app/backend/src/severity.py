from dataclasses import dataclass

from .metrics import SEVERITY_EVALUATION_TOTAL, SEVERITY_HIGH_TOTAL

KEYWORD_WEIGHTS = {
    "breach": 40,
    "ransomware": 50,
    "data exfiltration": 45,
    "critical": 25,
    "privilege escalation": 35,
}

MODIFIER_WEIGHTS = {
    "production": 20,
    "customer_impact": 20,
    "isolated": -15,
    "known_issue": -10,
}


@dataclass
class SeverityResult:
    score: int
    level: str
    route: str


def evaluate_severity(summary: str, modifiers: list[str] | None = None) -> SeverityResult:
    lower = summary.lower()
    score = 10
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in lower:
            score += weight
    for modifier in modifiers or []:
        score += MODIFIER_WEIGHTS.get(modifier, 0)
    score = max(0, min(score, 100))

    if score >= 75:
        level, route = "high", "page-on-call-and-security-lead"
        SEVERITY_HIGH_TOTAL.inc()
    elif score >= 45:
        level, route = "medium", "create-priority-ticket"
    else:
        level, route = "low", "standard-queue"

    SEVERITY_EVALUATION_TOTAL.inc()
    return SeverityResult(score=score, level=level, route=route)
