from src.domain.entities import ContractRules, PayrollRequest, PayrollResponse, PaymentRule
from src.application.ports import AIExtractorPort, CalculationRepositoryPort

class PayrollCalculator:
    def __init__(self, ai_extractor: AIExtractorPort, repository: CalculationRepositoryPort, withholding_rate: float):
        self.ai_extractor = ai_extractor
        self.repository = repository
        self.withholding_rate = withholding_rate

    async def calculate(self, request: PayrollRequest) -> PayrollResponse:
        rules: ContractRules = await self.ai_extractor.extract_rules(request.contract_text)

        gross = 0.0
        concept = ""

        if rules.rule == PaymentRule.FIXED:
            gross = rules.value
            concept = f"Pago fijo de ${rules.value:,.0f} COP"
        elif rules.rule == PaymentRule.PERCENTAGE:
            gross = request.box_office_total * (rules.value / 100)
            concept = f"{rules.value}% de la taquilla (${request.box_office_total:,.0f} COP)"
        elif rules.rule == PaymentRule.MINIMUM_GUARANTEE:
            percentage_calc = request.box_office_total * (rules.value / 100)
            gross = max(percentage_calc, rules.value)
            concept = f"Máximo entre garantía de ${rules.value:,.0f} COP y {rules.value}% de taquilla"

        deductions = gross * self.withholding_rate
        net = gross - deductions

        response = PayrollResponse(
            actor=rules.actor,
            gross=round(gross, 2),
            deductions=round(deductions, 2),
            net=round(net, 2),
            concept=concept
        )

        await self.repository.save(response)
        return response