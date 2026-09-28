from sqlalchemy.orm import Session

from app.models.application import Application, Status
from app.repositories.application import ApplicationRepository


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)

    def submit_application(self, user_id: int, business_name: str, business_address: str, tin_number: str) -> Application:
        application = Application(
            user_id=user_id,
            application_status=Status.PENDING,
            business_name=business_name,
            business_address=business_address
        )
        return self.app_repo.create(application)

    def update_application(self, application_id: int, business_name: str, business_address: str) -> Application | None:
        application = self.app_repo.get_by_id(application_id)
        if not application:
            return None
        application.business_name = business_name
        application.business_address = business_address
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_applications(self) -> list[Application]:
        return self.app_repo.get_all()

    def set_application_status(self, application_id: int, status: str) -> Application | None:
        application = self.app_repo.get_by_id(application_id)
        if not application:
            return None
        application.application_status = Status(status)
        self.db.commit()
        self.db.refresh(application)
        return application
