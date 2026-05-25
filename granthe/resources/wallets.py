"""Wallet resource — generate and manage deposit wallets."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP
from ..types import Wallet, PaginatedList


class Wallets:
    """Synchronous wallet operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def generate(
        self,
        network: str,
        currency: str,
        *,
        label: str | None = None,
    ) -> Wallet:
        """Generate a new deposit wallet for a specific network/currency."""
        payload: dict[str, Any] = {"network": network, "currency": currency}
        if label is not None:
            payload["label"] = label
        data = self._http.post("/wallets/generate", json=payload)
        return Wallet.from_dict(data)

    def get(self, wallet_id: str) -> Wallet:
        """Get a wallet by ID."""
        data = self._http.get(f"/wallets/{wallet_id}")
        return Wallet.from_dict(data)

    def list(
        self,
        *,
        network: str | None = None,
        currency: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        """List wallets with optional filters."""
        params: dict[str, Any] = {"page": page, "limit": limit}
        if network:
            params["network"] = network
        if currency:
            params["currency"] = currency
        data = self._http.get("/wallets", params=params)
        return PaginatedList.from_dict(data, Wallet)

    def balance(self, wallet_id: str) -> Wallet:
        """Get wallet with refreshed balance."""
        data = self._http.get(f"/wallets/{wallet_id}/balance")
        return Wallet.from_dict(data)


class AsyncWallets:
    """Async wallet operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def generate(
        self,
        network: str,
        currency: str,
        *,
        label: str | None = None,
    ) -> Wallet:
        payload: dict[str, Any] = {"network": network, "currency": currency}
        if label is not None:
            payload["label"] = label
        data = await self._http.post("/wallets/generate", json=payload)
        return Wallet.from_dict(data)

    async def get(self, wallet_id: str) -> Wallet:
        data = await self._http.get(f"/wallets/{wallet_id}")
        return Wallet.from_dict(data)

    async def list(
        self,
        *,
        network: str | None = None,
        currency: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> PaginatedList:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if network:
            params["network"] = network
        if currency:
            params["currency"] = currency
        data = await self._http.get("/wallets", params=params)
        return PaginatedList.from_dict(data, Wallet)

    async def balance(self, wallet_id: str) -> Wallet:
        data = await self._http.get(f"/wallets/{wallet_id}/balance")
        return Wallet.from_dict(data)
