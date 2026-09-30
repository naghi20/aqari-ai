# AQARI AI Property Draft Lambda Deployment Verification

**Date:** 2026-09-30
**Environment:** development
**AWS Region:** eu-central-1
**Verification status:** successful

## Purpose

This document records the successful deployment and end-to-end verification of the AQARI AI property-draft Lambda workflow.

The deployment validates this flow:

```text
Synthetic Joomla-style property event
→ AWS Lambda
→ Pydantic property validation
→ Joomla checkbox normalization
→ private-field filtering
→ DynamoDB property-draft write
→ CloudWatch Logs verification
```

## Deployed Lambda

| Setting | Verified value |
|---|---|
| Function name | `aqari-ai-create-property-dev` |
| Runtime | Python 3.12 |
| Architecture | ARM64 |
| Handler | `aqari_ai.handlers.create_property.lambda_handler` |
| Memory | 256 MB |
| Timeout | 15 seconds |
| Environment | development |
| DynamoDB table | `aqari-ai-properties-dev` |
| Log group | `/aws/lambda/aqari-ai-create-property-dev` |

## Deployment package verification

The property Lambda deployment package was built locally from CI-validated source code.

| Package property | Verification result |
|---|---|
| ZIP artifact | `aqari-ai-create-property-dev.zip` |
| Package size | Approximately 2.4 MB |
| Source files included | `create_property.py`, `property.py`, `validation_service.py` |
| Python runtime target | Python 3.12 |
| Lambda architecture target | ARM64 |
| Pydantic native binary | Verified as ARM aarch64 |
| Generated artifacts tracked by Git | No |

## CI verification

The project validation workflow completed successfully after the Joomla amenity and privacy feature was formatted with Ruff.

```text
Workflow: AQARI AI Backend Validation
Branch: main
Result: success
```

The validation pipeline includes:

```text
ruff check backend
ruff format --check backend
pytest
```

Local verification result:

```text
11 passed
```

## IAM least-privilege verification

The property-draft Lambda uses a dedicated execution role.

| Service | Allowed actions | Scope |
|---|---|---|
| CloudWatch Logs | `logs:CreateLogStream`, `logs:PutLogEvents` | Dedicated property Lambda log group |
| DynamoDB | `dynamodb:PutItem` | `aqari-ai-properties-dev` table only |

The property-draft role does not include:

```text
dynamodb:GetItem
dynamodb:Scan
dynamodb:UpdateItem
dynamodb:DeleteItem
s3:*
bedrock:*
cognito:*
secretsmanager:*
iam:*
```

## Invocation verification

A synthetic Joomla-style property payload was invoked successfully.

The Lambda application response confirmed:

```text
listing_status: draft
generation_status: not_requested
export_status: not_requested
```

A DynamoDB property-draft item was created successfully.

## Privacy verification

The deployed Lambda was verified to exclude private fields from both stored public-facing property data and the verified AI context.

The following fields were confirmed absent:

```text
internal_notes
internal_details
landlord
watchman
full_address
```

This ensures future AI listing generation can use verified property facts and checkbox amenities without automatically receiving sensitive operational details.

## CloudWatch Logs verification

CloudWatch Logs confirmed a successful property-draft creation event.

```text
START RequestId: <redacted>

Property draft created

END RequestId: <redacted>

REPORT RequestId: <redacted>
```

The Lambda `REPORT` entry confirmed the deployed ARM64 function completed execution and emitted standard runtime duration and memory telemetry.

## Joomla amenity verification

The deployed property schema supports these normalized Joomla checkbox amenities:

```text
parking
garden
basement
private_pool
common_pool
gym
sauna
steam
balcony
internet
lift
storage
laundry_room
driver_room
maid_room
central_ac
split_ac
window_ac
security
```

Unchecked amenity checkboxes default to `false`.

The legacy top-level `parking` field remains supported for compatibility and synchronizes with `features.parking`. Conflicting values are rejected during validation.

## Result

The AQARI AI property-draft serverless milestone is complete.

```text
CI-validated source code
→ ARM64 Lambda package
→ dedicated IAM execution role
→ deployed Python 3.12 Lambda
→ property validation
→ Joomla amenity normalization
→ privacy filtering
→ DynamoDB property draft
→ CloudWatch operational evidence
```

## Next phase

The next development phase is controlled AI listing-description generation.

The future generator must consume only `verified_ai_context`, not raw Joomla payloads or private operational details.

Planned next controls include:

- Versioned AI prompt templates.
- Arabic and English listing-generation evaluation cases.
- Prohibited-claim and factual-consistency checks.
- Human review and approval status before export.
- CloudWatch metrics, alarms, and dashboard coverage.
- Infrastructure as Code for repeatable environment creation.
