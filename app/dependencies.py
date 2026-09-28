from fastapi import Depends

from app.interfaces.mock_provider import MockVerificationProvider
from app.services.verification import IdentityVerificationService
from app.db.session import get_db


def get_verification_service(db=Depends(get_db)) -> IdentityVerificationService:
    provider = MockVerificationProvider()
    return IdentityVerificationService(nin_adapter=provider, db=db)
