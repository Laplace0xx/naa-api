from pydantic import BaseModel
from typing import Literal

class CheckMembership(BaseModel):
    status: Literal["active", "inactive", "expired", "pending"]

    