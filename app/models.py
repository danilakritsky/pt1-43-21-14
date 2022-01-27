"""This module contains pydantic models used for validating responses and requests."""

from typing import Optional, Generator
from bson.objectid import ObjectId
from pydantic import BaseModel, Field

# pylint: disable='R0903'


class MongoDBObjectId(ObjectId):
    """Custom data type used represent and validate an id of a note, so that
    it corresponds to the MongoDB's ObjectId.
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Get the function to be used for validation."""
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate the note's OjbectID."""
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Modify the return field schema."""
        field_schema.update(type="string")


class NoteResponseModel(BaseModel):
    """Model used to validate a note object in requests and responses."""

    id: MongoDBObjectId = Field(  # adds the separate validator for this field
        default_factory=MongoDBObjectId,  # called to provide the default value for the field
        alias="_id",
    )  # give an alias to our id, so that it corresponds to the MongoDB's _id field
    title: str = Field(...)
    body: str = Field(...)

    class Config:
        """Configures behavior of the model."""

        # allows NoteModel to recognize an alias ("_id") in requests and resonses
        # and validate it against the the "id" field's type
        allow_population_by_field_name = True
        # allows using our arbitrary MongoBDObjectID class for validation
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # serialize ObjectId to str
        schema_extra = {  # add example to the schema
            "example": {
                "_id": "61f197e7d0b033f65675a5a1",
                "title": "My First Note",
                "body": "Hello, World!",
            }
        }


class NoteRequestModel(BaseModel):
    """Model used to validate a note object in PUT requests."""

    title: Optional[str] = None  # optional values
    body: Optional[str] = None

    class Config:
        """Configures behavior of the model."""

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "My First Note",
                "body": "Hello, World!",
            }
        }


class NoteCreateRequestModel(BaseModel):
    """Model used to validate a note object in PUT requests."""

    title: str
    body: str

    class Config:
        """Configures behavior of the model."""

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "My First Note",
                "body": "Hello, World!",
            }
        }
