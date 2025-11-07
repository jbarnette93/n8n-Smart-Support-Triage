---
title: "2FA / MFA problems"
tags: [auth, 2fa, otp, totp, sms]
severity_default: S3
last_reviewed: 2025-10-15
owners: ["#support-auth", "@oncall-auth"]
jira_labels: ["triage", "auth", "2fa"]
---

## Summary
Users cannot complete two-factor authentication (TOTP codes rejected, SMS delays, backup codes lost).

## Symptoms
- TOTP code always invalid
- SMS code delays > 60 seconds
- Phone lost / number changed
- Backup codes not working

## Common Causes
- Time drift on device (>30s) for TOTP
- Carrier filtering for SMS
- Rate-limited due to too many attempts
- 2FA reset pending approval

## Quick Triage Checklist
1. Ask if device time is set to **Automatic**.
2. Check rate-limit counters for the user.
3. Verify SMS provider status (Twilio/MessageBird).

## Resolution Paths
**Self-serve**  
- Sync device time; use backup codes.  
- Wait 60s and request new code.

**Engineering**  
- Reset 2FA for user with identity verification.  
- Switch delivery channel (SMS → email) if policy allows.

## Observability
- `auth.2fa.verify_failed`, `auth.2fa.sms_latency_ms`

## Escalation
- S2 if provider-wide SMS delays or verification failures > 10%.
