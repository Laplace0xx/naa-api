from pydantic import BaseModel
from typing import Literal

type duoStatus = Literal["successful", "failed"]
type triStatus = Literal["successful", "pending", "failed"]


class UserNotification(BaseModel):
    msg: int

