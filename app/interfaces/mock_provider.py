from app.interfaces.VerificationInterface import NINVerificationAdapterInterface, VerificationResult


class MockVerificationProvider(NINVerificationAdapterInterface):
    async def verify_nin(self, nin: str) -> VerificationResult:
        if len(nin) == 11 and nin.isdigit():
            return VerificationResult(
                is_valid=True,
                full_name="Mock User",
                msg="NIN verified successfully"
            )
        return VerificationResult(
            is_valid=False,
            msg="Invalid NIN format"
        )

    async def verify_bvn(self, bvn: str) -> VerificationResult:
        if len(bvn) == 11 and bvn.isdigit():
            return VerificationResult(
                is_valid=True,
                full_name="Mock User",
                msg="BVN verified successfully"
            )
        return VerificationResult(
            is_valid=False,
            msg="Invalid BVN format"
        )
