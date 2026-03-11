"""Swap resource — currency swaps between crypto assets."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP
from ..types import Swap, SwapQuote, PaginatedList


class Swaps:
    """Synchronous swap operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def quote(
        self,
        from_currency: str,
        to_currency: str,
        amount: float,
    ) -> SwapQuote:
        """Get a swap price quote."""
        data = self._http.post("/vendor/swap/quote", json={
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        })
        return SwapQuote.from_dict(data)

    def create(
        self,
        from_currency: str,
        to_currency: str,
        amount: float,
    ) -> Swap:
        """Execute a swap."""
        data = self._http.post("/vendor/swap", json={
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        })
        return Swap.from_dict(data)

    def get(self, swap_id: str) -> Swap:
        """Get a swap by ID."""
        data = self._http.get(f"/vendor/swap/{swap_id}")
        return Swap.from_dict(data)

    def list(self, *, page: int = 1, limit: int = 50) -> PaginatedList:
        """List swaps."""
        data = self._http.get("/vendor/swaps", params={"page": page, "limit": limit})
        return PaginatedList.from_dict(data, Swap)


class AsyncSwaps:
    """Async swap operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def quote(self, from_currency: str, to_currency: str, amount: float) -> SwapQuote:
        data = await self._http.post("/vendor/swap/quote", json={
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        })
        return SwapQuote.from_dict(data)

    async def create(self, from_currency: str, to_currency: str, amount: float) -> Swap:
        data = await self._http.post("/vendor/swap", json={
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        })
        return Swap.from_dict(data)

    async def get(self, swap_id: str) -> Swap:
        data = await self._http.get(f"/vendor/swap/{swap_id}")
        return Swap.from_dict(data)

    async def list(self, *, page: int = 1, limit: int = 50) -> PaginatedList:
        data = await self._http.get("/vendor/swaps", params={"page": page, "limit": limit})
        return PaginatedList.from_dict(data, Swap)
