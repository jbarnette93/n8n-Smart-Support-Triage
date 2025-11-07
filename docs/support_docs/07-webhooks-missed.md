---
title: "Missed or delayed webhooks"
tags: [webhooks, integrations, retries]
severity_default: S3
owners: ["#integrations"]
jira_labels: ["triage", "webhooks"]
---

## Summary
Partners report not receiving webhooks or receiving them late/out-of-order.

## Common Causes
- Partner endpoint 500/timeout; we back off  
- Signature verification failures on partner side  
- Clock skew creates ordering confusion

## Triage
1. Search by event ID; confirm delivery attempts and status.  
2. Verify partner's endpoint health and TLS cert.  
3. Suggest idempotency and ack/retry model.

## Engineering
- Tune retry schedule; dead-letter queue monitoring.  
- Provide replay endpoint with filters (event type, time range).
