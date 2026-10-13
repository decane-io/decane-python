# decane-sdk

Official Python SDK for Decane — institutional liquidity rail for crypto settlement.

> **Renamed from granthe.** The old package was `granthe` on PyPI. The API and webhook formats are unchanged, and the server still sends `Granthe-Signature` (and `X-Granthe-Signature`) for older integrations. Read `Decane-Signature` first and fall back to `Granthe-Signature` if you handle both.

[![PyPI](https://img.shields.io/pypi/v/decane-sdk)](https://pypi.org/project/decane-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/decane-sdk)](https://pypi.org/project/decane-sdk/)

## Install

```bash
pip install decane-sdk
```

## Quick Start

```python
from decane import Decane

decane = Decane(api_key="gr_...", webhook_secret="gr_whsec_...")

# Create a payment invoice
invoice = decane.invoices.create(
    amount=100.00,
    crypto_currency="USDT",
    network="tron",
    description="Premium Plan",
    customer_email="buyer@example.com",
    idempotency_key="order-1042",  # optional, safe to retry
)
print(f"Pay to: {invoice.wallet_address}")
print(f"Status: {invoice.status}")

# Request a payout
payout = decane.payouts.create(
    amount=50.00,
    currency="USDT",
    network="tron",
    recipient_address="TXyz...recipientAddress",
    idempotency_key="payout-1042",  # optional, safe to retry
)
print(f"Payout ID: {payout.id}")
```

## Async Support

```python
from decane import AsyncFlow

async with AsyncFlow(api_key="gr_...") as flow:
    invoice = await decane.invoices.create(
        amount=100, crypto_currency="USDT", network="ethereum",
    )
```

## Resources

### Invoices

```python
# Create
invoice = decane.invoices.create(amount=100, crypto_currency="USDT", network="tron")

# Get by ID
invoice = decane.invoices.get("inv_abc123")

# List with filters
result = decane.invoices.list(status="paid", page=1, limit=20)
for inv in result.items:
    print(inv.id, inv.amount, inv.status)

# Cancel
decane.invoices.cancel("inv_abc123")
```

### Payouts

```python
# Single payout
payout = decane.payouts.create(
    amount=50, currency="USDT", network="tron",
    recipient_address="TXyz...addr",
)

# Batch payout
payouts = decane.payouts.create_batch([
    {"amount": 50, "currency": "USDT", "network": "tron", "recipient_address": "TXyz..."},
    {"amount": 25, "currency": "USDT", "network": "tron", "recipient_address": "TAbc..."},
])

# Check status
payout = decane.payouts.get("pout_abc123")
```

### Wallets

```python
# Generate a new deposit wallet
wallet = decane.wallets.generate(network="ethereum", currency="USDT")
print(wallet.address)

# List wallets
result = decane.wallets.list(network="tron")

# Check balance
wallet = decane.wallets.balance("wal_abc123")
```

### Swaps

```python
# Get a quote
quote = flow.swaps.quote("BTC", "USDT", amount=0.01)
print(f"Rate: {quote.rate}, You get: {quote.to_amount} USDT")

# Execute swap
swap = flow.swaps.create("BTC", "USDT", amount=0.01)
```

### Webhooks

```python
from decane import Decane, InvalidSignatureError

decane = Decane(api_key="gr_...", webhook_secret="gr_whsec_...")

# In your webhook handler. Use the raw body, not re-serialized JSON.
def handle_webhook(request):
    payload = request.body
    header = request.headers.get("Decane-Signature") or request.headers["Granthe-Signature"]  # t=<unix>,v1=<hex>

    try:
        event = decane.webhooks.construct_event(payload, header, tolerance=300)
    except InvalidSignatureError:
        return {"error": "Invalid signature"}, 400

    # X-Decane-Delivery is the same on every retry, so use it to drop duplicates.
    if event.type == "invoice.completed":
        invoice_id = event.data["id"]
        print(f"Invoice {invoice_id} completed!")

    return {"status": "ok"}
```

`decane.webhooks.verify_signature(payload, header)` returns a bool if you want to parse the body yourself. The old `webhooks.verify(payload, signature)` for `X-Decane-Signature` (or `X-Granthe-Signature`) still works but is deprecated, because it has no timestamp check.

## Error Handling

```python
from decane import Decane, DecaneError, AuthenticationError, RateLimitError

decane = Decane(api_key="gr_...")

try:
    invoice = decane.invoices.create(amount=100, crypto_currency="USDT", network="tron")
except AuthenticationError:
    print("Bad API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except DecaneError as e:
    print(f"Error: {e.message} (code={e.code}, status={e.status})")
```

## Configuration

```python
decane = Decane(
    api_key="gr_...",
    webhook_secret="gr_whsec_...",      # For webhook verification
    base_url="https://api.decane.io/api/v1",  # Default
    timeout=30.0,                     # Request timeout in seconds
)
```

## Supported Networks

Bitcoin, Ethereum, Tron, BNB Chain, Solana, Ripple, Polygon, Avalanche, Dogecoin, Litecoin, TON, and more.

## License

MIT
