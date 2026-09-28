from fastapi import APIRouter, UploadFile

from app.schemas.application import ApplicationData


router = APIRouter(prefix="/applications")

@router.post("/{application_id}/upload-nin")
def upload_nin(application_id:int, file: UploadFile):
    ...

@router.post("/{application_id}/submit")
def submit_application(application_id:int, data: ApplicationData):
    ...

@router.patch("/{application_id}/update")
def update_application(application_id:int, data: ApplicationData):
    ...