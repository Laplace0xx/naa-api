from datetime import date, datetime
from enum import Enum
from sqlalchemy import String, Enum as SQLEnum
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class UserRole(Enum):
    ADMIN = "admin"
    AUCTIONEER = "auctioneer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    f_name: Mapped[str] = mapped_column(String(255))
    l_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True)
    gender:Mapped[Gender] = mapped_column(SQLEnum(Gender, name="gender"))
    dob: Mapped[date]
    role: Mapped[UserRole]  = mapped_column(SQLEnum(UserRole, name="user_role"))
    password_hash: Mapped[str]
    joined_at: Mapped[datetime]  = mapped_column(default=datetime.utcnow)