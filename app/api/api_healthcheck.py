from fastapi import APIRouter

router = APIRouter()


@router.get("/check")
async def check():
    return {
        "code": "000",
        "message": "Health check: Success"
    }
