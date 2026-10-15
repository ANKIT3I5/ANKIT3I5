"""Regression tests for the WHITE AI starter API.

These tests validate safe baseline behavior only; they do not certify production readiness.
"""
import pytest
from fastapi.testclient import TestClient

from app import main


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def isolate_app_state(monkeypatch):
    main.sessions.clear()
    monkeypatch.setattr(main, "GEMINI_API_KEY", "")


def test_health_endpoint_reports_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["project"] == "WHITE AI MVP"


def test_api_status_does_not_expose_secret():
    response = client.get("/api-status")

    assert response.status_code == 200
    body = response.json()
    assert body["ai_configured"] is False
    assert "GEMINI_API_KEY" not in str(body)


def test_chat_without_provider_key_returns_explicit_demo_response():
    response = client.post("/chat", json={"message": "नमस्ते"})

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "demo"
    assert body["session_id"]
    assert "वास्तविक AI" in body["note"]


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_rejects_message_over_limit():
    response = client.post("/chat", json={"message": "x" * 4001})

    assert response.status_code == 422


def test_billing_options_never_claim_live_payment_approval():
    response = client.get("/billing/options")

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "configuration_scaffold"
    assert body["automatic_40_percent_transfer"]["enabled"] is False
    assert body["crypto"]["enabled"] is False
