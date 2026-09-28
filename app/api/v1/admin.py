import csv
import io
import json
from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from pydantic import ValidationError

from app.db.session import get_db
from app.schemas.admin import SetApplicationsStatusRequest, SetApplicationsStatusResponse, BulkUploadApplicationsResponse, BulkOnboardRow, BulkRowError
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


def parse_bulk_file(filename: str, content: bytes) -> list[dict]:
    text = content.decode("utf-8-sig")
    if filename.lower().endswith(".json"):
        data = json.loads(text)
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        if not isinstance(data, list):
            raise ValueError("JSON body must be a list of rows or an object with a 'data' list")
        return data
    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]


@router.post("/bulk", response_model=BulkUploadApplicationsResponse)
async def bulk_upload(files: List[UploadFile], db=Depends(get_db)):
    auth_service = AuthService(db)
    app_service = ApplicationService(db)
    user_repo = UserRepository(db)
    seen_emails: set[str] = set()
    seen_phones: set[str] = set()
    successful = 0
    failed = 0
    duplicates = 0
    errors: list[BulkRowError] = []

    for file in files:
        try:
            rows = parse_bulk_file(file.filename or "", await file.read())
        except Exception as e:
            errors.append(BulkRowError(row=0, file=file.filename or "", reason=str(e)))
            failed += 1
            continue

        for index, raw in enumerate(rows, start=1):
            try:
                row = BulkOnboardRow.model_validate(raw)
            except ValidationError as e:
                failed += 1
                errors.append(BulkRowError(row=index, file=file.filename or "", reason=str(e.errors()[0]["msg"])))
                continue

            email = str(row.email).lower()
            phone = row.phone_number
            if email in seen_emails or phone in seen_phones:
                duplicates += 1
                continue
            if user_repo.get_by_email(email) or user_repo.get_by_phone(phone):
                seen_emails.add(email)
                seen_phones.add(phone)
                duplicates += 1
                continue

            try:
                user = auth_service.create_account(
                    f_name=row.f_name,
                    l_name=row.l_name,
                    gender=row.gender,
                    email=email,
                    phone_number=phone,
                    dob=str(row.dob),
                    password=row.password
                )
                app_service.submit_application(
                    user_id=user.id,
                    business_name=row.business_name,
                    business_address=row.business_address,
                    tin_number=row.tin_number
                )
                seen_emails.add(email)
                seen_phones.add(phone)
                successful += 1
            except ValueError as e:
                duplicates += 1
            except Exception as e:
                failed += 1
                errors.append(BulkRowError(row=index, file=file.filename or "", reason=str(e)))

    return BulkUploadApplicationsResponse(
        status="successful",
        successful=successful,
        failed=failed,
        duplicates=duplicates,
        errors=errors
    )


@router.post("/notification/{application_id}")
def send_user_notification(application_id: int, payload: UserNotification):
    return {"status": "sent", "application_id": application_id}
