from typing import Dict, Any, List, Tuple
from app.models.user import User
from app.schemas.carbon import CarbonBreakdown


class CarbonCalculator:
    VEHICLE_FACTORS = {
        "petrol": 0.21,
        "diesel": 0.27,
        "electric": 0.05,
        "hybrid": 0.12,
        "public_transport": 0.08,
        "bike": 0.0,
        "walking": 0.0
    }

    DIET_FACTORS = {
        "omnivore": 2.5,
        "vegetarian": 1.7,
        "vegan": 1.5,
        "pescatarian": 1.9
    }

    ELECTRICITY_FACTOR = 0.5
    GAS_FACTOR = 2.0
    SHOPPING_FACTOR = 10
    WASTE_BASE = 30

    @classmethod
    def calculate_transport(cls, user: User) -> float:
        factor = cls.VEHICLE_FACTORS.get(user.vehicle_type or "petrol", 0.21)
        monthly_km = user.daily_distance_km * user.weekly_frequency * 4.33
        return monthly_km * factor

    @classmethod
    def calculate_energy(cls, user: User) -> float:
        electricity = user.monthly_electricity_kwh * cls.ELECTRICITY_FACTOR
        gas = user.monthly_gas_m3 * cls.GAS_FACTOR
        return electricity + gas

    @classmethod
    def calculate_food(cls, user: User) -> float:
        base = cls.DIET_FACTORS.get(user.diet_type or "omnivore", 2.5)
        meat_multiplier = 1 + (user.weekly_meat_days / 7) * 0.5
        return base * 30 * meat_multiplier

    @classmethod
    def calculate_lifestyle(cls, user: User) -> float:
        shopping_freq_map = {"weekly": 1, "biweekly": 0.7, "monthly": 0.5}
        shopping_factor = shopping_freq_map.get(user.shopping_frequency or "weekly", 1)
        shopping = cls.SHOPPING_FACTOR * shopping_factor
        waste = cls.WASTE_BASE * (1 - user.waste_recycling_rate)
        return shopping + waste

    @classmethod
    def calculate_all(cls, user: User) -> Dict[str, float]:
        transport = cls.calculate_transport(user)
        energy = cls.calculate_energy(user)
        food = cls.calculate_food(user)
        lifestyle = cls.calculate_lifestyle(user)
        total = transport + energy + food + lifestyle

        if total > 0:
            transport_pct = (transport / total) * 100
            energy_pct = (energy / total) * 100
            food_pct = (food / total) * 100
            lifestyle_pct = (lifestyle / total) * 100
        else:
            transport_pct = energy_pct = food_pct = lifestyle_pct = 0

        score = cls.calculate_score(total)

        return {
            "transport_co2": transport,
            "energy_co2": energy,
            "food_co2": food,
            "lifestyle_co2": lifestyle,
            "total_co2": total,
            "transport_percent": transport_pct,
            "energy_percent": energy_pct,
            "food_percent": food_pct,
            "lifestyle_percent": lifestyle_pct,
            "carbon_score": score
        }

    @classmethod
    def calculate_score(cls, total_co2: float) -> int:
        if total_co2 <= 100:
            return 100
        elif total_co2 <= 200:
            return 85
        elif total_co2 <= 300:
            return 70
        elif total_co2 <= 400:
            return 55
        elif total_co2 <= 500:
            return 40
        elif total_co2 <= 600:
            return 25
        else:
            return 10

    @classmethod
    def get_breakdown(cls, data: Dict[str, float]) -> List[CarbonBreakdown]:
        return [
            CarbonBreakdown(category="Transport", co2=data["transport_co2"], percentage=data["transport_percent"]),
            CarbonBreakdown(category="Energy", co2=data["energy_co2"], percentage=data["energy_percent"]),
            CarbonBreakdown(category="Food", co2=data["food_co2"], percentage=data["food_percent"]),
            CarbonBreakdown(category="Lifestyle", co2=data["lifestyle_co2"], percentage=data["lifestyle_percent"])
        ]

    @classmethod
    def simulate_from_params(cls, params: Dict[str, Any], base_user: User) -> Dict[str, float]:
        simulated_user = User(
            vehicle_type=params.get("vehicle_type", base_user.vehicle_type),
            daily_distance_km=params.get("daily_distance_km", base_user.daily_distance_km),
            weekly_frequency=params.get("weekly_frequency", base_user.weekly_frequency),
            monthly_electricity_kwh=params.get("monthly_electricity_kwh", base_user.monthly_electricity_kwh),
            monthly_gas_m3=params.get("monthly_gas_m3", base_user.monthly_gas_m3),
            diet_type=params.get("diet_type", base_user.diet_type),
            weekly_meat_days=params.get("weekly_meat_days", base_user.weekly_meat_days),
            shopping_frequency=base_user.shopping_frequency,
            waste_recycling_rate=base_user.waste_recycling_rate
        )
        return cls.calculate_all(simulated_user)
