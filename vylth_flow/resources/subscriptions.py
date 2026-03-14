"""Subscriptions resource — recurring billing plans and subscriber management."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP


class Subscriptions:
    """Synchronous subscription operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    # ── Plans ──

    def create_plan(
        self,
        name: str,
        amount: float,
        *,
        description: str | None = None,
        currency: str = "USD",
        interval_type: str = "monthly",
        interval_count: int = 1,
        trial_days: int = 0,
        max_subscribers: int | None = None,
        webhook_url: str | None = None,
    ) -> dict[str, Any]:
        """Create a subscription plan."""
        payload: dict[str, Any] = {
            "name": name,
            "amount": amount,
            "currency": currency,
            "interval_type": interval_type,
            "interval_count": interval_count,
            "trial_days": trial_days,
        }
        if description is not None:
            payload["description"] = description
        if max_subscribers is not None:
            payload["max_subscribers"] = max_subscribers
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        return self._http.post("/merchants/me/subscription-plans", json=payload)

    def list_plans(self, *, active: bool | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """List subscription plans."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if active is not None:
            params["active"] = active
        return self._http.get("/merchants/me/subscription-plans", params=params)

    def update_plan(self, plan_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a subscription plan."""
        return self._http.patch(f"/merchants/me/subscription-plans/{plan_id}", json=kwargs)

    def delete_plan(self, plan_id: str) -> None:
        """Deactivate a subscription plan."""
        self._http.delete(f"/merchants/me/subscription-plans/{plan_id}")

    # ── Subscribers ──

    def list_subscriptions(self, *, plan_id: str | None = None, status: str | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """List subscribers."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if plan_id is not None:
            params["plan_id"] = plan_id
        if status is not None:
            params["status"] = status
        return self._http.get("/merchants/me/subscriptions", params=params)

    def cancel_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Cancel a subscription."""
        return self._http.post(f"/merchants/me/subscriptions/{subscription_id}/cancel")

    # ── Stats ──

    def get_stats(self) -> dict[str, Any]:
        """Get subscription stats (MRR, churn, totals)."""
        return self._http.get("/merchants/me/subscriptions/stats")

    # ── Payments ──

    def list_payments(self, *, subscription_id: str | None = None, status: str | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """List subscription payments."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if subscription_id is not None:
            params["subscription_id"] = subscription_id
        if status is not None:
            params["status"] = status
        return self._http.get("/merchants/me/subscription-payments", params=params)


class AsyncSubscriptions:
    """Async subscription operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def create_plan(self, name: str, amount: float, *, description: str | None = None, currency: str = "USD", interval_type: str = "monthly", interval_count: int = 1, trial_days: int = 0, max_subscribers: int | None = None, webhook_url: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": name, "amount": amount, "currency": currency, "interval_type": interval_type, "interval_count": interval_count, "trial_days": trial_days}
        if description is not None:
            payload["description"] = description
        if max_subscribers is not None:
            payload["max_subscribers"] = max_subscribers
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        return await self._http.post("/merchants/me/subscription-plans", json=payload)

    async def list_plans(self, *, active: bool | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if active is not None:
            params["active"] = active
        return await self._http.get("/merchants/me/subscription-plans", params=params)

    async def update_plan(self, plan_id: str, **kwargs: Any) -> dict[str, Any]:
        return await self._http.patch(f"/merchants/me/subscription-plans/{plan_id}", json=kwargs)

    async def delete_plan(self, plan_id: str) -> None:
        await self._http.delete(f"/merchants/me/subscription-plans/{plan_id}")

    async def list_subscriptions(self, *, plan_id: str | None = None, status: str | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if plan_id is not None:
            params["plan_id"] = plan_id
        if status is not None:
            params["status"] = status
        return await self._http.get("/merchants/me/subscriptions", params=params)

    async def cancel_subscription(self, subscription_id: str) -> dict[str, Any]:
        return await self._http.post(f"/merchants/me/subscriptions/{subscription_id}/cancel")

    async def get_stats(self) -> dict[str, Any]:
        return await self._http.get("/merchants/me/subscriptions/stats")

    async def list_payments(self, *, subscription_id: str | None = None, status: str | None = None, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if subscription_id is not None:
            params["subscription_id"] = subscription_id
        if status is not None:
            params["status"] = status
        return await self._http.get("/merchants/me/subscription-payments", params=params)
