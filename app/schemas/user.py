from datetime import date
from typing import Self

from pydantic import BaseModel, EmailStr, model_validator

class RegisterUserRequest(BaseModel):
    f_name: str
    l_name: str
    gender: str
    email: EmailStr
    phone_number: str
    dob: date
    password: str

class RegisterUserResponse(BaseModel):
    status: str

class AuthenticateUserRequest(BaseModel):
    email: EmailStr | None=None
    phone_number: str | None=None
    password: str

    @model_validator(mode='after')
    def check_email_or_phone_number(self) -> Self:
        if not self.email and not self.phone_number:
            raise ValueError("You must provide either email or phone number")

        if self.email and self.phone_number:
            raise ValueError("Provide only one of email or phone number")
        return self

class AuthenticateUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    
