import pytest
from app.services.carbon_calculator import CarbonCalculator
from app.schemas.user import UserProfileUpdate


def test_transport_emissions():
    """Test transport emissions calculation"""
    calc = CarbonCalculator()
    emissions = calc._calculate_transport("petrol", 20, 5)
    assert emissions > 0
    assert isinstance(emissions, float)


def test_low_transport_emissions():
    """Test that walking/biking has 0 emissions"""
    calc = CarbonCalculator()
    emissions_walk = calc._calculate_transport("walking", 20, 5)
    emissions_bike = calc._calculate_transport("bike", 20, 5)
    assert emissions_walk == 0
    assert emissions_bike == 0


def test_energy_emissions():
    """Test energy emissions calculation"""
    calc = CarbonCalculator()
    emissions = calc._calculate_energy(300, 100)
    assert emissions > 0
    assert isinstance(emissions, float)


def test_food_emissions():
    """Test food emissions calculation"""
    calc = CarbonCalculator()
    emissions_omnivore = calc._calculate_food("omnivore", 5)
    emissions_vegan = calc._calculate_food("vegan", 0)
    assert emissions_omnivore > emissions_vegan


def test_lifestyle_emissions():
    """Test lifestyle emissions calculation"""
    calc = CarbonCalculator()
    emissions = calc._calculate_lifestyle("weekly", 0.3)
    assert isinstance(emissions, float)


def test_full_carbon_calculation():
    """Test full carbon footprint calculation"""
    calc = CarbonCalculator()
    profile = UserProfileUpdate(
        vehicle_type="petrol",
        daily_distance_km=20,
        weekly_frequency=5,
        monthly_electricity_kwh=300,
        monthly_gas_m3=100,
        diet_type="omnivore",
        weekly_meat_days=5,
        shopping_frequency="weekly",
        waste_recycling_rate=0.3
    )
    result = calc.calculate(profile)
    assert result.total_co2 > 0
    assert 0 <= result.carbon_score <= 100
    assert (
        round(result.transport_percent + result.energy_percent +
              result.food_percent + result.lifestyle_percent, 1)
        == 100.0
    )


def test_ai_assistant_recommendations():
    """Test that AI assistant recommendations are generated"""
    from app.services.ai_assistant import AIAssistant
    from app.schemas.user import UserProfileResponse
    from app.schemas.carbon import CarbonLogResponse

    user = UserProfileResponse(
        id=1,
        email="test@example.com",
        name="Test User",
        vehicle_type="petrol",
        daily_distance_km=20,
        weekly_frequency=5,
        monthly_electricity_kwh=300,
        monthly_gas_m3=100,
        diet_type="omnivore",
        weekly_meat_days=5,
        shopping_frequency="weekly",
        waste_recycling_rate=0.3,
        created_at="2024-01-01T00:00:00"
    )

    carbon_data = {
        "transport_percent": 50,
        "food_percent": 30,
        "energy_percent": 15,
        "lifestyle_percent": 5,
        "total_co2": 400
    }

    recs = AIAssistant.generate_recommendations(user, carbon_data)
    assert len(recs) >= 1
    assert all(hasattr(r, "title") for r in recs)
    assert all(hasattr(r, "difficulty") for r in recs)


def test_ai_chat():
    """Test AI chat functionality"""
    from app.services.ai_assistant import AIAssistant
    from app.schemas.user import UserProfileResponse

    user = UserProfileResponse(
        id=1,
        email="test@example.com",
        name="Test User",
        vehicle_type="petrol",
        daily_distance_km=20,
        weekly_frequency=5,
        monthly_electricity_kwh=300,
        monthly_gas_m3=100,
        diet_type="omnivore",
        weekly_meat_days=5,
        shopping_frequency="weekly",
        waste_recycling_rate=0.3,
        created_at="2024-01-01T00:00:00"
    )

    carbon_data = {
        "transport_percent": 50,
        "food_percent": 30,
        "energy_percent": 15,
        "lifestyle_percent": 5,
        "total_co2": 400
    }

    msg, recs = AIAssistant.chat(user, carbon_data, "What should I do?")
    assert isinstance(msg, str)
    assert len(msg) > 0
    assert recs is not None
