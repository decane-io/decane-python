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
        destination: str,
        *,
        metadata: dict[str, Any] | None = None,
        callback_url: str | None = None,
    ) -> Payout:
        """Request a payout to an external wallet address."""
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
            "destination_address": destination,
        }
        if metadata is not None:
            payload["metadata"] = metadata
        if callback_url is not None:
            payload["callback_url"] = callback_url

        data = self._http.post("/vendor/payout", json=payload)
        return Payout.from_dict(data)

    def create_batch(
        self,
        payouts: list[dict[str, Any]],
    ) -> list[Payout]:
        """Create multiple payouts in a single request.

        Each item should have: amount, currency, network, destination_address.
        """
        data = self._http.post("/vendor/payout/batch", json={"payouts": payouts})
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
        destination: str,
        *,
        metadata: dict[str, Any] | None = None,
        callback_url: str | None = None,
    ) -> Payout:
        payload: dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "network": network,
            "destination_address": destination,
        }
        if metadata is not None:
            payload["metadata"] = metadata
        if callback_url is not None:
            payload["callback_url"] = callback_url

        data = await self._http.post("/vendor/payout", json=payload)
        return Payout.from_dict(data)

    async def create_batch(self, payouts: list[dict[str, Any]]) -> list[Payout]:
        data = await self._http.post("/vendor/payout/batch", json={"payouts": payouts})
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
