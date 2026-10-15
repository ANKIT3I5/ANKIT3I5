# WHITE AI Android Client (starter)

This folder contains an early Expo / React Native Android client for the WHITE AI MVP.

## Current scope
- Hindi-first chat UI
- Sends messages to the existing FastAPI backend at `POST /chat`
- Keeps the returned session ID in app memory while the app is open
- Backend URL is configured in `src/config.js`

## Not yet done
- No APK has been built or tested on a physical Android phone
- No live backend URL is configured
- No login, persistent memory, or live search
- No AI API key is included; keep provider credentials on the backend

## Run
Install Node.js LTS, then run:
```bash
npm install
npx expo start
```
Open the project with Expo Go on Android. For phone-only development, use an online workspace that supports Node.js and Expo, subject to that service's current capabilities.

## Backend URL
Edit `src/config.js`. Use the public HTTPS URL of your deployed FastAPI backend. Do not use `localhost` to reach a server on another device. The backend must allow the app's web origin if you also test the web client.

This is source code, not a release-ready app.
