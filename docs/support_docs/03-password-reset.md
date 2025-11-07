---
title: "Password reset not working"
tags: [auth, password, email]
severity_default: S3
owners: ["#support-auth"]
jira_labels: ["triage", "password"]
---

## Summary
Password reset emails not received or links invalid/expired.

## Symptoms
- "We sent a reset email" but user doesn't receive it
- Link leads to "token invalid" or "expired"
- Works for some domains but not others

## Common Causes
- Email in spam, or corporate filters
- Multiple reset requests; earlier token used
- Link clicked by security scanners (auto-expiry)
- Clock skew on token validation

## Quick Triage
1. Confirm email address correctness and domain.  
2. Ask user to check spam and "Quarantine" folders.  
3. Resend once; avoid spamming.  
4. For corporate domains, suggest allow-listing sending domain.

## Engineering
- Increase token lifetime temporarily if mass issue.  
- Add `no-transform` for scanners; use one-time token w/ short TTL + refresh endpoint.
