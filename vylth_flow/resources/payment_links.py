"""Payment link resource — create and manage hosted payment links."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP


class PaymentLinks:
    """Synchronous payment link operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def create(
        self,
        amount: float,
        currency: str,
        *,
        title: str | None = None,
        description: str | None = None,
        redirect_url: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"amount": amount, "currency": currency}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if redirect_url is not None:
            payload["redirect_url"] = redirect_url
        if metadata is not None:
            payload["metadata"] = metadata
        return self._http.post("/merchants/me/payment-links", json=payload)

    def list(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return self._http.get("/merchants/me/payment-links", params={"page": page, "limit": limit})

    def update(self, link_id: str, **fields: Any) -> dict[str, Any]:
        return self._http.patch(f"/merchants/me/payment-links/{link_id}", json=fields)

    def delete(self, link_id: str) -> None:
        self._http.delete(f"/merchants/me/payment-links/{link_id}")


class AsyncPaymentLinks:
    """Async payment link operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create(
        self,
        amount: float,
        currency: str,
        *,
        title: str | None = None,
        description: str | None = None,
        redirect_url: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"amount": amount, "currency": currency}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if redirect_url is not None:
            payload["redirect_url"] = redirect_url
        if metadata is not None:
            payload["metadata"] = metadata
        return await self._http.post("/merchants/me/payment-links", json=payload)

    async def list(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return await self._http.get("/merchants/me/payment-links", params={"page": page, "limit": limit})

    async def update(self, link_id: str, **fields: Any) -> dict[str, Any]:
        return await self._http.patch(f"/merchants/me/payment-links/{link_id}", json=fields)

    async def delete(self, link_id: str) -> None:
        await self._http.delete(f"/merchants/me/payment-links/{link_id}")
