---
title: "Billing & invoices"
tags: [billing, invoices, payments]
severity_default: S3
owners: ["#support-billing"]
jira_labels: ["triage", "billing"]
---

## Summary
Invoice mismatches, missing invoices, wrong currency, or tax/VAT questions.

## Typical Requests
- "I can't find last month's invoice"
- "Charged twice"
- "Wrong currency or VAT shown"

## Triage Checklist
1. Confirm account ID and billing period.  
2. Check payment provider dashboard (Stripe) for duplicates/refunds.  
3. Verify tax settings and currency at account-level.  
4. Provide invoice download link if available.

## Engineering
- Reconcile Stripe events with our ledger.  
- Trigger invoice regeneration if metadata was corrected.
