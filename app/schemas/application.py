from typing import List, Literal

from pydantic import BaseModel
from pydantic.networks import HttpUrl

from app.schemas.admin import duoStatus

type triStatus = Literal["successful", "pending", "failed"]

class ApplicationData(BaseModel):
    business_name: str
    business_address: str
    tin_number: str

class UploadDocumentRequest(BaseModel):
    type: str = "NIN"
    file_name: str
    file_url: HttpUrl

class UploadDocumentResponse(BaseModel):
    status: duoStatus

class SubmitApplicationRequest(BaseModel):
    application: ApplicationData

class SubmitApplicationResponse(BaseModel):
    status: triStatus

class UpdateApplicationsRequest(BaseModel):
    business_name: str
    business_address: str

class UpdateApplicationsResponse(BaseModel):
    status: List[duoStatus]


