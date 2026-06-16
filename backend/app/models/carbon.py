from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class CarbonLog(Base):
    __tablename__ = "carbon_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    transport_co2 = Column(Float, default=0.0)
    energy_co2 = Column(Float, default=0.0)
    food_co2 = Column(Float, default=0.0)
    lifestyle_co2 = Column(Float, default=0.0)
    total_co2 = Column(Float, default=0.0)

    transport_percent = Column(Float, default=0.0)
    energy_percent = Column(Float, default=0.0)
    food_percent = Column(Float, default=0.0)
    lifestyle_percent = Column(Float, default=0.0)

    carbon_score = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="carbon_logs")
