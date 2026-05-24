"""Tests for the Flow Python SDK."""

import hashlib
import hmac
import json

import httpx
import pytest
import respx

from granthe import (
    Flow,
    AsyncFlow,
    FlowError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    InvalidSignatureError,
)

BASE = "https://granthe.io/api/flow"


# ── Sync Client Tests ──


class TestFlow:
    def test_init_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key is required"):
            Flow(api_key="")

    def test_repr(self):
        flow = Flow(api_key="test_key")
        assert repr(flow) == "Flow(connected)"
        flow.close()

    def test_context_manager(self):
        with Flow(api_key="test_key") as flow:
            assert repr(flow) == "Flow(connected)"


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
                "payment_url": "https://pay.granthe.io/inv_123",
            })
        )
        with Flow(api_key="test_key") as flow:
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
                "status": "paid", "tx_hash": "0xabc",
            })
        )
        with Flow(api_key="test_key") as flow:
            inv = flow.invoices.get("inv_123")
            assert inv.status.value == "paid"
            assert inv.tx_hash == "0xabc"

    @respx.mock
    def test_list(self):
        respx.get(f"{BASE}/invoices").mock(
            return_value=httpx.Response(200, json={
                "items": [
                    {"id": "inv_1", "merchant_id": "m_1", "amount": 50, "currency": "USDT", "network": "tron", "status": "paid"},
                    {"id": "inv_2", "merchant_id": "m_1", "amount": 75, "currency": "BTC", "network": "bitcoin", "status": "pending"},
                ],
                "total": 2, "page": 1, "per_page": 50,
            })
        )
        with Flow(api_key="test_key") as flow:
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
        with Flow(api_key="test_key") as flow:
            payout = flow.payouts.create(
                amount=50, currency="USDT", network="tron", destination="TXyz",
            )
            assert payout.id == "pout_123"
            assert payout.status.value == "pending"

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
        with Flow(api_key="test_key") as flow:
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
        with Flow(api_key="test_key") as flow:
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
        with Flow(api_key="test_key") as flow:
            quote = flow.swaps.quote("BTC", "USDT", 0.01)
            assert quote.to_amount == 670.50
            assert quote.rate == 67050.0


class TestWebhooks:
    def test_verify_valid(self):
        secret = "whsec_test123"
        payload = json.dumps({"id": "evt_1", "type": "invoice.paid", "data": {"id": "inv_1"}})
        sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        flow = Flow(api_key="test_key", webhook_secret=secret)
        event = flow.webhooks.verify(payload, sig)
        assert event.type == "invoice.paid"
        assert event.data["id"] == "inv_1"
        flow.close()

    def test_verify_invalid(self):
        flow = Flow(api_key="test_key", webhook_secret="whsec_test123")
        with pytest.raises(InvalidSignatureError):
            flow.webhooks.verify('{"test": true}', "badsig")
        flow.close()

    def test_is_valid(self):
        secret = "whsec_test123"
        payload = '{"id": "evt_1", "type": "test"}'
        sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        flow = Flow(api_key="test_key", webhook_secret=secret)
        assert flow.webhooks.is_valid(payload, sig) is True
        assert flow.webhooks.is_valid(payload, "wrong") is False
        flow.close()


class TestErrors:
    @respx.mock
    def test_401(self):
        respx.get(f"{BASE}/invoices/x").mock(
            return_value=httpx.Response(401, json={"detail": "Invalid API key"})
        )
        with Flow(api_key="bad_key") as flow:
            with pytest.raises(AuthenticationError):
                flow.invoices.get("x")

    @respx.mock
    def test_404(self):
        respx.get(f"{BASE}/invoices/nonexistent").mock(
            return_value=httpx.Response(404, json={"detail": "Not found"})
        )
        with Flow(api_key="test_key") as flow:
            with pytest.raises(NotFoundError):
                flow.invoices.get("nonexistent")

    @respx.mock
    def test_429(self):
        respx.get(f"{BASE}/invoices/x").mock(
            return_value=httpx.Response(429, json={"detail": "Too many requests"}, headers={"Retry-After": "5"})
        )
        with Flow(api_key="test_key") as flow:
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
        async with AsyncFlow(api_key="test_key") as flow:
            inv = await flow.invoices.create(amount=200, currency="BTC", network="bitcoin")
            assert inv.id == "inv_async"
            assert inv.wallet_address == "bc1q..."
