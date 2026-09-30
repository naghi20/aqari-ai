import json
from types import SimpleNamespace

from aqari_ai.handlers.health import lambda_handler


def test_health_handler_returns_success(monkeypatch) -> None:
    monkeypatch.setenv("AQARI_ENVIRONMENT", "development")

    context = SimpleNamespace(aws_request_id="test-request-id")

    response = lambda_handler(event={}, context=context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert response_body["service"] == "aqari-ai"
    assert response_body["status"] == "healthy"
    assert response_body["environment"] == "development"
    assert response_body["request_id"] == "test-request-id"
    assert "timestamp_utc" in response_body
