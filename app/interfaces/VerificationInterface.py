from pydantic import BaseModel
from abc import ABC, abstractmethod

class VerificationResult(BaseModel):
    is_valid: bool
    full_name: str | None=None
    msg: str | None=None

class NINVerificationAdapterInterface(ABC):
    @abstractmethod
    async def verify_nin(self, nin: str) -> VerificationResult:
        ...

    @abstractmethod
    async def verify_bvn(self, bvn: str) -> VerificationResult:
        ...
