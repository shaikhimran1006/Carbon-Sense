import pytest
from app.services.carbon_calculator import CarbonCalculator
from app.models.user import User


def test_transport_calculation():
    user = User(vehicle_type="petrol", daily_distance_km=30, weekly_frequency=5)
    result = CarbonCalculator.calculate_transport(user)
    assert result > 0


def test_energy_calculation():
    user = User(monthly_electricity_kwh=300, monthly_gas_m3=50)
    result = CarbonCalculator.calculate_energy(user)
    assert result > 0


def test_food_calculation():
    user = User(diet_type="omnivore", weekly_meat_days=5)
    result = CarbonCalculator.calculate_food(user)
    assert result > 0


def test_full_calculation():
    user = User(
        vehicle_type="petrol",
        daily_distance_km=30,
        weekly_frequency=5,
        monthly_electricity_kwh=300,
        monthly_gas_m3=50,
        diet_type="omnivore",
        weekly_meat_days=5,
        shopping_frequency="weekly",
        waste_recycling_rate=0.3
    )
    data = CarbonCalculator.calculate_all(user)
    assert "total_co2" in data
    assert data["total_co2"] > 0
    assert 0 <= data["carbon_score"] <= 100
