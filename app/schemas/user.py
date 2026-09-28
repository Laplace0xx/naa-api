from datetime import date

from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    f_name: str
    l_name: str
    gender: str
    email: EmailStr
    phone_number: int
    dob: date
    role: str

class RegisterUserResponse(BaseModel):
    status: str
    payload: str

class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    phone_number: int
    password_hash: str

class AuthenticateUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    
