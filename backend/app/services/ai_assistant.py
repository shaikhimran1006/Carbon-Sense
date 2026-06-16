from typing import List, Optional
from app.models.user import User
from app.schemas.carbon import Recommendation


class AIAssistant:
    @classmethod
    def generate_recommendations(cls, user: User, carbon_data: dict) -> List[Recommendation]:
        recommendations = []

        if carbon_data["transport_percent"] >= 40:
            recommendations.append(Recommendation(
                title="Use public transport twice weekly",
                description="Switching to buses or trains 2 days a week can significantly reduce your transport emissions.",
                difficulty="easy",
                expected_reduction=25.0,
                impact=f"Reduce {25.0}kg CO2/month"
            ))
            recommendations.append(Recommendation(
                title="Carpool with colleagues",
                description="Share rides with friends or colleagues to cut your transport footprint in half.",
                difficulty="easy",
                expected_reduction=15.0,
                impact=f"Reduce {15.0}kg CO2/month"
            ))

        if carbon_data["energy_percent"] >= 30:
            recommendations.append(Recommendation(
                title="Switch to LED bulbs",
                description="LED bulbs use 75% less energy than incandescent bulbs.",
                difficulty="easy",
                expected_reduction=12.0,
                impact=f"Reduce {12.0}kg CO2/month"
            ))
            recommendations.append(Recommendation(
                title="Reduce AC usage by 2°C",
                description="Small temperature adjustments make a big difference over time.",
                difficulty="medium",
                expected_reduction=20.0,
                impact=f"Reduce {20.0}kg CO2/month"
            ))

        if carbon_data["food_percent"] >= 35:
            recommendations.append(Recommendation(
                title="Try meat-free Mondays",
                description="One day without meat each week is a great start.",
                difficulty="easy",
                expected_reduction=18.0,
                impact=f"Reduce {18.0}kg CO2/month"
            ))
            recommendations.append(Recommendation(
                title="Buy local produce",
                description="Reducing food miles lowers your food carbon footprint.",
                difficulty="medium",
                expected_reduction=10.0,
                impact=f"Reduce {10.0}kg CO2/month"
            ))

        if not recommendations:
            recommendations.append(Recommendation(
                title="Start with small changes",
                description="You're already doing great! Try incorporating one new habit this week.",
                difficulty="easy",
                expected_reduction=5.0,
                impact=f"Reduce {5.0}kg CO2/month"
            ))

        return recommendations[:4]

    @classmethod
    def chat(cls, user: User, carbon_data: dict, message: str) -> tuple[str, Optional[List[Recommendation]]]:
        lower_msg = message.lower()
        response_parts = []

        if "travel" in lower_msg or "car" in lower_msg or "transport" in lower_msg:
            transport_pct = round(carbon_data["transport_percent"], 1)
            response_parts.append(f"Your transport contributes {transport_pct}% of your footprint.")
        elif "food" in lower_msg or "diet" in lower_msg or "meat" in lower_msg:
            food_pct = round(carbon_data["food_percent"], 1)
            response_parts.append(f"Your food choices contribute {food_pct}% of your footprint.")
        elif "energy" in lower_msg or "electricity" in lower_msg:
            energy_pct = round(carbon_data["energy_percent"], 1)
            response_parts.append(f"Your home energy contributes {energy_pct}% of your footprint.")
        else:
            total = round(carbon_data["total_co2"], 1)
            response_parts.append(f"Your total monthly carbon footprint is {total}kg CO2.")

        recommendations = cls.generate_recommendations(user, carbon_data)

        response = " ".join(response_parts)
        if not response:
            response = "Here are some personalized recommendations for you!"

        return response, recommendations
