from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.carbon import CarbonLog
from app.schemas.carbon import (
    CarbonLogResponse,
    CarbonBreakdown,
    Recommendation,
    SimulationRequest,
    SimulationResult,
    AssistantRequest,
    AssistantResponse
)
from app.services.carbon_calculator import CarbonCalculator
from app.services.ai_assistant import AIAssistant

router = APIRouter(prefix="/carbon", tags=["Carbon"])


@router.post("/calculate", response_model=CarbonLogResponse)
def calculate_carbon(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = CarbonCalculator.calculate_all(current_user)
    log = CarbonLog(user_id=current_user.id, **data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/history", response_model=List[CarbonLogResponse])
def get_history(
    skip: int = 0,
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(CarbonLog)
        .filter(CarbonLog.user_id == current_user.id)
        .order_by(CarbonLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return logs


@router.get("/latest", response_model=CarbonLogResponse)
def get_latest(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest = (
        db.query(CarbonLog)
        .filter(CarbonLog.user_id == current_user.id)
        .order_by(CarbonLog.created_at.desc())
        .first()
    )
    if not latest:
        return calculate_carbon(current_user, db)
    return latest


@router.get("/recommendations", response_model=List[Recommendation])
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest = (
        db.query(CarbonLog)
        .filter(CarbonLog.user_id == current_user.id)
        .order_by(CarbonLog.created_at.desc())
        .first()
    )
    if not latest:
        data = CarbonCalculator.calculate_all(current_user)
    else:
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
    base_data = CarbonCalculator.calculate_all(current_user)
    sim_data = CarbonCalculator.simulate_from_params(
        sim_request.model_dump(exclude_unset=True),
        current_user
    )
    before = base_data["total_co2"]
    after = sim_data["total_co2"]
    reduction = before - after
    reduction_pct = (reduction / before) * 100 if before > 0 else 0
    breakdown = CarbonCalculator.get_breakdown(sim_data)
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
    latest = (
        db.query(CarbonLog)
        .filter(CarbonLog.user_id == current_user.id)
        .order_by(CarbonLog.created_at.desc())
        .first()
    )
    if not latest:
        data = CarbonCalculator.calculate_all(current_user)
    else:
        data = {
            "transport_percent": latest.transport_percent,
            "energy_percent": latest.energy_percent,
            "food_percent": latest.food_percent,
            "lifestyle_percent": latest.lifestyle_percent,
            "total_co2": latest.total_co2
        }
    response, recs = AIAssistant.chat(current_user, data, request.message)
    return AssistantResponse(response=response, recommendations=recs)
