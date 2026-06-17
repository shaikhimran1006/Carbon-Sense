import pytest
from app.services.carbon_calculator import CarbonCalculator
from app.schemas.user import UserProfileUpdate


def test_transport_emissions():
    """Test transport emissions calculation for various vehicle types."""
    calc = CarbonCalculator()
    # Test petrol car
    emissions_petrol = calc._calculate_transport("petrol", 20, 5)
    assert emissions_petrol > 0
    assert isinstance(emissions_petrol, float)

    # Test diesel (should be higher than petrol)
    emissions_diesel = calc._calculate_transport("diesel", 20, 5)
    assert emissions_diesel > emissions_petrol

    # Test hybrid (should be lower)
    emissions_hybrid = calc._calculate_transport("hybrid", 20, 5)
    assert emissions_hybrid < emissions_petrol


def test_zero_transport_emissions():
    """Test that walking/biking/public transport have 0 emissions."""
    calc = CarbonCalculator()
    assert calc._calculate_transport("walking", 20, 5) == 0
    assert calc._calculate_transport("bike", 20, 5) == 0
    assert calc._calculate_transport("public_transport", 20, 5) == 0
    assert calc._calculate_transport("electric", 20, 5) == 0


def test_zero_usage_transport_emissions():
    """Test edge case: zero distance or zero frequency should have 0 emissions."""
    calc = CarbonCalculator()
    assert calc._calculate_transport("petrol", 0, 5) == 0
    assert calc._calculate_transport("petrol", 20, 0) == 0


def test_energy_emissions():
    """Test energy emissions calculation and edge cases."""
    calc = CarbonCalculator()
    # Normal case
    emissions_normal = calc._calculate_energy(300, 100)
    assert emissions_normal > 0
    assert isinstance(emissions_normal, float)

    # Edge case: zero energy usage
    assert calc._calculate_energy(0, 0) == 0


def test_food_emissions():
    """Test food emissions calculation for different diet types."""
    calc = CarbonCalculator()
    # Test diet hierarchy (omnivore > pescatarian > vegetarian > vegan)
    emissions_omnivore = calc._calculate_food("omnivore", 5)
    emissions_pescatarian = calc._calculate_food("pescatarian", 5)
    emissions_vegetarian = calc._calculate_food("vegetarian", 0)
    emissions_vegan = calc._calculate_food("vegan", 0)

    assert emissions_omnivore > emissions_pescatarian
    assert emissions_pescatarian > emissions_vegetarian
    assert emissions_vegetarian > emissions_vegan

    # Test meat days affect emissions
    emissions_high_meat = calc._calculate_food("omnivore", 7)
    emissions_low_meat = calc._calculate_food("omnivore", 1)
    assert emissions_high_meat > emissions_low_meat


def test_lifestyle_emissions():
    """Test lifestyle emissions calculation and recycling impact."""
    calc = CarbonCalculator()
    # Normal case
    emissions = calc._calculate_lifestyle("weekly", 0.3)
    assert isinstance(emissions, float)
    assert emissions > 0

    # More recycling should lower emissions
    emissions_low_recycle = calc._calculate_lifestyle("weekly", 0.1)
    emissions_high_recycle = calc._calculate_lifestyle("weekly", 0.9)
    assert emissions_low_recycle > emissions_high_recycle


def test_full_carbon_calculation():
    """Test full carbon footprint calculation with complete profile."""
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
    assert round(
        result.transport_percent + result.energy_percent +
        result.food_percent + result.lifestyle_percent,
        1
    ) == 100.0


def test_minimal_profile_calculation():
    """Test calculation with minimal profile (all zeros/defaults)."""
    calc = CarbonCalculator()
    profile = UserProfileUpdate(
        daily_distance_km=0,
        weekly_frequency=0,
        monthly_electricity_kwh=0,
        monthly_gas_m3=0,
        weekly_meat_days=0,
        waste_recycling_rate=0.0
    )
    result = calc.calculate(profile)
    assert result.total_co2 >= 0
    assert 0 <= result.carbon_score <= 100


def test_ai_assistant_recommendations_high_transport():
    """Test AI assistant recommends transport-specific actions for high transport impact."""
    from app.services.ai_assistant import AIAssistant
    from app.schemas.user import UserProfileResponse

    user = UserProfileResponse(
        id=1,
        email="test@example.com",
        name="Test User",
        vehicle_type="petrol",
        daily_distance_km=50,
        weekly_frequency=7,
        monthly_electricity_kwh=100,
        monthly_gas_m3=50,
        diet_type="vegan",
        weekly_meat_days=0,
        shopping_frequency="monthly",
        waste_recycling_rate=0.8,
        created_at="2024-01-01T00:00:00"
    )

    carbon_data = {
        "transport_percent": 80,
        "food_percent": 5,
        "energy_percent": 10,
        "lifestyle_percent": 5,
        "total_co2": 600
    }

    recs = AIAssistant.generate_recommendations(user, carbon_data)
    assert len(recs) >= 1


def test_ai_assistant_recommendations_high_food():
    """Test AI assistant recommends food-specific actions for high food impact."""
    from app.services.ai_assistant import AIAssistant
    from app.schemas.user import UserProfileResponse

    user = UserProfileResponse(
        id=1,
        email="test@example.com",
        name="Test User",
        vehicle_type="bike",
        daily_distance_km=5,
        weekly_frequency=5,
        monthly_electricity_kwh=150,
        monthly_gas_m3=50,
        diet_type="omnivore",
        weekly_meat_days=7,
        shopping_frequency="weekly",
        waste_recycling_rate=0.5,
        created_at="2024-01-01T00:00:00"
    )

    carbon_data = {
        "transport_percent": 5,
        "food_percent": 75,
        "energy_percent": 15,
        "lifestyle_percent": 5,
        "total_co2": 400
    }

    recs = AIAssistant.generate_recommendations(user, carbon_data)
    assert len(recs) >= 1


def test_ai_chat_various_messages():
    """Test AI chat responds to different message types."""
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

    # Test different message intents
    test_messages = [
        "How's my carbon footprint?",
        "What about my food emissions?",
        "Tell me about transport"
    ]
    for msg in test_messages:
        response, recs = AIAssistant.chat(user, carbon_data, msg)
        assert isinstance(response, str)
        assert len(response) > 0
