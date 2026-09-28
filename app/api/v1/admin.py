import csv
import io
from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException

from app.db.session import get_db
from app.schemas.admin import SetApplicationsStatusRequest, SetApplicationsStatusResponse, BulkUploadApplicationsResponse
from app.schemas.application import ApplicationData
from app.schemas.user import AuthenticateUserRequest
from app.schemas.common import UserNotification
from app.services.auth import AuthService
from app.services.application import ApplicationService
from app.repositories.user import UserRepository

router = APIRouter(prefix="/admin")


@router.post("/login")
def admin_login(data: AuthenticateUserRequest, db=Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(
        email=data.email,
        phone_number=data.phone_number,
        password=data.password
    )
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    access_token = service.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/applications", response_model=list[ApplicationData])
def view_applications(db=Depends(get_db)):
    service = ApplicationService(db)
    applications = service.get_applications()
    return [
        ApplicationData(
            business_name=app.business_name,
            business_address=app.business_address,
            tin_number=""
        )
        for app in applications
    ]


@router.patch("/applications/{application_id}/status", response_model=SetApplicationsStatusResponse)
def set_application_status(
    application_id: int,
    data: SetApplicationsStatusRequest,
    db=Depends(get_db)
):
    service = ApplicationService(db)
    application = service.set_application_status(application_id, data.set_status)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return SetApplicationsStatusResponse(status="successful")


@router.post("/bulk", response_model=BulkUploadApplicationsResponse)
async def bulk_upload(files: List[UploadFile], db=Depends(get_db)):
    results = {"successful": 0, "failed": 0, "duplicates": 0, "errors": []}
    app_service = ApplicationService(db)
    user_repo = UserRepository(db)

    for file in files:
        content = await file.read()
        try:
            reader = csv.DictReader(io.StringIO(content.decode()))
            for row in reader:
                email = row.get("email", "")
                if email and user_repo.get_by_email(email):
                    results["duplicates"] += 1
                    continue

                try:
                    app_service.submit_application(
                        user_id=int(row.get("user_id", 0)),
                        business_name=row.get("business_name", ""),
                        business_address=row.get("business_address", ""),
                        tin_number=row.get("tin_number", "")
                    )
                    results["successful"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append(f"{file.filename}: {str(e)}")
        except Exception as e:
            results["errors"].append(f"{file.filename}: {str(e)}")

    return BulkUploadApplicationsResponse(status="successful")


@router.post("/notification/{application_id}")
def send_user_notification(application_id: int, payload: UserNotification):
    return {"status": "sent", "application_id": application_id}
