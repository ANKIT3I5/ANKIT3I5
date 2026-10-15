# WHITE AI MVP Security Policy

This repository is an early-stage MVP. Passing automated checks does not mean the service is production-ready.

## Supported versions
Only the current main branch is maintained during this MVP stage. No production SLA is provided.

## Report a vulnerability
Please do not publish exploit details or secrets in a public issue. Use GitHub's private vulnerability reporting feature if it is enabled for this repository; otherwise contact the repository owner privately through GitHub. Include affected path, impact, and safe reproduction steps. Do not include live credentials or private user data.

## Secrets and keys
- Never commit real API keys, passwords, webhook secrets, private keys, access tokens, or production environment files.
- Store backend credentials only in the hosting provider's encrypted Secrets/environment settings.
- Keep Gemini and payment-provider secrets on the backend. Never embed them in Android, Wix/browser JavaScript, app config, or APKs.
- Use least-privilege credentials, separate test and production keys, and rotate/revoke a key immediately if it may have leaked.
- .gitignore reduces accidental commits but does not protect secrets already tracked or pushed.

## Transport and access
- Use HTTPS for deployed API traffic.
- Keep CORS restricted to known origins. CORS is not authentication.
- Before public production use, add authentication/authorization, per-user and per-IP rate limits, request-size limits, abuse monitoring, and a persistent audit trail.
- Do not expose subscription creation or privileged operations publicly until authorization, webhook idempotency, persistent transaction records, and server-side entitlement checks exist.

## Monitoring and response
- Review GitHub Actions security checks on every change.
- Enable GitHub Secret Scanning and Push Protection in repository Settings if available for this repository. A workflow scan runs after a push/PR; it is not a substitute for push protection.
- If a credential is exposed, revoke/rotate it at the provider first, inspect its usage, remove it from current code, and follow GitHub's sensitive-data removal guidance for history cleanup.
- Do not log raw secrets, authorization headers, payment payloads containing sensitive data, or private user messages unnecessarily.

## Current limitations
- This MVP does not yet have production-grade authentication, persistent storage, automated key rotation, alerting, or full request rate limiting.
- Payment routes are scaffolding, not production payment infrastructure.
- A successful CI run verifies only the checks configured in that workflow; it does not certify the app or hosting environment as secure.
