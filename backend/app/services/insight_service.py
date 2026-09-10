"""
services/insight_service.py
Generates a short, human-readable actionable insight summary
for the sales/support team based on all analyzed signals.
"""

import logging

logger = logging.getLogger("insight_service")


class InsightService:
    def generate(self, category: str, priority: str, industry: str = None,
                 budget_inr: float = None, entities: dict = None) -> str:
        parts = [f"{priority} priority {category} enquiry"]

        if industry:
            parts.append(f"from the {industry} industry")

        if budget_inr:
            parts.append(f"with an indicated budget of ₹{budget_inr:,.0f}")

        if entities:
            if entities.get("email"):
                parts.append(f"Contact email captured: {entities['email']}.")
            if entities.get("organizations"):
                orgs = ", ".join(entities["organizations"][:2])
                parts.append(f"Mentioned organization(s): {orgs}.")

        recommendation = self._recommend_action(priority)
        insight = " ".join(parts) + f". {recommendation}"

        logger.info("Generated insight: %s", insight)
        return insight

    @staticmethod
    def _recommend_action(priority: str) -> str:
        if priority == "High":
            return "Recommend immediate follow-up within 24 hours."
        if priority == "Medium":
            return "Recommend follow-up within 2-3 business days."
        return "Can be added to the standard nurture/follow-up queue."


insight_service = InsightService()
