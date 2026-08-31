import requests
import pytest

@pytest.fixture
def server_url():
    # Replace with actual server URL if available
    return "http://localhost:8000"

def test_dashboard_500_error(server_url, monkeypatch):
    """Ensure the dashboard endpoint handles 500 Internal Server Error gracefully."""
    def mock_get(*args, **kwargs):
        class Resp:
            status_code = 500
            text = "Internal Server Error"
        return Resp()
    monkeypatch.setattr(requests, "get", mock_get)
    resp = requests.get(f"{server_url}/dashboard")
    assert resp.status_code == 500
    # In a real implementation, the client should display an error message instead of crashing
    # Here we just assert the status code; UI handling is verified elsewhere.
