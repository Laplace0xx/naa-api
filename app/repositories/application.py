from sqlalchemy.orm import Session
from app.models.application import Application


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, application_id: int) -> Application | None:
        return self.db.query(Application).filter(Application.id == application_id).first()

    def get_all(self) -> list[Application]:
        return self.db.query(Application).all()

    def create(self, application: Application) -> Application:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application
