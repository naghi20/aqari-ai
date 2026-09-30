import json
import logging
import os
from datetime import UTC, datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def lambda_handler(event: dict, context: object) -> dict:
    """Return a minimal AQARI AI service health response."""

    request_id = getattr(context, "aws_request_id", "local-development")

    response_body = {
        "service": "aqari-ai",
        "status": "healthy",
        "environment": os.getenv("AQARI_ENVIRONMENT", "development"),
        "request_id": request_id,
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }

    LOGGER.info(
        "AQARI AI health check completed",
        extra={
            "request_id": request_id,
            "environment": response_body["environment"],
        },
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response_body),
    }
