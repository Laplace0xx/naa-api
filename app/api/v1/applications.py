from fastapi import APIRouter, Depends, HTTPException, Form

from app.db.session import get_db
from app.schemas.application import ApplicationData, SubmitApplicationRequest, SubmitApplicationResponse, UpdateApplicationsRequest, UpdateApplicationsResponse
from app.dependencies import get_verification_service
from app.services.verification import IdentityVerificationService
from app.services.application import ApplicationService

router = APIRouter(prefix="/applications")


@router.post("/{application_id}/upload-nin")
async def upload_nin(
    application_id: int,
    nin: str = Form(...),
    service: IdentityVerificationService = Depends(get_verification_service)
):
    result = await service.verify_identity(
        user_id=application_id,
        cred_type="nin",
        cred_value=nin
    )
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result["reason"])
    return result


@router.post("/{application_id}/submit", response_model=SubmitApplicationResponse)
def submit_application(
    application_id: int,
    data: SubmitApplicationRequest,
    db=Depends(get_db)
):
    service = ApplicationService(db)
    application = service.submit_application(
        user_id=application_id,
        business_name=data.application.business_name,
        business_address=data.application.business_address,
        tin_number=data.application.tin_number
    )
    return SubmitApplicationResponse(status="successful")


@router.patch("/{application_id}/update", response_model=UpdateApplicationsResponse)
def update_application(
    application_id: int,
    data: UpdateApplicationsRequest,
    db=Depends(get_db)
):
    service = ApplicationService(db)
    application = service.update_application(
        application_id=application_id,
        business_name=data.business_name,
        business_address=data.business_address
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return UpdateApplicationsResponse(status=["successful"])
