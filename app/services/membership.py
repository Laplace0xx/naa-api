from sqlalchemy.orm import Session

from app.models.membership import Membership, MembershipStatus
from app.repositories.membership import MembershipRepository


class MembershipService:
    def __init__(self, db: Session):
        self.db = db
        self.membership_repo = MembershipRepository(db)

    def get_status(self, user_id: int) -> dict:
        membership = self.membership_repo.get_by_user_id(user_id)
        if not membership:
            return {"status": "not_found", "membership_status": None}
        return {"status": "found", "membership_status": membership.membership_status.value}
