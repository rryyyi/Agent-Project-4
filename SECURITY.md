# Security policy

## Supported version

Security fixes target the latest 0.1.x release. This is a local single-user research tool, not an authenticated hosted service.

## Reporting

Do not post secrets or exploit payloads containing private data in public issues. If GitHub's private vulnerability reporting is available on this repository, use the Security tab to submit a private report. Otherwise open a minimal issue requesting a private reporting channel without disclosing exploit details or private data.

Include affected version, environment, impact and minimal reproduction once a private channel is established. No response-time SLA is promised.

## Deployment boundaries

- Default binding is 127.0.0.1; the API has no authentication or tenant isolation.
- Do not expose the service publicly without access controls and operational limits.
- LLM requests send persona and bounded history to the configured upstream provider.
- Runtime traces contain prompts/persona data; review before sharing.
- Keys are read from the server environment, not browser configuration.
- Provider exception text is suppressed; successful model text remains untrusted data.
- PDF parsing is bounded, but not sandboxed for hostile files. Use trusted documents.
- Browser explanations are inserted as text. JSON exports contain original explanation text.
- The per-process API admission cap is not a distributed usage quota.
