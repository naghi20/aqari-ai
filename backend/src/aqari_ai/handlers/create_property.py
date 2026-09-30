import json
import logging
import os
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from botocore.exceptions import ClientError
from pydantic import ValidationError

from aqari_ai.models.property import ListingStatus, PropertyDraftCreate
from aqari_ai.services.dynamodb_service import get_properties_table, put_property_draft
from aqari_ai.services.validation_service import build_verified_property_context

LOGGER = logging.getLogger()
LOGGER.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def _json_default(value: Any) -> str:
    """Serialize Decimal and datetime values for API-style JSON responses."""

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    raise TypeError(f"Type {type(value).__name__} is not JSON serializable")


def _response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    """Create a consistent JSON HTTP-style Lambda response."""

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=_json_default),
    }


def lambda_handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    """Validate a synthetic property record and create a DynamoDB draft item."""

    request_id = getattr(context, "aws_request_id", "local-development")

    try:
        property_payload = event.get("property", event)
        property_draft = PropertyDraftCreate.model_validate(property_payload)
    except ValidationError as error:
        LOGGER.warning("Property draft validation failed", extra={"request_id": request_id})

        return _response(
            400,
            {
                "message": "Invalid property draft payload",
                "errors": json.loads(error.json()),
                "request_id": request_id,
            },
        )

    property_id = f"PROP-{uuid4()}"
    created_at = datetime.now(UTC).isoformat()

    property_data = property_draft.model_dump(mode="python")
    property_data.pop("internal_notes", None)

    item = {
        "property_id": property_id,
        "entity_type": "property_draft",
        "listing_status": ListingStatus.DRAFT.value,
        "created_at": created_at,
        "updated_at": created_at,
        "request_id": request_id,
        "property_data": property_data,
        "verified_ai_context": build_verified_property_context(property_draft),
        "generation_status": "not_requested",
        "export_status": "not_requested",
    }

    try:
        table = get_properties_table()
        put_property_draft(table, item)
    except ClientError:
        LOGGER.exception(
            "DynamoDB property draft write failed",
            extra={
                "request_id": request_id,
                "property_id": property_id,
            },
        )

        return _response(
            500,
            {
                "message": "Unable to create property draft",
                "request_id": request_id,
            },
        )

    LOGGER.info(
        "Property draft created",
        extra={
            "request_id": request_id,
            "property_id": property_id,
        },
    )

    return _response(
        201,
        {
            "message": "Property draft created",
            "property_id": property_id,
            "listing_status": ListingStatus.DRAFT.value,
            "generation_status": "not_requested",
            "export_status": "not_requested",
            "request_id": request_id,
            "created_at": created_at,
        },
    )
