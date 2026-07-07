from enum import Enum
from pydantic import BaseModel, Field

class PaymentRule(str, Enum):
    FIXED = "fijo"
    PERCENTAGE = "porcentaje"
    MINIMUM_GUARANTEE = "garantia_minima"

class ContractRules(BaseModel):
    actor: str
    rule: PaymentRule
    value: float

class PayrollRequest(BaseModel):
    contract_text: str
    box_office_total: float = Field(..., gt=0, description="Total neto de taquilla")

class PayrollResponse(BaseModel):
    actor: str
    gross: float
    deductions: float
    net: float
    concept: str