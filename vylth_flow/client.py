"""Vylth Flow client — the main entry point for the SDK."""

from __future__ import annotations

from ._internal.http import AsyncHTTP, SyncHTTP, DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from .resources.invoices import AsyncInvoices, Invoices
from .resources.payouts import AsyncPayouts, Payouts
from .resources.swaps import AsyncSwaps, Swaps
from .resources.wallets import AsyncWallets, Wallets
from .resources.webhooks import Webhooks


class Flow:
    """Synchronous Vylth Flow client.

    Usage::

        from vylth_flow import Flow

        flow = Flow(api_key="vf_live_...", webhook_secret="whsec_...")

        # Create an invoice
        invoice = flow.invoices.create(
            amount=100, currency="USDT", network="tron",
        )
        print(invoice.wallet_address)

        # Request a payout
        payout = flow.payouts.create(
            amount=50, currency="USDT", network="tron",
            destination="TXyz...addr",
        )

        # Verify a webhook
        event = flow.webhooks.verify(payload, signature)
    """

    def __init__(
        self,
        api_key: str,
        *,
        webhook_secret: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if not api_key:
            raise ValueError("api_key is required")

        self._http = SyncHTTP(api_key=api_key, base_url=base_url, timeout=timeout)

        self.invoices = Invoices(self._http)
        self.payouts = Payouts(self._http)
        self.wallets = Wallets(self._http)
        self.swaps = Swaps(self._http)
        self.webhooks = Webhooks(webhook_secret or "")

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> Flow:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return "Flow(connected)"


class AsyncFlow:
    """Async Vylth Flow client.

    Usage::

        from vylth_flow import AsyncFlow

        async with AsyncFlow(api_key="vf_live_...") as flow:
            invoice = await flow.invoices.create(
                amount=100, currency="USDT", network="tron",
            )
    """

    def __init__(
        self,
        api_key: str,
        *,
        webhook_secret: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if not api_key:
            raise ValueError("api_key is required")

        self._http = AsyncHTTP(api_key=api_key, base_url=base_url, timeout=timeout)

        self.invoices = AsyncInvoices(self._http)
        self.payouts = AsyncPayouts(self._http)
        self.wallets = AsyncWallets(self._http)
        self.swaps = AsyncSwaps(self._http)
        self.webhooks = Webhooks(webhook_secret or "")

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncFlow:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    def __repr__(self) -> str:
        return "AsyncFlow(connected)"
