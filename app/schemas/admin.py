from datetime import date

from pydantic import BaseModel, EmailStr
from typing import List

from app.schemas.application import ApplicationData
from app.schemas.common import duoStatus

class ViewApplicationsRequest(BaseModel):
    data: List[ApplicationData]

class ViewApplicationsResponse(BaseModel):
    status: duoStatus

class SetApplicationsStatusRequest(BaseModel):
    set_status: duoStatus

class SetApplicationsStatusResponse(BaseModel):
    status: duoStatus

class BulkUploadApplicationsRequest(BaseModel):
    data: List[ApplicationData]

class BulkOnboardRow(BaseModel):
    f_name: str
    l_name: str
    gender: str
    email: EmailStr
    phone_number: str
    dob: date
    password: str
    business_name: str
    business_address: str
    tin_number: str

class BulkRowError(BaseModel):
    row: int
    file: str
    reason: str

class BulkUploadApplicationsResponse(BaseModel):
    status: duoStatus
    successful: int = 0
    failed: int = 0
    duplicates: int = 0
    errors: List[BulkRowError] = []


    