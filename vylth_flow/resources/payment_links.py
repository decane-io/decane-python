"""Payment Links resource — create and manage shareable payment URLs."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP


class PaymentLinks:
    """Synchronous payment link operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def create(
        self,
        title: str,
        *,
        description: str | None = None,
        amount: float | None = None,
        currency: str = "USD",
        crypto_currency: str | None = None,
        network: str | None = None,
        redirect_url: str | None = None,
    ) -> dict[str, Any]:
        """Create a shareable payment link."""
        payload: dict[str, Any] = {"title": title, "currency": currency}
        if description is not None:
            payload["description"] = description
        if amount is not None:
            payload["amount"] = amount
        if crypto_currency is not None:
            payload["crypto_currency"] = crypto_currency
        if network is not None:
            payload["network"] = network
        if redirect_url is not None:
            payload["redirect_url"] = redirect_url
        return self._http.post("/merchants/me/payment-links", json=payload)

    def list(self, *, active: bool | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """List payment links."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if active is not None:
            params["active"] = active
        return self._http.get("/merchants/me/payment-links", params=params)

    def update(self, link_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a payment link."""
        return self._http.patch(f"/merchants/me/payment-links/{link_id}", json=kwargs)

    def delete(self, link_id: str) -> None:
        """Deactivate a payment link."""
        self._http.delete(f"/merchants/me/payment-links/{link_id}")


class AsyncPaymentLinks:
    """Async payment link operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create(self, title: str, *, description: str | None = None, amount: float | None = None, currency: str = "USD", crypto_currency: str | None = None, network: str | None = None, redirect_url: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"title": title, "currency": currency}
        if description is not None:
            payload["description"] = description
        if amount is not None:
            payload["amount"] = amount
        if crypto_currency is not None:
            payload["crypto_currency"] = crypto_currency
        if network is not None:
            payload["network"] = network
        if redirect_url is not None:
            payload["redirect_url"] = redirect_url
        return await self._http.post("/merchants/me/payment-links", json=payload)

    async def list(self, *, active: bool | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if active is not None:
            params["active"] = active
        return await self._http.get("/merchants/me/payment-links", params=params)

    async def update(self, link_id: str, **kwargs: Any) -> dict[str, Any]:
        return await self._http.patch(f"/merchants/me/payment-links/{link_id}", json=kwargs)

    async def delete(self, link_id: str) -> None:
        await self._http.delete(f"/merchants/me/payment-links/{link_id}")
