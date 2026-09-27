from pydantic import BaseModel
from typing import Literal, List

from app.schemas.application import ApplicationData

type duoStatus = Literal["successful", "failed"]

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

class BulkUploadApplicationsResponse(BaseModel):
    status: duoStatus


    