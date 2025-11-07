---
title: "SSO/SAML/OIDC setup & errors"
tags: [sso, saml, oidc, enterprise]
severity_default: S3
owners: ["#support-auth", "#enterprise"]
jira_labels: ["triage", "sso"]
---

## Summary
Enterprise customers need help setting up SSO or experience login loops/assertion errors.

## Common Causes
- Wrong ACS/redirect URL or Audience/Entity ID mismatch  
- Clock skew > 3 minutes  
- NameID format mismatch (email vs. persistent ID)  
- Group/role mapping misconfigured

## Triage
1. Collect IdP metadata XML or OIDC discovery URL.  
2. Confirm certificate fingerprint and validity dates.  
3. Compare Audience/Redirect URLs with tenant config.

## Resolution
- Provide correct metadata templates.  
- Enable debug mode and share correlation IDs.  
- For OIDC, verify scopes (`openid email profile`) and client secret rotation.
