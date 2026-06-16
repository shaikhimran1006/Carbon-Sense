from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CarbonLogBase(BaseModel):
    pass


class CarbonLogResponse(BaseModel):
    id: int
    transport_co2: float
    energy_co2: float
    food_co2: float
    lifestyle_co2: float
    total_co2: float
    transport_percent: float
    energy_percent: float
    food_percent: float
    lifestyle_percent: float
    carbon_score: int
    created_at: datetime

    class Config:
        from_attributes = True


class CarbonBreakdown(BaseModel):
    category: str
    co2: float
    percentage: float


class Recommendation(BaseModel):
    title: str
    description: str
    difficulty: str
    expected_reduction: float
    impact: str


class SimulationRequest(BaseModel):
    vehicle_type: Optional[str] = None
    daily_distance_km: Optional[float] = None
    weekly_frequency: Optional[int] = None
    monthly_electricity_kwh: Optional[float] = None
    monthly_gas_m3: Optional[float] = None
    diet_type: Optional[str] = None
    weekly_meat_days: Optional[int] = None


class SimulationResult(BaseModel):
    before_total: float
    after_total: float
    reduction_kg: float
    reduction_percent: float
    breakdown: List[CarbonBreakdown]


class AssistantRequest(BaseModel):
    message: str


class AssistantResponse(BaseModel):
    response: str
    recommendations: Optional[List[Recommendation]] = None
