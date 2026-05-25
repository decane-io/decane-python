# granthe

Official Python SDK for Granthe — institutional liquidity rail for crypto settlement.

[![PyPI](https://img.shields.io/pypi/v/granthe)](https://pypi.org/project/granthe/)
[![Python](https://img.shields.io/pypi/pyversions/granthe)](https://pypi.org/project/granthe/)

## Install

```bash
pip install granthe
```

## Quick Start

```python
from granthe import Granthe

granthe = Granthe(api_key="vf_live_...", webhook_secret="whsec_...")

# Create a payment invoice
invoice = granthe.invoices.create(
    amount=100.00,
    currency="USDT",
    network="tron",
    description="Premium Plan",
    customer_email="buyer@example.com",
)
print(f"Pay to: {invoice.wallet_address}")
print(f"Status: {invoice.status}")

# Request a payout
payout = granthe.payouts.create(
    amount=50.00,
    currency="USDT",
    network="tron",
    destination="TXyz...recipientAddress",
)
print(f"Payout ID: {payout.id}")
```

## Async Support

```python
from granthe import AsyncFlow

async with AsyncFlow(api_key="vf_live_...") as flow:
    invoice = await granthe.invoices.create(
        amount=100, currency="USDT", network="ethereum",
    )
```

## Resources

### Invoices

```python
# Create
invoice = granthe.invoices.create(amount=100, currency="USDT", network="tron")

# Get by ID
invoice = granthe.invoices.get("inv_abc123")

# List with filters
result = granthe.invoices.list(status="paid", page=1, limit=20)
for inv in result.items:
    print(inv.id, inv.amount, inv.status)

# Cancel
granthe.invoices.cancel("inv_abc123")
```

### Payouts

```python
# Single payout
payout = granthe.payouts.create(
    amount=50, currency="USDT", network="tron",
    destination="TXyz...addr",
)

# Batch payout
payouts = granthe.payouts.create_batch([
    {"amount": 50, "currency": "USDT", "network": "tron", "destination_address": "TXyz..."},
    {"amount": 25, "currency": "USDT", "network": "tron", "destination_address": "TAbc..."},
])

# Check status
payout = granthe.payouts.get("pout_abc123")
```

### Wallets

```python
# Generate a new deposit wallet
wallet = granthe.wallets.generate(network="ethereum", currency="USDT")
print(wallet.address)

# List wallets
result = granthe.wallets.list(network="tron")

# Check balance
wallet = granthe.wallets.balance("wal_abc123")
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
from granthe import Granthe, InvalidSignatureError

granthe = Granthe(api_key="vf_live_...", webhook_secret="whsec_...")

# In your webhook handler:
def handle_webhook(request):
    payload = request.body
    signature = request.headers["X-Granthe-Signature"]

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
from granthe import Granthe, FlowError, AuthenticationError, RateLimitError

granthe = Granthe(api_key="vf_live_...")

try:
    invoice = granthe.invoices.create(amount=100, currency="USDT", network="tron")
except AuthenticationError:
    print("Bad API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except FlowError as e:
    print(f"Error: {e.message} (code={e.code}, status={e.status})")
```

## Configuration

```python
granthe = Granthe(
    api_key="vf_live_...",
    webhook_secret="whsec_...",      # For webhook verification
    base_url="https://granthe.io/api/flow",  # Default
    timeout=30.0,                     # Request timeout in seconds
)
```

## Supported Networks

Bitcoin, Ethereum, Tron, BNB Chain, Solana, Ripple, Polygon, Avalanche, Dogecoin, Litecoin, TON, and more.

## License

MIT
