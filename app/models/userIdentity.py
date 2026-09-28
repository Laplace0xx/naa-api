from datetime import date, datetime

from sqlalchemy import ForeignKey, Enum as SQLEnum, String

from app.models.base import Base
from enum import  Enum
from sqlalchemy.orm import Mapped, mapped_column

class Creds(Enum):
    NIN = "nin"
    BVN = "bvn"

class UserIdentity(Base):
    __tablename__ = "user_identity"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    cred: Mapped[Creds] = mapped_column(SQLEnum(Creds, name="cred_type"), unique=True)
    hmac_vale: Mapped[str] = mapped_column(String(30))
    verified_at: Mapped[date] = mapped_column(default=datetime.utcnow)