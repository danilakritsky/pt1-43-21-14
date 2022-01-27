"""This module contains the app's routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", status_code=200, tags=["greeting"])
async def root() -> dict:
    """Get root."""
    return {"message": "Welcome:)"}
