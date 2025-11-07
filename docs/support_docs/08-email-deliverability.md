---
title: "Email deliverability"
tags: [email, deliverability, smtp, dmarc, dkim, spf]
severity_default: S3
owners: ["#platform-email"]
jira_labels: ["triage", "email"]
---

## Summary
Customers don't receive emails or see high spam/junk placement.

## Checklist
- Verify domain alignment for SPF/DKIM/DMARC.  
- Check provider status (SES/SendGrid).  
- Suppression list: confirm address not suppressed.  
- Content checks: excessive links, all caps, URL mismatches.

## Guidance
- Encourage domain authentication and subdomain for transactional.  
- Warm up new IPs slowly.  
- Provide test mode with seed list.
