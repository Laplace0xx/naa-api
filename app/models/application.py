from enum import Enum
from sqlalchemy import ForeignKey, Enum as SQLEnum, String

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(Base): 
    __tablename__ = "applications"
    
    id:Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id:Mapped[str] = mapped_column(ForeignKey("users.id"))
    application_status:Mapped[Status] = mapped_column(SQLEnum(Status, name="application_status"))
    business_name:Mapped[str] = mapped_column(String(30))
    business_address: Mapped[str] = mapped_column(String(30))
    
    