# vylth-flow

Official Python SDK for **Vylth Flow** — self-custody crypto payment processing.

[![PyPI](https://img.shields.io/pypi/v/vylth-flow)](https://pypi.org/project/vylth-flow/)
[![Python](https://img.shields.io/pypi/pyversions/vylth-flow)](https://pypi.org/project/vylth-flow/)

## Install

```bash
pip install vylth-flow
```

## Quick Start

```python
from vylth_flow import Flow

flow = Flow(api_key="vf_live_...", webhook_secret="whsec_...")

# Create a payment invoice
invoice = flow.invoices.create(
    amount=100.00,
    currency="USDT",
    network="tron",
    description="Premium Plan",
    customer_email="buyer@example.com",
)
print(f"Pay to: {invoice.wallet_address}")
print(f"Status: {invoice.status}")

# Request a payout
payout = flow.payouts.create(
    amount=50.00,
    currency="USDT",
    network="tron",
    destination="TXyz...recipientAddress",
)
print(f"Payout ID: {payout.id}")
```

## Async Support

```python
from vylth_flow import AsyncFlow

async with AsyncFlow(api_key="vf_live_...") as flow:
    invoice = await flow.invoices.create(
        amount=100, currency="USDT", network="ethereum",
    )
```

## Resources

### Invoices

```python
# Create
invoice = flow.invoices.create(amount=100, currency="USDT", network="tron")

# Get by ID
invoice = flow.invoices.get("inv_abc123")

# List with filters
result = flow.invoices.list(status="paid", page=1, limit=20)
for inv in result.items:
    print(inv.id, inv.amount, inv.status)

# Cancel
flow.invoices.cancel("inv_abc123")
```

### Payouts

```python
# Single payout
payout = flow.payouts.create(
    amount=50, currency="USDT", network="tron",
    destination="TXyz...addr",
)

# Batch payout
payouts = flow.payouts.create_batch([
    {"amount": 50, "currency": "USDT", "network": "tron", "destination_address": "TXyz..."},
    {"amount": 25, "currency": "USDT", "network": "tron", "destination_address": "TAbc..."},
])

# Check status
payout = flow.payouts.get("pout_abc123")
```

### Wallets

```python
# Generate a new deposit wallet
wallet = flow.wallets.generate(network="ethereum", currency="USDT")
print(wallet.address)

# List wallets
result = flow.wallets.list(network="tron")

# Check balance
wallet = flow.wallets.balance("wal_abc123")
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
from vylth_flow import Flow, InvalidSignatureError

flow = Flow(api_key="vf_live_...", webhook_secret="whsec_...")

# In your webhook handler:
def handle_webhook(request):
    payload = request.body
    signature = request.headers["X-Flow-Signature"]

    try:
        event = flow.webhooks.verify(payload, signature)
    except InvalidSignatureError:
        return {"error": "Invalid signature"}, 400

    if event.type == "invoice.paid":
        invoice_id = event.data["id"]
        print(f"Invoice {invoice_id} paid!")

    return {"status": "ok"}
```

## Error Handling

```python
from vylth_flow import Flow, FlowError, AuthenticationError, RateLimitError

flow = Flow(api_key="vf_live_...")

try:
    invoice = flow.invoices.create(amount=100, currency="USDT", network="tron")
except AuthenticationError:
    print("Bad API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except FlowError as e:
    print(f"Error: {e.message} (code={e.code}, status={e.status})")
```

## Configuration

```python
flow = Flow(
    api_key="vf_live_...",
    webhook_secret="whsec_...",      # For webhook verification
    base_url="https://flow.vylth.com/api/flow",  # Default
    timeout=30.0,                     # Request timeout in seconds
)
```

## Supported Networks

Bitcoin, Ethereum, Tron, BNB Chain, Solana, Ripple, Polygon, Avalanche, Dogecoin, Litecoin, TON, and more.

## License

MIT
