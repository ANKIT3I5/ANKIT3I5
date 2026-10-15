# WHITE AI DNS, VPN, and API setup

This document separates device-wide networking from the WHITE AI API. Do not treat a DNS resolver as a VPN server.

## Current implementation status

- Android client API base URL is configured in `src/config.js`. It currently points to the existing Replit HTTPS hostname.
- Backend already exposes `GET /health` and `GET /api-status`.
- This Expo/React Native starter does **not** implement a custom VPN client or native Android `VpnService`.
- No VPN server address, protocol, keys, or client configuration have been supplied. A custom VPN tunnel cannot be brought online without a real server and client configuration.
- Do not commit API keys, VPN private keys, WireGuard configs, or other secrets to this repository.

## 1. Configure Cloudflare Private DNS on Android

On Android 9 or later:

1. Open **Settings**.
2. Open **Connections** or **Network & internet**.
3. Find **Private DNS**. On Samsung devices it is commonly under **Connections → More connection settings → Private DNS**.
4. Choose **Private DNS provider hostname**.
5. Enter `one.one.one.one`.
6. Tap **Save**.

This configures encrypted DNS-over-TLS to Cloudflare. It does **not** create a VPN tunnel. If the phone reports that the server cannot be reached or internet access breaks, return to Private DNS and select **Automatic**.

For malware filtering, Cloudflare documents `security.cloudflare-dns.com` as the Private DNS hostname. Filtering may block some legitimate domains, so use the standard hostname first unless filtering is desired.

Official instructions: https://developers.cloudflare.com/1.1.1.1/setup/android/

## 2. VPN options

### For immediate phone-wide VPN protection

Use Cloudflare's official **1.1.1.1: Faster Internet** app from Google Play, and follow its in-app VPN permission prompt. Its WARP mode uses a Cloudflare-operated tunnel. Android permits only one active VPN connection at a time, so disconnect any other VPN first.

Official instructions: https://developers.cloudflare.com/1.1.1.1/setup/android/

### For a WHITE AI-branded custom VPN

This is **not enabled** in the current Expo app. It requires:
- A provisioned VPN server or managed VPN provider.
- A supported protocol and client configuration, such as a WireGuard profile and server keys.
- A native Android implementation or a vetted native module. Expo Go alone cannot provide a complete custom VPN tunnel.
- Secure storage for private keys, explicit Android VPN permission, connection/error handling, and leak/reconnect testing.

Do not invent a server endpoint or generate fake connection credentials. Do not claim the VPN is connected until a real tunnel is established and tested.

## 3. API configuration and live checks

The mobile client reads the base URL from `src/config.js`. Keep it as an HTTPS origin with no trailing slash. Never put the Gemini provider key in the app.

Check the currently configured backend from a browser or terminal:

- `GET https://gifted-wonderful-publishers--ankit3i5.replit.app/health`
  - Expected: HTTP 200 and JSON containing `"status":"ok"`.
- `GET https://gifted-wonderful-publishers--ankit3i5.replit.app/api-status`
  - Check `ai_configured`; `true` only means a server-side Gemini key is present, not that model calls/quota have been proven.
- `POST https://gifted-wonderful-publishers--ankit3i5.replit.app/chat`
  - JSON body: `{"message":"नमस्ते","session_id":null}`.
  - If `provider` is `demo`, the backend is responding but live AI is not configured for that response.

Example PowerShell checks:

```powershell
Invoke-RestMethod "https://gifted-wonderful-publishers--ankit3i5.replit.app/health"
Invoke-RestMethod "https://gifted-wonderful-publishers--ankit3i5.replit.app/api-status"
```

If a request fails, verify that the backend deployment is running, the hostname resolves, and the deployment URL has not changed. Do not label the API live until an actual request succeeds.

## 4. Acceptance checklist

- [ ] Android Private DNS saves successfully and browsing still works.
- [ ] If using WARP, the Android system VPN indicator appears and WARP reports Connected.
- [ ] `/health` returns HTTP 200 from the target phone/network.
- [ ] `/api-status` is reviewed without exposing the secret key.
- [ ] `/chat` returns a response; distinguish `demo` from `gemini`.
- [ ] Custom WHITE AI VPN remains marked **not configured** until a real server and native client are provisioned.
- [ ] Keep the dependency security audit blocking; never suppress advisories to make CI green.
