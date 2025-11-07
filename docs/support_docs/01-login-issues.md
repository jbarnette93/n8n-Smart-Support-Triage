---
title: "Login issues / cannot sign in"
tags: [auth, login, accounts, frontend]
severity_default: S3
last_reviewed: 2025-10-15
owners: ["#support-auth", "@oncall-auth"]
jira_labels: ["triage", "auth", "login"]
---

## Summary
Users report being unable to log in: spinning loader, invalid credentials, or unexpected "account not found" messages.

## Symptoms
- "Invalid email or password" even when correct
- Loader spins and returns to login screen
- "Account not found" after signup
- Works on mobile but not web (or vice versa)

## Common Causes
- Account not verified (email confirmation pending)
- Recent password change not propagated to cache/session store
- OAuth provider outage (Google/Apple)
- Region-based cookie/CORS misconfig after deploy
- Clock skew on client older than 5 minutes

## Quick Triage Checklist
1. Check **Status Page** for auth/IdP incidents.
2. Verify account state (active, verified) in the admin panel.
3. Ask for timestamp, browser, and request ID (if visible in footer/console).
4. Test login on a fresh browser profile or incognito.
5. Look for spikes in `auth.login.failed` and `auth.oauth.error` metrics.

## Resolution Paths
**Self-serve**  
- Resend verification email.  
- Clear cookies/site data and retry.  
- Try password reset.

**Engineering**
- Invalidate auth cache for the user ID.  
- Check IdP logs and client secrets rotation status.  
- Review last deploy diff for auth/cookie domain changes.

## Observability
- Logs: `auth-service` → `login_failed`, `oauth_callback_error`  
- Metrics: error rate < 0.5% baseline; alert at > 2% over 5 min

## Escalation
- S3 → S2 if affecting > 5% of active users or cross-region.
- Page `@oncall-auth` if sustained > 15 min.

## Notes for Automation
- If user mentions `login`, `sign in`, or `can't sign in`, suggest verification and password reset first.
