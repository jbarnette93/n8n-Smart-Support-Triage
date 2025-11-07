---
title: "Mobile app crash on startup (iOS/Android)"
tags: [mobile, crash, ios, android]
severity_default: S2
owners: ["#mobile", "@oncall-mobile"]
jira_labels: ["incident", "mobile"]
---

## Summary
App crashes immediately on launch for a subset of devices/OS versions.

## Triage
- Confirm app version and OS version; collect crash logs (Xcode/Logcat).  
- Check feature flag rollout % and recent remote config changes.  
- Correlate with dependency updates (analytics SDK, push SDK).

## Actions
- Disable problematic feature flag or remote config.  
- Hotfix and staged rollout; publish store update.  
- Post advisory in-app message if possible.
