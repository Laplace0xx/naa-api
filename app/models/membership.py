from datetime import date, datetime

from enum import Enum
from sqlalchemy import ForeignKey, Enum as SQLEnum

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class MembershipStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"

class Membership(Base):
    __tablename__ = "memberships"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    membership_status: Mapped[MembershipStatus] = mapped_column(SQLEnum(MembershipStatus, name="membership_status"))
    issued_at: Mapped[date] = mapped_column(default=datetime.utcnow)