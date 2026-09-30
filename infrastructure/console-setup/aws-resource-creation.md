# AQARI AI AWS Resource Creation

This guide records the console-first and AWS CLI creation of AQARI AI MVP resources.

## Prerequisites

- AWS CLI authenticated locally
- Working Region set to `eu-central-1`
- AWS Budget alerts created
- No real Joomla exports, customer data, or production photos used
- Public GitHub repository already created

## Environment variables

Use shell variables locally. Do not commit an account-specific bucket name.

```bash
export AWS_REGION="eu-central-1"
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query 'Account' --output text)"
export AQARI_BUCKET_NAME="aqari-ai-${AWS_ACCOUNT_ID}-euc1"
export AQARI_TABLE_NAME="aqari-ai-properties-dev"
```

## Create S3 bucket

```bash
aws s3api create-bucket \
  --bucket "${AQARI_BUCKET_NAME}" \
  --region "${AWS_REGION}" \
  --create-bucket-configuration LocationConstraint="${AWS_REGION}"
```

## Secure S3 bucket

```bash
aws s3api put-public-access-block \
  --bucket "${AQARI_BUCKET_NAME}" \
  --public-access-block-configuration \
    BlockPublicAcls=true,\
IgnorePublicAcls=true,\
BlockPublicPolicy=true,\
RestrictPublicBuckets=true

aws s3api put-bucket-ownership-controls \
  --bucket "${AQARI_BUCKET_NAME}" \
  --ownership-controls 'Rules=[{ObjectOwnership=BucketOwnerEnforced}]'

aws s3api put-bucket-encryption \
  --bucket "${AQARI_BUCKET_NAME}" \
  --server-side-encryption-configuration \
  '{
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        },
        "BucketKeyEnabled": false
      }
    ]
  }'

aws s3api put-bucket-tagging \
  --bucket "${AQARI_BUCKET_NAME}" \
  --tagging 'TagSet=[
    {Key=Project,Value=AQARI-AI},
    {Key=Environment,Value=dev},
    {Key=ManagedBy,Value=aws-cli-console-first},
    {Key=Owner,Value=naghi20}
  ]'
```

## Verify S3 security

```bash
aws s3api get-bucket-location \
  --bucket "${AQARI_BUCKET_NAME}"

aws s3api get-public-access-block \
  --bucket "${AQARI_BUCKET_NAME}"

aws s3api get-bucket-ownership-controls \
  --bucket "${AQARI_BUCKET_NAME}"

aws s3api get-bucket-encryption \
  --bucket "${AQARI_BUCKET_NAME}"

aws s3api get-bucket-tagging \
  --bucket "${AQARI_BUCKET_NAME}" \
  --output table

aws s3api list-objects-v2 \
  --bucket "${AQARI_BUCKET_NAME}" \
  --query 'KeyCount' \
  --output text
```

Expected MVP state:

```text
Region: eu-central-1
Public access block: all true
Object ownership: BucketOwnerEnforced
Encryption: AES256
Object count: 0
```

## Create DynamoDB table

```bash
aws dynamodb create-table \
  --table-name "${AQARI_TABLE_NAME}" \
  --attribute-definitions \
    AttributeName=property_id,AttributeType=S \
  --key-schema \
    AttributeName=property_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --tags \
    Key=Project,Value=AQARI-AI \
    Key=Environment,Value=dev \
    Key=ManagedBy,Value=aws-cli-console-first \
    Key=Owner,Value=naghi20 \
  --region "${AWS_REGION}"
```

## Wait for table activation

```bash
aws dynamodb wait table-exists \
  --table-name "${AQARI_TABLE_NAME}" \
  --region "${AWS_REGION}"
```

## Verify DynamoDB table

```bash
aws dynamodb describe-table \
  --table-name "${AQARI_TABLE_NAME}" \
  --region "${AWS_REGION}" \
  --query 'Table.{
    TableName:TableName,
    TableStatus:TableStatus,
    BillingMode:BillingModeSummary.BillingMode,
    PartitionKey:KeySchema.AttributeName,
    PartitionKeyType:AttributeDefinitions.AttributeType
  }' \
  --output table
```

## AWS CLI pager

To prevent CLI output from opening in a pager:

```bash
aws configure set cli_pager ""
```

## Important restrictions

Do not:

- Make the S3 bucket public
- Upload real property photos before pre-signed upload URLs exist
- Upload Joomla MySQL exports
- Store AWS keys, tokens, or passwords in Git
- Store the exact account-specific bucket name in public documentation
- Insert customer data into DynamoDB before the authenticated application exists
- Invoke Bedrock before Lambda validation and cost controls are implemented
