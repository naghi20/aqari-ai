# AQARI AI Data Privacy Policy

## Purpose

AQARI AI processes real-estate listing information to create editable content drafts. The project is built as a public portfolio repository, but real customer and production property data must remain private.

## Prohibited repository content

The public GitHub repository must never contain:

- Joomla MySQL dumps or database exports
- real listing records
- property owner, tenant, agent, or customer names
- phone numbers, email addresses, national IDs, passport details, or payment information
- exact private addresses
- production property images
- AWS credentials, IAM access keys, Meta tokens, Joomla credentials, or secrets
- Terraform state files
- S3 object URLs that expose private content

## Approved development data

Only these may be committed:

- fictional or anonymized property examples
- data schemas
- synthetic test records
- non-sensitive configuration templates
- architecture diagrams
- source code, infrastructure code, and documentation

## Source of truth

Human-entered and verified property data is the source of truth. AI-generated content is a draft and must not be treated as a verified statement of fact.

## Human approval

Before external publication, an authorized human must verify:

- property type
- rent or sale price
- location
- bedrooms and bathrooms
- size
- furnishing and parking details
- amenities
- availability
- images selected for publication
- generated website and social-media text

## Future controls

Later project phases will add:

- S3 private buckets and encryption
- Cognito authentication
- IAM least-privilege roles
- CloudWatch audit logging
- DynamoDB approval records
- Secrets Manager for third-party credentials
- image metadata removal
- Amazon Rekognition moderation and quality checks
