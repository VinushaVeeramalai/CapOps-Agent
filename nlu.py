import re
from pydantic import BaseModel, Field
from typing import Optional

class NLUResult(BaseModel):
    intent: str = Field(description="Must be one of: IT_ACCESS_REQUEST, HR_LEAVE_QUERY, INVOICE_STATUS, PASSWORD_RESET, ONBOARDING_HELP, COMPLAINT, GENERAL")
    employee_id: Optional[str] = Field(None, description="Employee ID like CG-1234 extracted from text")
    department: Optional[str] = Field(None)
    date_range: Optional[str] = Field(None)
    ticket_id: Optional[str] = Field(None)
    system_name: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)
    language: str = Field(description="Detected language code, e.g., en, hi, ta, fr. Auto-detect from text.")

def classify_intent(text: str) -> dict:
    lowered = (text or "").lower()
    employee_id_match = re.search(r"\bCG-\d{4}\b", text or "", re.IGNORECASE)
    employee_id = employee_id_match.group(0).upper() if employee_id_match else None

    intent = "GENERAL"
    if any(k in lowered for k in ["password", "reset", "otp", "login issue"]):
        intent = "PASSWORD_RESET"
    elif any(k in lowered for k in ["access", "permission", "vpn", "sap access"]):
        intent = "IT_ACCESS_REQUEST"
    elif any(k in lowered for k in ["leave", "vacation", "pto", "holiday"]):
        intent = "HR_LEAVE_QUERY"
    elif any(k in lowered for k in ["invoice", "billing", "payment status"]):
        intent = "INVOICE_STATUS"
    elif any(k in lowered for k in ["onboarding", "new joiner", "first day"]):
        intent = "ONBOARDING_HELP"
    elif any(k in lowered for k in ["angry", "frustrated", "complaint", "worst"]):
        intent = "COMPLAINT"

    system_name = None
    for candidate in ["sap", "workday", "vpn", "jira", "email"]:
        if candidate in lowered:
            system_name = candidate.upper()
            break

    language = "en"
    if re.search(r"[\u0900-\u097F]", text or ""):
        language = "hi"

    result = NLUResult(
        intent=intent,
        employee_id=employee_id,
        department=None,
        date_range=None,
        ticket_id=None,
        system_name=system_name,
        priority="P1" if intent == "COMPLAINT" else "P3",
        language=language,
    )
    return result.dict()
