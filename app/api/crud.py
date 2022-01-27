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


async def read_all() -> List[dict]:
    """Get a list of documents in a collection."""
    documents = []
    async for document in db.collection.find():
        documents.append(document)
    return documents


async def read(document_id: str) -> dict:
    """Get a single document by its id."""
    document = await db.collection.find_one({"_id": ObjectId(document_id)})
    if document:
        return document


async def update(document_id: str, update_data: dict) -> dict:
    """Update document with new data."""
    # don't update fields with empty values
    new_data = {
        key: val for key, val in update_data.__dict__.items() if val is not None
    }
    document_to_update = await db.collection.find_one({"_id": ObjectId(document_id)})
    if new_data and document_to_update is not None:
        update_result = await db.collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": new_data}
        )
        if update_result.modified_count == 1:
            # get updated note
            return await db.collection.find_one({"_id": ObjectId(document_id)})
    # return the existing document if no update data has been given
    return document_to_update


async def delete(document_id: str) -> DeleteResult:
    """Delete note."""
    document = await db.collection.find_one({"_id": ObjectId(document_id)})
    if document:
        delete_result = await db.collection.delete_one({"_id": ObjectId(document_id)})
        return delete_result
