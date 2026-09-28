from pydantic import BaseModel
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

class BulkUploadApplicationsResponse(BaseModel):
    status: duoStatus


    