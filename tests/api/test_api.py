"""Test alpaca-partner-backend REST API."""

import httpx
from alpaca_partner_backend.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_docs() -> None:
    """Test that reading the root is successful."""
    response = client.get("/")
    assert httpx.codes.is_success(response.status_code)
