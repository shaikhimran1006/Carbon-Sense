from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    vehicle_type: Optional[str] = None
    daily_distance_km: Optional[float] = None
    weekly_frequency: Optional[int] = None
    monthly_electricity_kwh: Optional[float] = None
    monthly_gas_m3: Optional[float] = None
    diet_type: Optional[str] = None
    weekly_meat_days: Optional[int] = None
    shopping_frequency: Optional[str] = None
    waste_recycling_rate: Optional[float] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    location: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
