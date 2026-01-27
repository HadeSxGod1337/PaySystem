from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Account(Base):
    """User account model"""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Numeric(10, 2, asdecimal=True), default=Decimal("0.00"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="accounts")
