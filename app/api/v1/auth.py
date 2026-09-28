from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import (
    RegisterUserRequest, AuthenticateUserRequest, ResetPasswordRequest,
    RegisterUserResponse, AuthenticateUserResponse
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/create-account", response_model=RegisterUserResponse)
def create_account(data: RegisterUserRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        service.create_account(
            f_name=data.f_name,
            l_name=data.l_name,
            gender=data.gender,
            email=data.email,
            phone_number=data.phone_number,
            dob=str(data.dob),
            password=data.password
        )
        return RegisterUserResponse(status="success")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=AuthenticateUserResponse)
def login(data: AuthenticateUserRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(
        email=data.email,
        phone_number=data.phone_number,
        password=data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = service.create_access_token(user)
    return AuthenticateUserResponse(access_token=access_token)


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    success = service.reset_password(data.email, data.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}
