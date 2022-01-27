"""This modules contains tests for the api routes."""

import json
from pydantic import ValidationError

import pytest
import unittest.mock as mock

from app.api import crud
from bson.objectid import ObjectId


def test_create_note(test_client, test_note_id, monkeypatch):
    test_request_body = {"title": "New Note", "body": "Hello, World!"}
    test_response_body = {
        "_id": test_note_id,
        "title": "New Note",
        "body": "Hello, World!",
    }

    async def mock_create(data):
        return test_response_body

    monkeypatch.setattr(crud, "create", mock_create)

    response = test_client.post(
        "/", data=json.dumps(test_request_body)
    )  # jsonifies the body
    print(response.json())  # jsonifies response
    assert response.status_code == 200
    assert response.json() == test_response_body


def test_create_note_invalid(test_client, monkeypatch):
    response = test_client.post("/", data=json.dumps({"title": 1}))
    assert response.status_code == 422
