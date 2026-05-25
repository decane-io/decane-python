"""Payout resource — request and manage crypto payouts."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP
from ..types import Payout, PaginatedList


class Payouts:
    """Synchronous payout operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def create(
        self,
        amount: float,
        currency: str,
        network: str,
        recipient_address: str,
        *,
        reference_id: str | None = None,
    ) -> Payout:
        """Request a payout to an external wallet address."""
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
            "recipient_address": recipient_address,
        }
        if reference_id is not None:
            payload["reference_id"] = reference_id

        data = self._http.post("/vendor/payout", json=payload)
        return Payout.from_dict(data)

    def create_batch(
        self,
        payouts: list[dict[str, Any]],
        *,
        reference_id: str | None = None,
    ) -> list[Payout]:
        """Create multiple payouts in a single request.

        Each item should have: amount, currency, network, recipient_address.
        """
        body: dict[str, Any] = {"payouts": payouts}
        if reference_id is not None:
            body["reference_id"] = reference_id
        data = self._http.post("/vendor/payout/batch", json=body)
        items = data if isinstance(data, list) else data.get("payouts", data.get("items", []))
        return [Payout.from_dict(p) for p in items]

    def get(self, payout_id: str) -> Payout:
        """Get a payout by ID."""
        data = self._http.get(f"/vendor/query/payout/{payout_id}")
        return Payout.from_dict(data)

    def list(
        self,
        *,
        status: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        """List payouts with optional filters."""
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        data = self._http.get("/vendor/query/payouts", params=params)
        return PaginatedList.from_dict(data, Payout)


class AsyncPayouts:
    """Async payout operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create(
        self,
        amount: float,
        currency: str,
        network: str,
        recipient_address: str,
        *,
        reference_id: str | None = None,
    ) -> Payout:
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
            "recipient_address": recipient_address,
        }
        if reference_id is not None:
            payload["reference_id"] = reference_id

        data = await self._http.post("/vendor/payout", json=payload)
        return Payout.from_dict(data)

    async def create_batch(
        self,
        payouts: list[dict[str, Any]],
        *,
        reference_id: str | None = None,
    ) -> list[Payout]:
        body: dict[str, Any] = {"payouts": payouts}
        if reference_id is not None:
            body["reference_id"] = reference_id
        data = await self._http.post("/vendor/payout/batch", json=body)
        items = data if isinstance(data, list) else data.get("payouts", data.get("items", []))
        return [Payout.from_dict(p) for p in items]

    async def get(self, payout_id: str) -> Payout:
        data = await self._http.get(f"/vendor/query/payout/{payout_id}")
        return Payout.from_dict(data)

    async def list(
        self,
        *,
        status: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        data = await self._http.get("/vendor/query/payouts", params=params)
        return PaginatedList.from_dict(data, Payout)
