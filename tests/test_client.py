"""Tests for the Decane Python SDK."""

import hashlib
import hmac
import json
import time

import httpx
import pytest
import respx

from decane import (
    Decane,
    AsyncDecane,
    DecaneError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    InvalidSignatureError,
)

BASE = "https://api.decane.io/api/v1"


# ── Sync Client Tests ──


class TestFlow:
    def test_init_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key is required"):
            Decane(api_key="")

    def test_repr(self):
        flow = Decane(api_key="test_key")
        assert repr(flow) == "Decane(connected)"
        flow.close()

    def test_context_manager(self):
        with Decane(api_key="test_key") as flow:
            assert repr(flow) == "Decane(connected)"


class TestInvoices:
    @respx.mock
    def test_create(self):
        respx.post(f"{BASE}/invoices").mock(
            return_value=httpx.Response(200, json={
                "id": "inv_123",
                "merchant_id": "m_1",
                "amount": 100.0,
                "currency": "USDT",
                "network": "tron",
                "status": "pending",
                "wallet_address": "TXyz123",
                "payment_url": "https://pay.decane.io/inv_123",
            })
        )
        with Decane(api_key="test_key") as flow:
            inv = flow.invoices.create(amount=100, currency="USDT", network="tron")
            assert inv.id == "inv_123"
            assert inv.wallet_address == "TXyz123"
            assert inv.status.value == "pending"
            assert inv.amount == 100.0

    @respx.mock
    def test_get(self):
        respx.get(f"{BASE}/invoices/inv_123").mock(
            return_value=httpx.Response(200, json={
                "id": "inv_123", "merchant_id": "m_1",
                "amount": 100.0, "currency": "USDT", "network": "tron",
                "status": "completed", "tx_hash": "0xabc",
            })
        )
        with Decane(api_key="test_key") as flow:
            inv = flow.invoices.get("inv_123")
            assert inv.status.value == "completed"
            assert inv.tx_hash == "0xabc"

    @respx.mock
    def test_list(self):
        respx.get(f"{BASE}/invoices").mock(
            return_value=httpx.Response(200, json={
                "items": [
                    {"id": "inv_1", "merchant_id": "m_1", "amount": 50, "currency": "USDT", "network": "tron", "status": "completed"},
                    {"id": "inv_2", "merchant_id": "m_1", "amount": 75, "currency": "BTC", "network": "bitcoin", "status": "pending"},
                ],
                "total": 2, "page": 1, "per_page": 50,
            })
        )
        with Decane(api_key="test_key") as flow:
            result = flow.invoices.list()
            assert len(result.items) == 2
            assert result.items[0].id == "inv_1"


class TestPayouts:
    @respx.mock
    def test_create(self):
        respx.post(f"{BASE}/vendor/payout").mock(
            return_value=httpx.Response(200, json={
                "id": "pout_123", "amount": 50.0, "currency": "USDT",
                "network": "tron", "destination_address": "TXyz",
                "status": "pending",
            })
        )
        with Decane(api_key="test_key") as flow:
            payout = flow.payouts.create(
                amount=50, currency="USDT", network="tron", recipient_address="TXyz",
            )
            assert payout.id == "pout_123"
            assert payout.status == "pending"

    @respx.mock
    def test_batch(self):
        respx.post(f"{BASE}/vendor/payout/batch").mock(
            return_value=httpx.Response(200, json={
                "payouts": [
                    {"id": "p1", "amount": 50, "currency": "USDT", "network": "tron", "destination_address": "T1", "status": "pending"},
                    {"id": "p2", "amount": 25, "currency": "USDT", "network": "tron", "destination_address": "T2", "status": "pending"},
                ]
            })
        )
        with Decane(api_key="test_key") as flow:
            payouts = flow.payouts.create_batch([
                {"amount": 50, "currency": "USDT", "network": "tron", "destination_address": "T1"},
                {"amount": 25, "currency": "USDT", "network": "tron", "destination_address": "T2"},
            ])
            assert len(payouts) == 2


