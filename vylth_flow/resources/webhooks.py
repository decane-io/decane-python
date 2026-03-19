"""Webhook verification — verify incoming webhook signatures."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from ..errors import InvalidSignatureError
from ..types import WebhookEvent


class Webhooks:
    """Webhook signature verification. Works with both sync and async clients."""

    def __init__(self, secret: str):
        self._secret = secret

    def verify(self, payload: str | bytes, signature: str) -> WebhookEvent:
        """Verify a webhook signature and return the parsed event.

        Args:
            payload: The raw request body (string or bytes).
            signature: The value of the X-Flow-Signature header.

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
