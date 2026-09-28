from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.membership import MembershipService

router = APIRouter(prefix="/membership")


@router.get("/status")
def get_membership_status(user_id: int, db: Session = Depends(get_db)):
    service = MembershipService(db)
    return service.get_status(user_id)
