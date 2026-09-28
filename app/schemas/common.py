from pydantic import BaseModel

class UserNotification(BaseModel):
    msg: int