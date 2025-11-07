---
title: "Payment API 500 errors across regions"
tags: [payments, api, backend, outage]
severity_default: S1
owners: ["#payments", "@oncall-api"]
jira_labels: ["incident", "payments"]
---

## Summary
Elevated 5xx from `/payments/*` endpoints, often following a deploy or provider incident.

## Symptoms
- 500s/502s from payment endpoints
- Spikes in error dashboards (US/EU)
- Refunds delayed or webhook retries pile up

## Likely Causes
- Back-end dependency outage (DB, Redis)  
- Provider issues (Stripe API incident)  
- Breaking change deployed inadvertently  
- Schema migration causing lock/contention

## Immediate Actions (Runbook)
1. **Assess blast radius**: check `payments.api.5xx` and traffic split per region.  
2. **Toggle feature flag** for latest deploy if present.  
3. **Fail open** for idempotent operations if policy allows.  
4. **Rate-limit** non-critical endpoints to protect DB.  
5. Post status-page incident and Slack updates every 15 min.

## Observability
- Logs: `payments-service` error traces with request IDs  
- Metrics: p95 latency, 5xx rate, DB pool saturation

## Resolution
- Rollback or hotfix; coordinate with provider if external.
