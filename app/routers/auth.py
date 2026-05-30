from fastapi import APIRouter

router = APIRouter()

@router.get("/github/callback")
async def github_callback(code: str):
    # Placeholder – implement GitHub OAuth as needed
    return {"access_token": "fake-token", "token_type": "bearer"}