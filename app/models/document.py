from datetime import date

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id:Mapped[str] = mapped_column(primary_key=True)
    user_id:Mapped[str] = mapped_column(ForeignKey("users.id"))
    storage_id:Mapped[str] = mapped_column(String(25))
    type:Mapped[str] = mapped_column(Enum("NIN"))
    submitted_at: Mapped[date]