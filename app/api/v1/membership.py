from fastapi import APIRouter

router = APIRouter(prefix="/membership")

@router.get("/status")
def get_membership_status():
    ...