"""Carbon footprint API endpoints with refactored repository layer and improved code quality.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.carbon import (
    CarbonLogResponse,
    Recommendation,
    SimulationRequest,
    SimulationResult,
    AssistantRequest,
    AssistantResponse
)
from app.services.carbon_calculator import CarbonCalculator
from app.services.ai_assistant import AIAssistant
from app.services.carbon_repository import CarbonRepository

router = APIRouter(prefix="/carbon", tags=["Carbon"])


@router.post("/calculate", response_model=CarbonLogResponse)
def calculate_carbon(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate and save new carbon footprint entry for current user.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Newly created CarbonLog with footprint data
    """
    calculator = CarbonCalculator()
    data = calculator.calculate_all(current_user)
    return CarbonRepository.create(db, current_user, data)


@router.get("/history", response_model=List[CarbonLogResponse])
def get_history(
    skip: int = 0,
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve paginated carbon footprint history for current user.

    Args:
        skip: Number of entries to skip
        limit: Max number of entries to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of CarbonLog entries sorted from newest to oldest
    """
    return CarbonRepository.get_history(db, current_user, skip, limit)


@router.get("/latest", response_model=CarbonLogResponse)
def get_latest(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get latest carbon footprint for current user (calculate if needed).

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Most recent (or newly calculated) CarbonLog entry
    """
    calculator = CarbonCalculator()
    return CarbonRepository.get_or_calculate_latest(db, current_user, calculator)


@router.get("/recommendations", response_model=List[Recommendation])
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate personalized carbon reduction recommendations.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        List of personalized recommendations
    """
    calculator = CarbonCalculator()
    latest = CarbonRepository.get_or_calculate_latest(db, current_user, calculator)
    data = {
        "transport_percent": latest.transport_percent,
        "energy_percent": latest.energy_percent,
        "food_percent": latest.food_percent,
        "lifestyle_percent": latest.lifestyle_percent,
        "total_co2": latest.total_co2
    }
    return AIAssistant.generate_recommendations(current_user, data)


@router.post("/simulate", response_model=SimulationResult)
def simulate_changes(
    sim_request: SimulationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate the impact of lifestyle changes on carbon footprint.

    Args:
        sim_request: Lifestyle changes to simulate
        current_user: Authenticated user
        db: Database session

    Returns:
        Simulation results showing before/after comparison
    """
    calculator = CarbonCalculator()
    base_data = calculator.calculate_all(current_user)
    sim_data = calculator.simulate_from_params(
        sim_request.model_dump(exclude_unset=True),
        current_user
    )
    before = base_data["total_co2"]
    after = sim_data["total_co2"]
    reduction = before - after
    reduction_pct = (reduction / before) * 100 if before > 0 else 0.0
    breakdown = calculator.get_breakdown(sim_data)
    return SimulationResult(
        before_total=before,
        after_total=after,
        reduction_kg=reduction,
        reduction_percent=reduction_pct,
        breakdown=breakdown
    )


@router.post("/assistant", response_model=AssistantResponse)
def chat_with_assistant(
    request: AssistantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI-powered personal climate assistant.

    Args:
        request: User's chat message
        current_user: Authenticated user
        db: Database session

    Returns:
        Assistant's response and optional recommendations
    """
    calculator = CarbonCalculator()
    latest = CarbonRepository.get_or_calculate_latest(db, current_user, calculator)
    data = {
        "transport_percent": latest.transport_percent,
        "energy_percent": latest.energy_percent,
        "food_percent": latest.food_percent,
        "lifestyle_percent": latest.lifestyle_percent,
        "total_co2": latest.total_co2
    }
    response, recs = AIAssistant.chat(current_user, data, request.message)
    return AssistantResponse(response=response, recommendations=recs)
