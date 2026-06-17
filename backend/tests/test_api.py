import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_user():
    """Test user registration endpoint"""
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password12345", "name": "Test User"}
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email():
    """Test registration with duplicate email fails"""
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password12345", "name": "Test User 1"}
    )
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password12345", "name": "Test User 2"}
    )
    assert response.status_code == 409


def test_login_user():
    """Test user login endpoint"""
    # First register a user
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password12345", "name": "Login Test"}
    )
    # Then log in
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password12345"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    """Test login fails with wrong password"""
    client.post(
        "/auth/register",
        json={"email": "wrong@example.com", "password": "password12345", "name": "Wrong Test"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword123"}
    )
    assert response.status_code == 401


def test_calculate_carbon():
    """Test carbon calculation endpoint"""
    # Register and log in
    register_res = client.post(
        "/auth/register",
        json={"email": "carbon@example.com", "password": "password12345", "name": "Carbon Test"}
    )
    token = register_res.json()["access_token"]

    # Update user profile
    client.put(
        "/users/me",
        json={
            "vehicle_type": "petrol",
            "daily_distance_km": 20,
            "weekly_frequency": 5,
            "monthly_electricity_kwh": 300,
            "monthly_gas_m3": 100,
            "diet_type": "omnivore",
            "weekly_meat_days": 5,
            "shopping_frequency": "weekly",
            "waste_recycling_rate": 0.3
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Calculate carbon
    response = client.post(
        "/carbon/calculate",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_co2" in data
    assert "carbon_score" in data
    assert data["total_co2"] > 0
    assert 0 <= data["carbon_score"] <= 100


def test_get_carbon_recommendations():
    """Test recommendations endpoint"""
    register_res = client.post(
        "/auth/register",
        json={"email": "recs@example.com", "password": "password12345", "name": "Recs Test"}
    )
    token = register_res.json()["access_token"]

    response = client.get(
        "/carbon/recommendations",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_simulator():
    """Test carbon simulator endpoint"""
    register_res = client.post(
        "/auth/register",
        json={"email": "sim@example.com", "password": "password12345", "name": "Sim Test"}
    )
    token = register_res.json()["access_token"]

    response = client.post(
        "/carbon/simulate",
        json={"diet_type": "vegan"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "before_total" in response.json()
    assert "after_total" in response.json()
