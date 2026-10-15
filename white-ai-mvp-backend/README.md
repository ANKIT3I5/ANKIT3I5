# WHITE AI MVP Backend (starter)

FastAPI starter backend for the WHITE AI web and Android clients.

## Endpoints
- `GET /` project status
- `GET /health` health check
- `GET /api-status` whether a server-side Gemini key is configured
- `POST /chat` chat API compatible with the web and Android clients

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open `/docs` to test the API.

## Configure AI
Set `GEMINI_API_KEY` in the hosting provider's secret/environment settings. Never commit keys to GitHub or put them in mobile/web client code. Check current provider quota and data-use terms before using real user messages.

## Important current limitations
- Conversation memory is stored only in server RAM and disappears on restart.
- No authentication, persistent database, rate limiting, production monitoring, or search API yet.
- Before deploying for public use, configure CORS for the exact Wix site origin, request limits, privacy controls, and HTTPS.
- Do not send sensitive data to this starter.
