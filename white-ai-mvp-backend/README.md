# WHITE AI MVP Backend (starter)

FastAPI starter backend for the WHITE AI web and Android clients.

## Endpoints
- `GET /` project status
- `GET /health` health check
- `GET /api-status` whether a server-side Gemini key is configured
- `POST /chat` chat API compatible with the web and Android clients
- `GET /billing/options` payment configuration status (not proof of live approval)
- `POST /billing/subscription` creates a hosted Razorpay subscription link from a preconfigured plan
- `POST /billing/razorpay/webhook` verifies Razorpay webhook signature
- `GET /billing/webhook-status` temporary RAM-only webhook diagnostics

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open `/docs` to test the API.

## Configure AI
Set `GEMINI_API_KEY` in the hosting provider's secret/environment settings. Never commit keys to GitHub or put them in mobile/web client code. Check current provider quota and data-use terms before using real user messages.

## Configure Razorpay (test mode first)
1. Create/verify your Razorpay merchant account and complete required KYC.
2. Enable UPI and international cards only if Razorpay approves your account and the relevant features.
3. Create a subscription plan in the Razorpay Dashboard. Put its ID in `RAZORPAY_PLAN_ID`.
4. Add `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_PLAN_ID`, and `RAZORPAY_WEBHOOK_SECRET` in hosting Secrets (for example Replit Secrets). Never put real keys in GitHub, Wix HTML, or Android code.
5. Configure the Razorpay webhook URL as `https://YOUR-BACKEND-HOST/billing/razorpay/webhook` and select relevant subscription/payment events in the dashboard.
6. Test with provider test mode and verify webhook signatures before considering live mode.

The subscription endpoint uses a fixed, dashboard-created plan; it does not accept an arbitrary amount from the client. The hosted checkout URL is returned as `checkout_url`.

## Revenue-share accounting
The requested 40% share is **not automatically transferred**. Before any payout, agree in writing on the calculation base (gross or net), treatment of payment fees, refunds, taxes, AI/hosting costs, and payout schedule. Verify the recipient independently. This starter has no persistent ledger or automatic PhonePe payout integration.

## Crypto
Live crypto checkout is intentionally disabled. Do not enable it by setting a flag alone. First confirm provider availability, applicable Indian tax obligations, and any FIU-IND/PMLA registration or reporting obligations with qualified legal/compliance advice.

## Important production limitations
- Conversation memory and webhook diagnostics are stored only in server RAM and disappear on restart.
- No authentication, persistent database, idempotency handling, rate limiting, entitlement activation, refunds, or production monitoring yet.
- Payment routes are an integration scaffold, not production-ready. Do not expose checkout creation publicly until authentication, abuse prevention, persistent transaction records, webhook idempotency, and server-side subscription entitlement checks are implemented.
- A successful webhook signature alone is not enough to grant premium access; verify event type, payment/subscription status, amount, currency, and duplicate delivery in persistent storage.
- Before public deployment, configure exact CORS origins, request limits, privacy controls, HTTPS, and a reviewed privacy/refund/terms policy.
- Do not send sensitive data to this starter.
