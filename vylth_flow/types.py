"""Vylth Flow SDK data types."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class InvoiceStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    UNDERPAID = "underpaid"
    OVERPAID = "overpaid"


class PayoutStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SwapStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Invoice:
    """A payment invoice."""

    id: str
    merchant_id: str
    amount: float
    currency: str
    network: str
    status: InvoiceStatus
    wallet_address: str | None = None
    description: str | None = None
    customer_email: str | None = None
    callback_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    payment_url: str | None = None
    tx_hash: str | None = None
    paid_amount: float | None = None
    expires_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Invoice:
        return cls(
            id=data.get("id", ""),
            merchant_id=data.get("merchant_id", ""),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", ""),
            network=data.get("network", ""),
            status=InvoiceStatus(data.get("status", "pending")),
            wallet_address=data.get("wallet_address"),
            description=data.get("description"),
            customer_email=data.get("customer_email"),
            callback_url=data.get("callback_url"),
            metadata=data.get("metadata") or {},
            payment_url=data.get("payment_url"),
            tx_hash=data.get("tx_hash"),
            paid_amount=float(data["paid_amount"]) if data.get("paid_amount") else None,
            expires_at=data.get("expires_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _raw=data,
        )


@dataclass
class Payment:
    """A detected payment/deposit."""

    id: str
    invoice_id: str | None = None
    amount: float = 0
    currency: str = ""
    network: str = ""
    tx_hash: str | None = None
    from_address: str | None = None
    to_address: str | None = None
    confirmations: int = 0
    status: str = ""
    created_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Payment:
        return cls(
            id=data.get("id", ""),
            invoice_id=data.get("invoice_id"),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", ""),
            network=data.get("network", ""),
            tx_hash=data.get("tx_hash"),
            from_address=data.get("from_address"),
            to_address=data.get("to_address"),
            confirmations=int(data.get("confirmations", 0)),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            _raw=data,
        )


@dataclass
class Payout:
    """A vendor payout request."""

    id: str
    amount: float
    currency: str
    network: str
    destination: str
    status: PayoutStatus
    tx_hash: str | None = None
    fee: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    completed_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Payout:
        return cls(
            id=data.get("id", ""),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", ""),
            network=data.get("network", ""),
            destination=data.get("destination_address", data.get("destination", "")),
            status=PayoutStatus(data.get("status", "pending")),
            tx_hash=data.get("tx_hash"),
            fee=float(data["fee"]) if data.get("fee") else None,
            metadata=data.get("metadata") or {},
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
            _raw=data,
        )


@dataclass
class Wallet:
    """A deposit wallet."""

    id: str
    address: str
    network: str
    currency: str
    balance: float = 0
    label: str | None = None
    created_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Wallet:
        return cls(
            id=data.get("id", ""),
            address=data.get("address", ""),
            network=data.get("network", ""),
            currency=data.get("currency", ""),
            balance=float(data.get("balance", 0)),
            label=data.get("label"),
            created_at=data.get("created_at"),
            _raw=data,
        )


@dataclass
class SwapQuote:
    """A swap price quote."""

    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    rate: float
    expires_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SwapQuote:
        return cls(
            from_currency=data.get("from_currency", ""),
            to_currency=data.get("to_currency", ""),
            from_amount=float(data.get("from_amount", 0)),
            to_amount=float(data.get("to_amount", 0)),
            rate=float(data.get("rate", 0)),
            expires_at=data.get("expires_at"),
            _raw=data,
        )


@dataclass
class Swap:
    """A completed or pending swap."""

    id: str
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    rate: float
    status: SwapStatus
    tx_hash: str | None = None
    created_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Swap:
        return cls(
            id=data.get("id", ""),
            from_currency=data.get("from_currency", ""),
            to_currency=data.get("to_currency", ""),
            from_amount=float(data.get("from_amount", 0)),
            to_amount=float(data.get("to_amount", 0)),
            rate=float(data.get("rate", 0)),
            status=SwapStatus(data.get("status", "pending")),
            tx_hash=data.get("tx_hash"),
            created_at=data.get("created_at"),
            _raw=data,
        )


@dataclass
class WebhookEvent:
    """A verified webhook event."""

    id: str
    type: str
    data: dict[str, Any]
    created_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WebhookEvent:
        return cls(
            id=data.get("id", ""),
            type=data.get("type", data.get("event", "")),
            data=data.get("data", {}),
            created_at=data.get("created_at"),
            _raw=data,
        )


@dataclass
class PaginatedList:
    """A paginated list response."""

    items: list[Any]
    total: int
    page: int
    per_page: int
    has_more: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any], item_cls: type) -> PaginatedList:
        items_raw = data.get("items", data.get("data", data.get("results", [])))
        return cls(
            items=[item_cls.from_dict(i) for i in items_raw],
            total=int(data.get("total", len(items_raw))),
            page=int(data.get("page", 1)),
            per_page=int(data.get("per_page", data.get("limit", len(items_raw)))),
            has_more=bool(data.get("has_more", False)),
        )
