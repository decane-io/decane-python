"""Team resource — manage merchant team members and invites."""

from __future__ import annotations

from typing import Any

from .._internal.http import AsyncHTTP, SyncHTTP


class Teams:
    """Synchronous team operations."""

    def __init__(self, http: SyncHTTP):
        self._http = http

    def get(self) -> dict[str, Any]:
        return self._http.get("/merchants/me/team")

    def my_role(self) -> dict[str, Any]:
        return self._http.get("/merchants/me/team/my-role")

    def invite(self, email: str, role: str) -> dict[str, Any]:
        return self._http.post("/merchants/me/team/invite", json={"email": email, "role": role})

    def revoke_invite(self, invite_id: str) -> dict[str, Any]:
        return self._http.post(f"/merchants/me/team/invite/{invite_id}/revoke")

    def update_role(self, member_id: str, role: str) -> dict[str, Any]:
        return self._http.patch(f"/merchants/me/team/{member_id}/role", json={"role": role})

    def remove(self, member_id: str) -> None:
        self._http.delete(f"/merchants/me/team/{member_id}")


class AsyncTeams:
    """Async team operations."""

    def __init__(self, http: AsyncHTTP):
        self._http = http

    async def get(self) -> dict[str, Any]:
        return await self._http.get("/merchants/me/team")

    async def my_role(self) -> dict[str, Any]:
        return await self._http.get("/merchants/me/team/my-role")

    async def invite(self, email: str, role: str) -> dict[str, Any]:
        return await self._http.post("/merchants/me/team/invite", json={"email": email, "role": role})

    async def revoke_invite(self, invite_id: str) -> dict[str, Any]:
        return await self._http.post(f"/merchants/me/team/invite/{invite_id}/revoke")

    async def update_role(self, member_id: str, role: str) -> dict[str, Any]:
        return await self._http.patch(f"/merchants/me/team/{member_id}/role", json={"role": role})

    async def remove(self, member_id: str) -> None:
        await self._http.delete(f"/merchants/me/team/{member_id}")
