# WHITE AI Android Client (starter)

**DNS/VPN/API setup guide:** see [NETWORK_SETUP.md](./NETWORK_SETUP.md). The current app does not implement a custom VPN tunnel; configure device Private DNS separately and use a real VPN provider until a native VPN client and server are provisioned.

Hindi-first Expo / React Native client for the WHITE AI MVP. This folder is **not a native Java Android project**. It is the existing React Native app, chosen to reuse the current code and reduce setup work.

## What works in the starter
- Hindi-first chat interface and new-chat button
- Sends messages to the FastAPI backend at `POST /chat`
- Keeps a returned session ID in memory while the app remains open
- Backend URL is configured in `src/config.js`
- Does not include an AI provider API key

## Not ready for release
- No APK has been built or tested on a physical Android phone
- No public backend URL is configured by default
- No login, persistent chat history, rate limiting, or release signing
- Backend memory is temporary; restarting the server clears sessions
- Billing code in the backend is a scaffold, not production-ready payment processing

## Low-cost Windows setup (4 GB RAM)
Use a physical Android phone with Expo Go rather than an Android Emulator. An emulator can use a lot of RAM.

1. Install Node.js LTS from https://nodejs.org/en/download
2. Install Git if needed from https://git-scm.com/download/win, or download this repository as a ZIP from GitHub.
3. Extract the repository and open a terminal inside `white-ai-mvp-android`.
4. Check Node/npm:
   ```powershell
   node -v
   npm -v
   ```
5. Install dependencies:
   ```powershell
   npm install
   ```
6. Check dependency health:
   ```powershell
   npm run doctor
   ```
7. Start Expo:
   ```powershell
   npm start
   ```
8. Install Expo Go on the Android phone, connect both devices to the same Wi-Fi, then scan the QR code. If LAN discovery is blocked, stop Expo with Ctrl+C and run:
   ```powershell
   npm run start:tunnel
   ```

## Expo SDK compatibility note
This security-audit branch currently targets Expo SDK 57 with React Native 0.86.3. Check Expo Go compatibility for the SDK installed on your phone. If Expo Go reports an SDK mismatch, follow the official SDK upgrade guide at https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/ and run `npx expo-doctor` after dependency changes.

## Configure the backend
Edit `src/config.js` and replace `https://YOUR-BACKEND-URL-HERE` with the public HTTPS URL of your deployed FastAPI backend, without a trailing slash. Example format only: `https://your-service.example.com`.

Check the backend first:
- `GET /health` should return a JSON status of `ok`.
- `GET /api-status` indicates whether a server-side Gemini key is configured.
- `POST /chat` accepts `{"message":"नमस्ते","session_id":null}`.

The starter backend returns a clearly labelled demo response if `GEMINI_API_KEY` is not set. Keep the key in the hosting provider's server-side Secrets/environment variables. Never put it in `src/config.js`, the app, Wix client code, or GitHub.

## Free-first guidance
- Expo Go is for development/testing, not a final standalone APK.
- Do not enable a paid hosting plan or enter payment details just to test the app.
- A free backend host may sleep or have quotas; a sleeping server can take time to wake up.
- Do not enable real payments until authentication, persistent transaction records, webhook idempotency, subscription entitlement checks, privacy terms, and refunds are implemented and reviewed.

## Troubleshooting
- `node is not recognized`: finish installing Node.js, then close and reopen the terminal.
- QR code appears but phone cannot connect: use the same Wi-Fi or try `npm run start:tunnel`.
- SDK mismatch: use the official Expo upgrade guide above; SDK 52 may be too old for the currently installed Expo Go.
- Chat says configure backend URL: the placeholder in `src/config.js` has not been replaced.
- Network/HTTP error: open the backend's `/health` URL in a browser and verify that the service is running.
- AI demo response: the server has no `GEMINI_API_KEY` configured or is intentionally running in demo mode.

This is an early prototype, not a release-ready or security-reviewed application.
