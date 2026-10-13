"""Webhook verification — verify incoming webhook signatures."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

from ..errors import InvalidSignatureError
from ..types import WebhookEvent


class Webhooks:
    """Webhook signature verification. Works with both sync and async clients."""

    def __init__(self, secret: str):
        self._secret = secret

    def verify(self, payload: str | bytes, signature: str) -> WebhookEvent:
        """Verify a legacy webhook signature and return the parsed event.

        .. deprecated::
            This checks the legacy ``X-Decane-Signature`` header, which has no
            timestamp and so allows replays. Use :meth:`verify_signature` or
            :meth:`construct_event` with the ``Decane-Signature`` header.

        Args:
            payload: The raw request body (string or bytes).
            signature: The value of the X-Decane-Signature header.

        Returns:
            A verified WebhookEvent.

        Raises:
            InvalidSignatureError: If the signature doesn't match.
        """
        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        expected = "sha256=" + hmac.new(
            self._secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected, signature):
            raise InvalidSignatureError()

        data = json.loads(payload)
        return WebhookEvent.from_dict(data)

    def is_valid(self, payload: str | bytes, signature: str) -> bool:
        """Check if a webhook signature is valid without raising.

        Returns:
            True if valid, False otherwise.
        """
        try:
            self.verify(payload, signature)
            return True
        except InvalidSignatureError:
            return False

    def verify_signature(
        self,
        payload: str | bytes,
        header: str,
        tolerance: int = 300,
    ) -> bool:
        """Verify a ``Decane-Signature`` header (``t=<unix>,v1=<hex>``).

        The signed message is ``"<t>."`` followed by the raw body. Returns False
        if the header is malformed, the timestamp is more than ``tolerance``
        seconds from now, or no ``v1`` value matches.

        Args:
            payload: The raw request body (string or bytes), exactly as received.
            header: The value of the Decane-Signature header.
            tolerance: Maximum age of the timestamp in seconds. Default 300.
        """
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if not header:
            return False

        timestamp: int | None = None
        candidates: list[str] = []
        for part in header.split(","):
            key, sep, value = part.strip().partition("=")
            if not sep:
                continue
            key, value = key.strip(), value.strip()
            if key == "t":
                try:
                    timestamp = int(value)
                except ValueError:
                    return False
            elif key == "v1":
                candidates.append(value)
        if timestamp is None or not candidates:
            return False
        if abs(time.time() - timestamp) > tolerance:
            return False

        expected = hmac.new(
            self._secret.encode("utf-8"),
            str(timestamp).encode("ascii") + b"." + payload,
            hashlib.sha256,
        ).hexdigest()
        return any(hmac.compare_digest(expected, c) for c in candidates)

    def construct_event(
        self,
        payload: str | bytes,
        header: str,
        tolerance: int = 300,
    ) -> WebhookEvent:
        """Verify a ``Decane-Signature`` header and return the parsed event.

        Raises:
            InvalidSignatureError: If verification fails.
        """
        if not self.verify_signature(payload, header, tolerance):
            raise InvalidSignatureError()
        return WebhookEvent.from_dict(json.loads(payload))
