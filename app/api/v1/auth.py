from fastapi import APIRouter
from app.schemas.user import RegisterUserRequest, AuthenticateUserRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/create-account")
def create_account(data: RegisterUserRequest):
    ...

@router.post("/login")
def login(data: AuthenticateUserRequest):
    ...

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    ...