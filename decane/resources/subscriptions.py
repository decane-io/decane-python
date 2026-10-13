"""Subscription resource — plans, active subscriptions, and recurring payments."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP


class Subscriptions:
    """Synchronous subscription operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def create_plan(
        self,
        name: str,
        amount: float,
        currency: str,
        interval: str,
        *,
        interval_count: int = 1,
        description: str | None = None,
        trial_days: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": name,
            "amount": amount,
            "currency": currency,
            "interval": interval,
            "interval_count": interval_count,
        }
        if description is not None:
            payload["description"] = description
        if trial_days is not None:
            payload["trial_days"] = trial_days
        if metadata is not None:
            payload["metadata"] = metadata
        return self._http.post("/merchants/me/subscription-plans", json=payload)

    def list_plans(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return self._http.get("/merchants/me/subscription-plans", params={"page": page, "limit": limit})

    def update_plan(self, plan_id: str, **fields: Any) -> dict[str, Any]:
        return self._http.patch(f"/merchants/me/subscription-plans/{plan_id}", json=fields)

    def delete_plan(self, plan_id: str) -> None:
        self._http.delete(f"/merchants/me/subscription-plans/{plan_id}")

    def list(self, *, status: str | None = None, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        return self._http.get("/merchants/me/subscriptions", params=params)

    def cancel(self, subscription_id: str) -> dict[str, Any]:
        return self._http.post(f"/merchants/me/subscriptions/{subscription_id}/cancel")

    def stats(self) -> dict[str, Any]:
        return self._http.get("/merchants/me/subscriptions/stats")

    def list_payments(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return self._http.get("/merchants/me/subscription-payments", params={"page": page, "limit": limit})


class AsyncSubscriptions:
    """Async subscription operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create_plan(
        self,
        name: str,
        amount: float,
        currency: str,
        interval: str,
        *,
        interval_count: int = 1,
        description: str | None = None,
        trial_days: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": name,
            "amount": amount,
            "currency": currency,
            "interval": interval,
            "interval_count": interval_count,
        }
        if description is not None:
            payload["description"] = description
        if trial_days is not None:
            payload["trial_days"] = trial_days
        if metadata is not None:
            payload["metadata"] = metadata
        return await self._http.post("/merchants/me/subscription-plans", json=payload)

    async def list_plans(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return await self._http.get("/merchants/me/subscription-plans", params={"page": page, "limit": limit})

    async def update_plan(self, plan_id: str, **fields: Any) -> dict[str, Any]:
        return await self._http.patch(f"/merchants/me/subscription-plans/{plan_id}", json=fields)

    async def delete_plan(self, plan_id: str) -> None:
        await self._http.delete(f"/merchants/me/subscription-plans/{plan_id}")

    async def list(self, *, status: str | None = None, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        return await self._http.get("/merchants/me/subscriptions", params=params)

    async def cancel(self, subscription_id: str) -> dict[str, Any]:
        return await self._http.post(f"/merchants/me/subscriptions/{subscription_id}/cancel")

    async def stats(self) -> dict[str, Any]:
        return await self._http.get("/merchants/me/subscriptions/stats")

    async def list_payments(self, *, page: int = 1, limit: int = 50) -> list[dict[str, Any]]:
        return await self._http.get("/merchants/me/subscription-payments", params={"page": page, "limit": limit})
