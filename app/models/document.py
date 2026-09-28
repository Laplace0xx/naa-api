from datetime import date, datetime

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id:Mapped[int] = mapped_column(primary_key=True, nullable=False)
    application_id:Mapped[int] = mapped_column(ForeignKey("applications.id"))
    storage_id:Mapped[str] = mapped_column(String(25))
    type:Mapped[str] = mapped_column(SQLEnum("NIN", "BVN", name="document_type"))
    submitted_at: Mapped[date] = mapped_column(default=datetime.utcnow)