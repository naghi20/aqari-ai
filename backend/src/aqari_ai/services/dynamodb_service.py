import os
from collections.abc import Mapping
from typing import Any

import boto3


def get_properties_table() -> Any:
    """Return the configured AQARI AI DynamoDB properties table."""

    table_name = os.getenv("AQARI_PROPERTIES_TABLE_NAME")

    if not table_name:
        raise RuntimeError("AQARI_PROPERTIES_TABLE_NAME environment variable is required")

    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)


def put_property_draft(
    table: Any,
    item: Mapping[str, Any],
) -> None:
    """Create a property draft only if its property ID does not already exist."""

    table.put_item(
        Item=dict(item),
        ConditionExpression="attribute_not_exists(property_id)",
    )
