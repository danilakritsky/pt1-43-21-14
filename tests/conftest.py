"""This module contains fixtures to be used for testing."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client(scope="module"):  # pylint: disable="W0613"
    """Yield the test client to be used in all tests."""
    client = TestClient(app)
    yield client


@pytest.fixture
def test_note_id(scope="module"):  # pylint: disable="W0613"
    return "61f19e1ab8b744785180cdd1"
