import hashlib
import hmac
import os

from sqlalchemy.orm import Session

from app.interfaces.VerificationInterface import NINVerificationAdapterInterface, VerificationResult
from app.models.userIdentity import UserIdentity, Creds
from app.repositories.user_identity import UserIdentityRepository


class IdentityVerificationService:
    def __init__(self, nin_adapter: NINVerificationAdapterInterface, db: Session):
        self.nin_adapter = nin_adapter
        self.db = db
        self.identity_repo = UserIdentityRepository(db)

    async def verify_identity(self, user_id: int, cred_type: str, cred_value: str) -> dict:
        clean_value = cred_value.strip()

        if self.identity_repo.get_by_user_id(user_id):
            return {"status": "failed", "reason": "Identity already verified"}

        if cred_type == "nin":
            result: VerificationResult = await self.nin_adapter.verify_nin(clean_value)
        elif cred_type == "bvn":
            result: VerificationResult = await self.nin_adapter.verify_bvn(clean_value)
        else:
            return {"status": "failed", "reason": "Invalid credential type"}

        if not result.is_valid:
            return {"status": "failed", "reason": result.msg or "Invalid identification credentials"}

        secret = os.getenv("HMAC_SECRET", "default-secret-key")
        hmac_value = hmac.new(
            secret.encode(),
            clean_value.encode(),
            hashlib.sha256
        ).hexdigest()

        identity = UserIdentity(
            user_id=user_id,
            cred=Creds(cred_type),
            hmac_value=hmac_value
        )
        self.identity_repo.create(identity)

        return {"status": "success", "message": "Identity verified successfully"}
