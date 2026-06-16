from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)

    vehicle_type = Column(String, nullable=True)
    daily_distance_km = Column(Float, default=0.0)
    weekly_frequency = Column(Integer, default=5)

    monthly_electricity_kwh = Column(Float, default=0.0)
    monthly_gas_m3 = Column(Float, default=0.0)

    diet_type = Column(String, default="omnivore")
    weekly_meat_days = Column(Integer, default=5)

    shopping_frequency = Column(String, default="weekly")
    waste_recycling_rate = Column(Float, default=0.3)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    carbon_logs = relationship("CarbonLog", back_populates="user", cascade="all, delete-orphan")
