# AQARI AI Property Draft Handler

## Purpose

The property-draft handler creates a validated property draft in DynamoDB.

This is the first AQARI AI business workflow.

It does not:

- Invoke Amazon Bedrock
- Upload images to S3
- Publish to Joomla
- Publish to Facebook or Instagram
- Accept real customer data in public test files

## Lambda handler

```text
aqari_ai.handlers.create_property.lambda_handler
```

## Input format

```json
{
  "property": {
    "reference_code": "BH-JUF-TEST-001",
    "property_type": "apartment",
    "transaction_type": "rent",
    "location": "Juffair",
    "price_bhd": 550,
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqm": 120,
    "furnished": true,
    "parking": true,
    "verified_features": [
      "balcony",
      "gym access"
    ]
  }
}
```

## Validation rules

- `reference_code` must contain only letters, numbers, underscores, and hyphens.
- `price_bhd` must be greater than zero.
- Apartments and villas require bedrooms and bathrooms.
- Location names are normalized.
- Duplicate verified features are removed.
- Internal notes are excluded from the stored property draft.
- Only verified fields are added to `verified_ai_context`.

## Stored DynamoDB fields

```text
property_id
entity_type
listing_status
created_at
updated_at
request_id
property_data
verified_ai_context
generation_status
export_status
```

## Response codes

| Status code | Meaning |
|---:|---|
| `201` | Valid property draft created |
| `400` | Property payload failed validation |
| `500` | DynamoDB write failed |

## Required environment variable

```text
AQARI_PROPERTIES_TABLE_NAME=aqari-ai-properties-dev
```

## Next feature

After the DynamoDB write workflow is tested in AWS, AQARI AI can add a controlled Bedrock generation handler.
