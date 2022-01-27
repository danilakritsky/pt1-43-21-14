"""This model contains CRUD operations against the database."""

from bson import ObjectId
from typing import List
from pymongo.results import DeleteResult

from app.db import db, MONGODB_COLLECTION

db.collection = db.get_collection(MONGODB_COLLECTION)


async def create(data: dict) -> dict:
    """Create new document in a collection and return it."""
    document = await db.collection.insert_one(data)
    created_document = await db.collection.find_one({"_id": document.inserted_id})
    return created_document