class TestWallets:
    @respx.mock
    def test_generate(self):
        respx.post(f"{BASE}/wallets/generate").mock(
            return_value=httpx.Response(200, json={
                "id": "wal_123", "address": "0xabc", "network": "ethereum",
                "currency": "USDT", "balance": 0,
            })
        )
        with Decane(api_key="test_key") as flow:
            wallet = flow.wallets.generate(network="ethereum", currency="USDT")
            assert wallet.address == "0xabc"
            assert wallet.network == "ethereum"


class TestSwaps:
    @respx.mock
    def test_quote(self):
        respx.post(f"{BASE}/vendor/swap/quote").mock(
            return_value=httpx.Response(200, json={
                "from_currency": "BTC", "to_currency": "USDT",
                "from_amount": 0.01, "to_amount": 670.50, "rate": 67050.0,
            })
        )
        with Decane(api_key="test_key") as flow:
            quote = flow.swaps.quote("BTC", "USDT", 0.01)
            assert quote.to_amount == 670.50
            assert quote.rate == 67050.0


class TestWebhooks:
    def test_verify_valid(self):
        secret = "whsec_test123"
        payload = json.dumps({"id": "evt_1", "type": "invoice.paid", "data": {"id": "inv_1"}})
        sig = "sha256=" + hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        flow = Decane(api_key="test_key", webhook_secret=secret)
        event = flow.webhooks.verify(payload, sig)
        assert event.type == "invoice.paid"
        assert event.data["id"] == "inv_1"
        flow.close()

    def test_verify_invalid(self):
        flow = Decane(api_key="test_key", webhook_secret="whsec_test123")
        with pytest.raises(InvalidSignatureError):
            flow.webhooks.verify('{"test": true}', "badsig")
        flow.close()

    def test_is_valid(self):
        secret = "whsec_test123"
        payload = '{"id": "evt_1", "type": "test"}'
        sig = "sha256=" + hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        flow = Decane(api_key="test_key", webhook_secret=secret)
        assert flow.webhooks.is_valid(payload, sig) is True
        assert flow.webhooks.is_valid(payload, "wrong") is False
        flow.close()


def _sign(secret: str, body: str, ts: int) -> str:
    mac = hmac.new(secret.encode(), f"{ts}.".encode() + body.encode(), hashlib.sha256).hexdigest()
    return f"t={ts},v1={mac}"


class TestWebhookTimestamped:
    secret = "whsec_test123"
    body = '{"id": "evt_1", "event": "invoice.completed", "created": 1700000000, "data": {"id": "inv_1"}}'

    def test_valid(self):
        ts = int(time.time())
        h = _sign(self.secret, self.body, ts)
        flow = Decane(api_key="test_key", webhook_secret=self.secret)
        assert flow.webhooks.verify_signature(self.body, h) is True
        assert flow.webhooks.verify_signature(self.body.encode(), f"t={ts}, v1={h.split('v1=')[1]}, v0=x") is True
        event = flow.webhooks.construct_event(self.body, h)
        assert event.type == "invoice.completed"
        flow.close()

    def test_fixed_vector(self):
        ts = 1700000000
        h = _sign(self.secret, self.body, ts)
        flow = Decane(api_key="test_key", webhook_secret=self.secret)
        assert flow.webhooks.verify_signature(self.body, h, tolerance=10**9) is True
        flow.close()

    def test_failures(self):
        ts = int(time.time())
        h = _sign(self.secret, self.body, ts)
        flow = Decane(api_key="test_key", webhook_secret=self.secret)
        assert flow.webhooks.verify_signature(self.body, _sign("other", self.body, ts)) is False
        assert flow.webhooks.verify_signature(self.body + " ", h) is False
        old = _sign(self.secret, self.body, ts - 301)
        assert flow.webhooks.verify_signature(self.body, old) is False
        assert flow.webhooks.verify_signature(self.body, old, tolerance=600) is True
        assert flow.webhooks.verify_signature(self.body, "garbage") is False
        with pytest.raises(InvalidSignatureError):
            flow.webhooks.construct_event(self.body, old)
        flow.close()


