"""This module contains the app's routes."""

from fastapi import APIRouter, HTTPException, status, Path, Body
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from app.models import NoteResponseModel, NoteRequestModel, NoteCreateRequestModel
from . import crud
from typing import List

router = APIRouter()

class NoteNotFoundException(HTTPException):
    """Exception to be raised when no note with the given id is found."""

    def __init__(self, note_id: str):
        """Initialize the instance."""
        super().__init__(404)
        self.note_id = note_id
        self.status_code = 404
        self.detail = f"Note {note_id!r} not found"


@router.get("/", status_code=200, tags=["greeting"])
async def root() -> dict:
    """Get root."""
    return {"message": "Welcome:)"}


@router.post(
    "/notes",
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


@router.get(
    "/notes",
    response_description="Get all notes",
    response_model=List[NoteResponseModel],
    tags=["notes"],
)
async def get_all_notes() -> dict:
    """Get all notes."""
    notes = await crud.read_all()
    return notes


@router.get(
    "/notes/{note_id}",
    response_description="Get note",
    response_model=NoteResponseModel,
    tags=["notes"],
)
# all parameters that come from route handler decorators are recognized
# as the request path parameters and we can we add a Path validator to them on the spot
async def get_note(note_id: str = Path(..., title="The id of the note to get")) -> dict:
    """Get a note by its id."""
    if (note := await crud.read(note_id)) is not None:
        return note
    raise NoteNotFoundException(note_id)


@router.put(
    "/notes/{note_id}",
    response_description="Update note",
    response_model=NoteResponseModel,
    tags=["notes"],
)
async def update_note(
    # even though our Body parameter precedes our Path parameter, the order is resolved by FastAPI
    note_data: NoteRequestModel,
    note_id: str = Path(..., title="The id of the note to update"),
) -> dict:
    """Update a note."""
    note = await crud.update(note_id, note_data)
    if note:
        return note
    raise NoteNotFoundException(note_id)


@router.delete("/notes/{note_id}", response_description="Delete note", tags=["notes"])
async def delete_note(
    note_id: str = Path(..., title="The id of the note to delete")
) -> JSONResponse:
    """Delete a note."""
    if (
        delete_result := await crud.delete(note_id)
    ) and delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise NoteNotFoundException(note_id)
