"""This module provide a connection to the test database."""

import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


try:
    MONGODB_URI = os.environ["MONGODB_URI"]
except KeyError:
    MONGODB_URI = "mongodb://test:test@db:27017/?authSource=test"

try:
    MONGODB_DATABASE = os.environ["MONGODB_COLLECTION"]

except KeyError:
    MONGODB_DATABASE = "test"

try:
    MONGODB_COLLECTION = os.environ["MONGODB_DATABASE"]
except KeyError:
    MONGODB_COLLECTION = "test"

mongo_client = AsyncIOMotorClient(MONGODB_URI)
mongo_client.get_io_loop = asyncio.get_running_loop

db = mongo_client[MONGODB_DATABASE]
