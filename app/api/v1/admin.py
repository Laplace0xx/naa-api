from typing import List

from fastapi import APIRouter, UploadFile

from app.schemas.admin import SetApplicationsStatusRequest
from app.schemas.application import ApplicationData
from app.schemas.user import AuthenticateUserRequest
from app.schemas.common import UserNotification

router = APIRouter(prefix="/admin")

@router.post("/login")
def admin_login(data: AuthenticateUserRequest):
    ...

@router.get("/applications", response_model=list[ApplicationData])
def view_applications():
    ...

@router.patch("/applications/{application_id}/status")
def set_application_status(application_id:int, data:SetApplicationsStatusRequest):
    ...

@router.post("/bulk")
def bulk_upload(files: List[UploadFile]):
    ...

@router.post("/notification/{application_id}")
def send_user_notification(application_id:int, payload:UserNotification):
    ...

