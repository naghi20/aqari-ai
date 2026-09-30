# AQARI AI Lambda Health Check Deployment Verification

## Purpose

This document records the successful deployment and verification of the first AQARI AI AWS Lambda function.

The health-check function verifies the serverless deployment path before AQARI AI receives access to property data, Amazon S3, DynamoDB, or Amazon Bedrock.

## Deployed function

| Setting | Value |
|---|---|
| Function name | `aqari-ai-health-dev` |
| AWS Region | `eu-central-1` |
| Runtime | `python3.12` |
| Handler | `aqari_ai.handlers.health.lambda_handler` |
| Architecture | `arm64` |
| Memory | `128 MB` |
| Timeout | `10 seconds` |
| Environment | `development` |
| Log level | `INFO` |
| Deployment state | `Active` |
| Last update status | `Successful` |

## CloudWatch Logs

| Setting | Value |
|---|---|
| Log group | `/aws/lambda/aqari-ai-health-dev` |
| Log retention | `14 days` |
| Initial stored log data | `0 bytes` before first invocation |

## IAM least-privilege role

| Setting | Value |
|---|---|
| Role name | `aqari-ai-lambda-execution-role-dev` |
| Trusted service | `lambda.amazonaws.com` |
| Inline policy | `AQARIHealthCloudWatchLogsWrite` |
| Allowed action | `logs:CreateLogStream` |
| Allowed action | `logs:PutLogEvents` |
| Allowed resource | AQARI health Lambda log streams only |

The health-check execution role does not have permissions for:

- Amazon S3
- Amazon DynamoDB
- Amazon Bedrock
- Amazon Cognito
- AWS Secrets Manager
- Joomla
- Meta APIs
- IAM administration

## Successful invocation

The function was invoked with this empty payload:

```json
{}
```

Verification result:

```text
StatusCode: 200
FunctionError: None
ExecutedVersion: $LATEST
```

The health response confirmed:

```json
{
  "service": "aqari-ai",
  "status": "healthy",
  "environment": "development"
}
```

## CloudWatch verification

The CloudWatch log stream confirmed:

```text
INIT_START
START RequestId
AQARI AI health check completed
END RequestId
REPORT RequestId
```

The initial invocation completed successfully with low memory usage and a short execution duration.

## Security controls verified

- Lambda code was validated locally before deployment.
- GitHub Actions CI passed before deployment.
- The deployment package contains only the minimal handler package.
- The Lambda role has CloudWatch log write permissions only.
- Logs use a 14-day retention period.
- No customer data, property photos, Joomla export, AWS key, GitHub token, or account-specific resource identifier is stored in this repository.

## Next feature

The next AQARI AI feature is a validated property-draft handler.

It will:

1. Accept synthetic property input.
2. Validate it with the existing Pydantic property model.
3. Create a `property_id`.
4. Write a draft item to `aqari-ai-properties-dev`.
5. Return the stored record metadata.
6. Add only the required DynamoDB permissions to the Lambda execution role.

Amazon Bedrock will not be invoked in this next feature.
