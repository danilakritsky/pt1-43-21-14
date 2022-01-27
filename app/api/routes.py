"""This module contains the app's routes."""

from fastapi import APIRouter, HTTPException, status, Path, Body
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from app.models import NoteResponseModel, NoteRequestModel, NoteCreateRequestModel
from . import crud
from typing import List

router = APIRouter()


@router.get("/", status_code=200, tags=["greeting"])
async def root() -> dict:
    """Get root."""
    return {"message": "Welcome:)"}


@router.post(
    "/",
    response_description="Create new note",
    response_model=NoteResponseModel,
    tags=["notes"],
)
# all pydantic models are recognized as request body parameters
async def create_note(note: NoteCreateRequestModel) -> dict:
    """Create new note."""
    note = jsonable_encoder(note)  # convert to a json-compatible data type
    new_note = await crud.create(note)
    if new_note:
        return new_note
