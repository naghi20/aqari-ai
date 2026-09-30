# AQARI AI Lambda Health Check

## Purpose

The AQARI AI health-check Lambda function verifies the serverless backend deployment path before application permissions are added.

The function does not access:

- Amazon S3
- Amazon DynamoDB
- Amazon Bedrock
- Amazon Cognito
- Joomla
- Meta APIs
- Secrets Manager

Its only AWS service interaction is writing operational logs to Amazon CloudWatch Logs.

## Function configuration

| Setting | Value |
|---|---|
| Function name | `aqari-ai-health-dev` |
| Runtime | `python3.12` |
| Handler | `aqari_ai.handlers.health.lambda_handler` |
| Architecture | `arm64` |
| Memory | `128 MB` |
| Timeout | `10 seconds` |
| Environment | `development` |
| Log group | `/aws/lambda/aqari-ai-health-dev` |
| Log retention | `14 days` |

## Expected response

```json
{
  "service": "aqari-ai",
  "status": "healthy",
  "environment": "development",
  "request_id": "AWS Lambda request ID",
  "timestamp_utc": "ISO-8601 UTC timestamp"
}
```

## Least-privilege role

The Lambda execution role initially has CloudWatch Logs permissions only.

It must not have access to:

- S3 buckets
- DynamoDB tables
- Bedrock models
- Cognito user pools
- Secrets Manager
- IAM management actions
- Public network configuration

Later implementation phases will add only the specific permissions needed by each feature.

## Local validation

```bash
source .venv/bin/activate
make validate
```

## Deployment validation

After deployment, invoke the function with an empty event:

```bash
aws lambda invoke \
  --function-name aqari-ai-health-dev \
  --region eu-central-1 \
  --payload '{}' \
  response.json

cat response.json
```

Expected:

```text
statusCode: 200
status: healthy
```
