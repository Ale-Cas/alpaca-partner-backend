"""Test alpaca-broker REST API."""

import httpx
from fastapi.testclient import TestClient

from alpaca_broker.api.main import app

client = TestClient(app)


def test_read_docs() -> None:
    """Test that reading the root is successful."""
    response = client.get("/")
    assert httpx.codes.is_success(response.status_code)
