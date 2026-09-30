# AWS Resources

This document records the AWS resources used by AQARI AI during the console-first MVP phase.

## Security note

This public repository does not contain:

- AWS account IDs
- Exact account-specific S3 bucket names
- AWS access keys
- GitHub tokens
- Joomla credentials
- Meta credentials
- Customer data
- Production property images
- Joomla database exports
- Terraform state files

## AWS Region

```text
eu-central-1
Europe (Frankfurt)
```

## Amazon S3

### Purpose

The S3 bucket will store original property images privately.

Initial MVP use:

```text
Private storage only
No real photos uploaded during resource setup
No public bucket access
No static website hosting
No direct browser upload permissions
```

### Safe bucket-name pattern

```text
aqari-ai-<aws-account-id>-euc1
```

The exact bucket name is intentionally excluded because it contains the AWS account identifier.

### Security configuration

| Setting | AQARI AI MVP configuration |
|---|---|
| Region | `eu-central-1` |
| Bucket type | General purpose |
| Object ownership | Bucket owner enforced |
| ACLs | Disabled |
| Block Public Access | All four settings enabled |
| Default encryption | SSE-S3 (`AES256`) |
| Versioning | Disabled for MVP |
| Static website hosting | Disabled |
| Initial object count | Zero |
| Real photos uploaded | No |

### Resource tags

| Key | Value |
|---|---|
| `Project` | `AQARI-AI` |
| `Environment` | `dev` |
| `ManagedBy` | `aws-cli-console-first` |
| `Owner` | `naghi20` |

## Amazon DynamoDB

### Table

```text
aqari-ai-properties-dev
```

### Purpose

DynamoDB will store property drafts and controlled AI-generation metadata.

Future records may include:

```text
property_id
listing_status
verified_property_data
s3_image_prefix
generated_listing_draft
model_id
prompt_version
created_at
updated_at
approved_by
approved_at
export_status
audit_events
```

### MVP configuration

| Setting | AQARI AI MVP configuration |
|---|---|
| Region | `eu-central-1` |
| Table name | `aqari-ai-properties-dev` |
| Table status | `ACTIVE` |
| Billing mode | On-demand / `PAY_PER_REQUEST` |
| Table class | DynamoDB Standard |
| Partition key | `property_id` |
| Partition key type | String (`S`) |
| Sort key | None |
| Encryption at rest | DynamoDB default encryption |
| Point-in-time recovery | Disabled for MVP |
| Deletion protection | Disabled for MVP |
| Initial property records | Zero |

### Resource tags

| Key | Value |
|---|---|
| `Project` | `AQARI-AI` |
| `Environment` | `dev` |
| `ManagedBy` | `aws-cli-console-first` |
| `Owner` | `naghi20` |

## Cost-control decisions

- AWS Budgets are configured before Bedrock invocation.
- The S3 bucket remains empty until the secure upload workflow exists.
- DynamoDB uses on-demand billing to avoid provisioned capacity planning.
- Bedrock will be invoked only for explicit create, edit, or regenerate actions.
- Generated text will be stored and reused rather than regenerated on each page view.
- Rekognition, Step Functions, public website hosting, and social-media automation are future phases.

## Planned resource lifecycle

| Phase | Resource action |
|---|---|
| Current | Empty private S3 bucket and empty DynamoDB table |
| Backend MVP | Lambda writes validated property drafts to DynamoDB |
| Upload phase | Lambda creates limited-time S3 pre-signed upload URLs |
| AI phase | Lambda invokes Bedrock with verified fields only |
| Review phase | Draft records gain approval and audit fields |
| Future | Rekognition, Step Functions, Joomla API, and Meta publishing |
