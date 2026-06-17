"""Repository layer for CarbonLog database operations to reduce code duplication."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.carbon import CarbonLog
from app.models.user import User


class CarbonRepository:
    """Repository class for handling CarbonLog database operations."""

    @staticmethod
    def get_latest(db: Session, user: User) -> Optional[CarbonLog]:
        """
        Get the most recent CarbonLog entry for a user.

        Args:
            db: SQLAlchemy database session
            user: User to get log for

        Returns:
            Latest CarbonLog or None if none exists
        """
        return (
            db.query(CarbonLog)
            .filter(CarbonLog.user_id == user.id)
            .order_by(CarbonLog.created_at.desc())
            .first()
        )

    @staticmethod
    def get_history(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 30
    ) -> List[CarbonLog]:
        """
        Get paginated CarbonLog history for a user.

        Args:
            db: SQLAlchemy database session
            user: User to get history for
            skip: Number of entries to skip
            limit: Maximum number of entries to return

        Returns:
            List of CarbonLog entries
        """
        return (
            db.query(CarbonLog)
            .filter(CarbonLog.user_id == user.id)
            .order_by(CarbonLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, user: User, data: dict) -> CarbonLog:
        """
        Create and save a new CarbonLog entry.

        Args:
            db: SQLAlchemy database session
            user: User to create log for
            data: CarbonLog data

        Returns:
            Created CarbonLog entry
        """
        log = CarbonLog(user_id=user.id, **data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_or_calculate_latest(
        db: Session,
        user: User,
        calculator
    ) -> CarbonLog:
        """
        Get latest log, or calculate and create a new one if none exists.

        Args:
            db: SQLAlchemy database session
            user: User to get log for
            calculator: CarbonCalculator instance to use for calculation

        Returns:
            Existing or newly created CarbonLog
        """
        latest = CarbonRepository.get_latest(db, user)
        if not latest:
            data = calculator.calculate_all(user)
            latest = CarbonRepository.create(db, user, data)
        return latest