class TestIdempotency:
    @respx.mock
    def test_invoice_key_sent(self):
        route = respx.post(f"{BASE}/invoices").mock(
            return_value=httpx.Response(200, json={"id": "inv_1", "merchant_id": "m", "amount": 1, "currency": "USDT", "network": "tron", "status": "pending"})
        )
        with Decane(api_key="test_key") as flow:
            flow.invoices.create(amount=1, currency="USDT", network="tron", idempotency_key="order-42")
        assert route.calls.last.request.headers["Idempotency-Key"] == "order-42"

    @respx.mock
    def test_payout_key_sent(self):
        route = respx.post(f"{BASE}/vendor/payout").mock(
            return_value=httpx.Response(200, json={"id": "p1", "amount": 1, "currency": "USDT", "network": "tron", "status": "pending"})
        )
        with Decane(api_key="test_key") as flow:
            flow.payouts.create(amount=1, currency="USDT", network="tron", recipient_address="T", idempotency_key="k.1")
        assert route.calls.last.request.headers["Idempotency-Key"] == "k.1"

    @respx.mock
    def test_batch_key_sent(self):
        route = respx.post(f"{BASE}/vendor/payout/batch").mock(return_value=httpx.Response(200, json={"payouts": []}))
        with Decane(api_key="test_key") as flow:
            flow.payouts.create_batch([], idempotency_key="b-1")
        assert route.calls.last.request.headers["Idempotency-Key"] == "b-1"

    @respx.mock
    def test_auto_generated_and_stable_across_retries(self, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda s: None)
        route = respx.post(f"{BASE}/invoices").mock(
            side_effect=[
                httpx.Response(503, json={"detail": "down"}),
                httpx.Response(200, json={"id": "inv_1", "merchant_id": "m", "amount": 1, "currency": "USDT", "network": "tron", "status": "pending"}),
            ]
        )
        with Decane(api_key="test_key") as flow:
            flow.invoices.create(amount=1, currency="USDT", network="tron")
        keys = {c.request.headers["Idempotency-Key"] for c in route.calls}
        assert len(route.calls) == 2 and len(keys) == 1 and len(next(iter(keys))) == 36


class TestErrors:
    @respx.mock
    def test_401(self):
        respx.get(f"{BASE}/invoices/x").mock(
            return_value=httpx.Response(401, json={"detail": "Invalid API key"})
        )
        with Decane(api_key="bad_key") as flow:
            with pytest.raises(AuthenticationError):
                flow.invoices.get("x")

    @respx.mock
    def test_404(self):
        respx.get(f"{BASE}/invoices/nonexistent").mock(
            return_value=httpx.Response(404, json={"detail": "Not found"})
        )
        with Decane(api_key="test_key") as flow:
            with pytest.raises(NotFoundError):
                flow.invoices.get("nonexistent")

    @respx.mock
    def test_429(self):
        respx.get(f"{BASE}/invoices/x").mock(
            return_value=httpx.Response(429, json={"detail": "Too many requests"}, headers={"Retry-After": "5"})
        )
        with Decane(api_key="test_key") as flow:
            with pytest.raises(RateLimitError) as exc_info:
                flow.invoices.get("x")
            assert exc_info.value.retry_after == 5.0


# ── Async Client Tests ──


class TestAsyncFlow:
    @pytest.mark.asyncio
    @respx.mock
    async def test_create_invoice(self):
        respx.post(f"{BASE}/invoices").mock(
            return_value=httpx.Response(200, json={
                "id": "inv_async", "merchant_id": "m_1",
                "amount": 200.0, "currency": "BTC", "network": "bitcoin",
                "status": "pending", "wallet_address": "bc1q...",
            })
        )
        async with AsyncDecane(api_key="test_key") as flow:
            inv = await flow.invoices.create(amount=200, currency="BTC", network="bitcoin")
            assert inv.id == "inv_async"
            assert inv.wallet_address == "bc1q..."
