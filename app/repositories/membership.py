from sqlalchemy.orm import Session
from app.models.membership import Membership


class MembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Membership | None:
        return self.db.query(Membership).filter(Membership.user_id == user_id).first()
