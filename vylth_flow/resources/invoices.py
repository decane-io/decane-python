"""Invoice resource — create and manage payment invoices."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP
from ..types import Invoice, PaginatedList


class Invoices:
    """Synchronous invoice operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def create(
        self,
        amount: float,
        currency: str,
        network: str,
        *,
        description: str | None = None,
        customer_email: str | None = None,
        callback_url: str | None = None,
        metadata: dict[str, Any] | None = None,
        expiry_minutes: int | None = None,
    ) -> Invoice:
        """Create a payment invoice. Returns an Invoice with wallet address and QR code URL."""
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
        }
        if description is not None:
            payload["description"] = description
        if customer_email is not None:
            payload["customer_email"] = customer_email
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if metadata is not None:
            payload["metadata"] = metadata
        if expiry_minutes is not None:
            payload["expiry_minutes"] = expiry_minutes

        data = self._http.post("/invoices", json=payload)
        return Invoice.from_dict(data)

    def get(self, invoice_id: str) -> Invoice:
        """Get an invoice by ID."""
        data = self._http.get(f"/invoices/{invoice_id}")
        return Invoice.from_dict(data)

    def list(
        self,
        *,
        status: str | None = None,
        currency: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        """List invoices with optional filters."""
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if currency:
            params["currency"] = currency
        data = self._http.get("/invoices", params=params)
        return PaginatedList.from_dict(data, Invoice)

    def cancel(self, invoice_id: str) -> Invoice:
        """Cancel a pending invoice."""
        data = self._http.post(f"/invoices/{invoice_id}/cancel")
        return Invoice.from_dict(data)


class AsyncInvoices:
    """Async invoice operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create(
        self,
        amount: float,
        currency: str,
        network: str,
        *,
        description: str | None = None,
        customer_email: str | None = None,
        callback_url: str | None = None,
        metadata: dict[str, Any] | None = None,
        expiry_minutes: int | None = None,
    ) -> Invoice:
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
        }
        if description is not None:
            payload["description"] = description
        if customer_email is not None:
            payload["customer_email"] = customer_email
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if metadata is not None:
            payload["metadata"] = metadata
        if expiry_minutes is not None:
            payload["expiry_minutes"] = expiry_minutes

        data = await self._http.post("/invoices", json=payload)
        return Invoice.from_dict(data)

    async def get(self, invoice_id: str) -> Invoice:
        data = await self._http.get(f"/invoices/{invoice_id}")
        return Invoice.from_dict(data)

    async def list(
        self,
        *,
        status: str | None = None,
        currency: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if currency:
            params["currency"] = currency
        data = await self._http.get("/invoices", params=params)
        return PaginatedList.from_dict(data, Invoice)

    async def cancel(self, invoice_id: str) -> Invoice:
        data = await self._http.post(f"/invoices/{invoice_id}/cancel")
        return Invoice.from_dict(data)
