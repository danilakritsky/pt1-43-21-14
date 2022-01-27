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
        "/notes", data=json.dumps(test_request_body)
    )  # jsonifies the body
    print(response.json())  # jsonifies response
    assert response.status_code == 200
    assert response.json() == test_response_body


def test_create_note_invalid(test_client, monkeypatch):
    response = test_client.post("/notes", data=json.dumps({"title": 1}))
    assert response.status_code == 422


def test_read_note(test_client, test_note_id, monkeypatch):
    test_data = {
        "_id": test_note_id,
        "title": "Note to be read.",
        "body": "Read!",
    }

    async def mock_read(id):
        return test_data

    monkeypatch.setattr(crud, "read", mock_read)

    response = test_client.get(f"/notes/{test_note_id}")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_invalid_id(test_client, monkeypatch):
    async def mock_read(id):
        return None

    monkeypatch.setattr(crud, "read", mock_read)

    response = test_client.get("/notes/42")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note '42' not found"


def test_read_all_notes(test_client, test_note_id, monkeypatch):
    test_data = [
        {
            "_id": test_note_id,
            "title": "something",
            "body": "something else",
        },
        {
            "_id": test_note_id.replace("1", "2"),
            "title": "someone",
            "body": "someone else",
        },
    ]

    async def mock_read_all():
        return test_data

    monkeypatch.setattr(crud, "read_all", mock_read_all)

    response = test_client.get("/notes")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_client, test_note_id, monkeypatch):
    test_update_data = {"title": "Set this new title", "body": "Set this new body"}

    async def mock_update(id, new_data):
        return {**{"_id": test_note_id}, **test_update_data}

    monkeypatch.setattr(crud, "update", mock_update)

    response = test_client.put(f"/notes/{test_note_id}", data=json.dumps(test_update_data))
    # TODO
    assert response.status_code == 200
    assert response.json() == {**{"_id": test_note_id}, **test_update_data}


@pytest.mark.parametrize(
    "id, new_data",
    [
        ["0", {}],
        ["1", {"title": "Set this title"}],
        ["2", {"title": "Set this title", "body": "Set this body"}],
    ],
)
def test_update_note_indalid_id(test_client, monkeypatch, id, new_data):
    async def mock_update(id, new_data):
        return None

    monkeypatch.setattr(crud, "update", mock_update)

    response = test_client.put(f"/notes/{id}", data=json.dumps(new_data))
    assert response.status_code == 404


def test_delete_note(test_client, monkeypatch, test_note_id):
    # create a mock DeleteResult object
    mock_resp = mock.MagicMock()
    mock_resp.__bool__.return_value = True
    mock_resp.deleted_count = 1

    async def mock_delete(id):
        return mock_resp

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_client.delete(f"/notes/{test_note_id}")
    assert response.status_code == 204


def test_delete_note_invalid_id(test_client, monkeypatch, test_note_id):
    async def mock_delete(id):
        return False

    response = test_client.delete(f"/notes/{test_note_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Note {test_note_id!r} not found"
