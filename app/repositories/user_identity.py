from sqlalchemy.orm import Session
from app.models.userIdentity import UserIdentity


class UserIdentityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> UserIdentity | None:
        return self.db.query(UserIdentity).filter(UserIdentity.user_id == user_id).first()

    def create(self, identity: UserIdentity) -> UserIdentity:
        self.db.add(identity)
        self.db.commit()
        self.db.refresh(identity)
        return identity
