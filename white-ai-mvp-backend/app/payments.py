import hashlib
import hmac
import json
import os
from collections import deque
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter(prefix="/billing", tags=["billing"])

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "").strip()
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "").strip()
RAZORPAY_PLAN_ID = os.getenv("RAZORPAY_PLAN_ID", "").strip()
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").strip()
CRYPTO_PROVIDER_ENABLED = os.getenv("CRYPTO_PROVIDER_ENABLED", "false").lower() == "true"

# Temporary diagnostic event store only. Use a database + idempotency before production.
verified_webhook_events: deque[dict[str, Any]] = deque(maxlen=100)


@router.get("/options")
def billing_options():
    """Shows configuration status only; it never claims that payments are live."""
    razorpay_ready = bool(
        RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and RAZORPAY_PLAN_ID
    )
    return {
        "project": "WHITE AI MVP",
        "mode": "configuration_scaffold",
        "india_upi_phonepe": {
            "available_through_provider": "Razorpay, if approved and enabled in dashboard",
            "configured": razorpay_ready,
        },
        "international_cards": {
            "available_through_provider": "Razorpay, if approved and enabled in dashboard",
            "configured": razorpay_ready,
        },
        "subscriptions": {"configured": razorpay_ready},
        "crypto": {
            "enabled": False,
            "provider_flag": CRYPTO_PROVIDER_ENABLED,
            "message": "Live crypto checkout is intentionally not implemented. Complete legal, tax, FIU-IND and provider eligibility review first.",
        },
        "automatic_40_percent_transfer": {
            "enabled": False,
            "message": "No automatic payouts. Reconcile verified payments, refunds, fees, tax and written recipient agreement first.",
        },
        "warning": "Configuration status is not proof of payment-provider approval or a successful live payment.",
    }


@router.post("/subscription")
async def create_subscription():
    """Creates a hosted subscription link from a preconfigured provider plan."""
    if not (RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and RAZORPAY_PLAN_ID):
        raise HTTPException(
            status_code=503,
            detail="Payments are not configured. Set Razorpay secrets and create/approve a plan in the Razorpay Dashboard first.",
        )

    payload = {
        "plan_id": RAZORPAY_PLAN_ID,
        "total_count": 12,
        "quantity": 1,
        "customer_notify": True,
        "notes": {"product": "WHITE AI Premium"},
    }
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                "https://api.razorpay.com/v1/subscriptions",
                auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
                json=payload,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Could not connect to payment provider.")

    if response.status_code >= 400:
        # Do not return provider response bodies because they may contain account details.
        raise HTTPException(
            status_code=502,
            detail=f"Payment provider rejected subscription creation (HTTP {response.status_code}). Check dashboard activation and plan settings.",
        )
    data = response.json()
    short_url = data.get("short_url")
    if not short_url:
        raise HTTPException(status_code=502, detail="Provider did not return a hosted checkout URL.")
    return {
        "provider": "razorpay",
        "subscription_id": data.get("id"),
        "checkout_url": short_url,
        "status": data.get("status", "created"),
        "note": "Hosted checkout created. Do not activate premium access until a verified payment/subscription webhook is processed.",
    }


@router.post("/razorpay/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str | None = Header(default=None),
):
    """Verifies Razorpay's webhook signature. Event storage is RAM-only in this starter."""
    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret is not configured.")
    if not x_razorpay_signature:
        raise HTTPException(status_code=400, detail="Missing webhook signature.")

    raw_body = await request.body()
    expected = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature.")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    event_name = payload.get("event", "unknown")
    verified_webhook_events.append(
        {
            "event": event_name,
            "received_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {"received": True, "verified": True, "event": event_name}


@router.get("/webhook-status")
def webhook_status():
    """Non-sensitive diagnostics; RAM-only and not a production audit log."""
    return {
        "recent_verified_events": list(verified_webhook_events),
        "storage": "temporary RAM only",
        "production_ready": False,
    }
