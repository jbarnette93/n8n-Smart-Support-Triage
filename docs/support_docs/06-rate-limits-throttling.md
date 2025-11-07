---
title: "Rate limits & throttling"
tags: [api, rate-limit, 429]
severity_default: S3
owners: ["#platform"]
jira_labels: ["triage", "api", "ratelimit"]
---

## Summary
Clients receive HTTP 429 or SDK throws "RateLimitExceeded".

## Triage
- Confirm client is using exponential backoff.  
- Check tenant-level quotas and recent spikes.  
- Identify new integrations or scripts.

## Guidance
- Advise retry with jitter; reduce concurrency.  
- Temporary quota lift for launches (requires approval).  
- For server-to-server, recommend batch endpoints.
