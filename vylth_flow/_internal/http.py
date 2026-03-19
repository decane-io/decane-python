"""HTTP transport layer for Vylth Flow SDK."""

from __future__ import annotations

import time
from typing import Any

import httpx

from ..errors import (
    AuthenticationError,
    FlowError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

DEFAULT_BASE_URL = "https://flow.vylth.com/api/flow/"
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_STATUSES = {429, 500, 502, 503, 504}


def _build_headers(api_key: str, api_secret: str | None = None) -> dict[str, str]:
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "vylth-flow-python/0.4.0",
    }
    if api_secret:
        headers["X-API-Secret"] = api_secret
    return headers


def _raise_for_status(response: httpx.Response) -> None:
    """Raise typed SDK errors from HTTP responses."""
    if response.status_code < 400:
        return

    try:
        body = response.json()
    except Exception:
        body = {"detail": response.text}

    message = body.get("detail", body.get("message", body.get("error", str(body))))
    code = body.get("code")

    if response.status_code == 401:
        raise AuthenticationError(message)
    if response.status_code == 404:
        raise NotFoundError(message)
    if response.status_code == 422:
        raise ValidationError(message, errors=body.get("errors"))
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        raise RateLimitError(message, retry_after=float(retry_after) if retry_after else None)
    if response.status_code >= 500:
        raise ServerError(message)

    raise FlowError(message, code=code, status=response.status_code)


class SyncHTTP:
    """Synchronous HTTP client with retry logic."""

    def __init__(self, api_key: str, base_url: str, timeout: float, api_secret: str | None = None):
        self._client = httpx.Client(
            base_url=base_url,
            headers=_build_headers(api_key, api_secret),
            timeout=timeout,
        )

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self._client.request(method, path, **kwargs)
                if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES - 1:
                    wait = (2**attempt) * 0.5
                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            wait = float(retry_after)
                    time.sleep(wait)
                    continue
                _raise_for_status(response)
                if response.status_code == 204:
                    return None
                return response.json()
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exc = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep((2**attempt) * 0.5)
                    continue
                raise FlowError(f"Connection error: {e}", code="network_error") from e
        if last_exc:
            raise FlowError(f"Max retries exceeded: {last_exc}", code="network_error") from last_exc
        raise FlowError("Unexpected error", code="unknown")

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._client.close()


class AsyncHTTP:
    """Async HTTP client with retry logic."""

    def __init__(self, api_key: str, base_url: str, timeout: float, api_secret: str | None = None):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=_build_headers(api_key, api_secret),
            timeout=timeout,
        )

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        import asyncio

        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                response = await self._client.request(method, path, **kwargs)
                if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES - 1:
                    wait = (2**attempt) * 0.5
                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            wait = float(retry_after)
                    await asyncio.sleep(wait)
                    continue
                _raise_for_status(response)
                if response.status_code == 204:
                    return None
                return response.json()
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exc = e
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep((2**attempt) * 0.5)
                    continue
                raise FlowError(f"Connection error: {e}", code="network_error") from e
        if last_exc:
            raise FlowError(f"Max retries exceeded: {last_exc}", code="network_error") from last_exc
        raise FlowError("Unexpected error", code="unknown")

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        await self._client.aclose()
