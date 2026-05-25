"""Granthe SDK data types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class InvoiceStatus(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    CONFIRMING = "confirming"
    COMPLETED = "completed"
    EXPIRED = "expired"
    UNDERPAID = "underpaid"
    OVERPAID = "overpaid"
    FAILED = "failed"


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
    amount: float           # fiat_amount from API
    currency: str           # fiat_currency from API
    status: InvoiceStatus
    # Optional fields
    network: str | None = None
    crypto_currency: str | None = None
    crypto_amount: float | None = None
    wallet_address: str | None = None   # deposit_address from API
    customer_email: str | None = None
    customer_name: str | None = None
    merchant_order_id: str | None = None
    callback_url: str | None = None
    return_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    payment_url: str | None = None
    tx_hash: str | None = None
    paid_amount: float | None = None    # received_amount from API
    confirmations: int = 0
    required_confirmations: int = 0
    expires_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Invoice:
        raw_status = data.get("status", "created")
        try:
            status = InvoiceStatus(raw_status)
        except ValueError:
            status = InvoiceStatus.CREATED
        return cls(
            id=data.get("id", ""),
            merchant_id=data.get("merchant_id", ""),
            amount=float(data.get("fiat_amount", data.get("amount", 0))),
            currency=data.get("fiat_currency", data.get("currency", "")),
            status=status,
            network=data.get("network"),
            crypto_currency=data.get("crypto_currency"),
            crypto_amount=float(data["crypto_amount"]) if data.get("crypto_amount") else None,
            wallet_address=data.get("deposit_address", data.get("wallet_address")),
            customer_email=data.get("customer_email"),
            customer_name=data.get("customer_name"),
            merchant_order_id=data.get("merchant_order_id"),
            callback_url=data.get("callback_url"),
            return_url=data.get("return_url"),
            metadata=data.get("metadata") or {},
            payment_url=data.get("payment_url"),
            tx_hash=data.get("tx_hash"),
            paid_amount=float(data["received_amount"]) if data.get("received_amount") else None,
            confirmations=int(data.get("confirmations", 0)),
            required_confirmations=int(data.get("required_confirmations", 0)),
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
    network: str
    currency: str
    status: str
    gross_amount: float = 0
    net_amount: float = 0
    fee_amount: float = 0
    nmc_amount: float | None = None
    recipient_address: str = ""
    reference_id: str | None = None
    batch_id: str | None = None
    tx_hash: str | None = None
    error_message: str | None = None
    created_at: str | None = None
    completed_at: str | None = None
    _raw: dict[str, Any] = field(default_factory=dict, repr=False)

    # Convenience aliases
    @property
    def amount(self) -> float:
        return self.gross_amount

    @property
    def destination(self) -> str:
        return self.recipient_address

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Payout:
        return cls(
            id=data.get("id", ""),
            network=data.get("network", ""),
            currency=data.get("currency", ""),
            status=data.get("status", "pending"),
            gross_amount=float(data.get("gross_amount", data.get("amount", 0))),
            net_amount=float(data.get("net_amount", 0)),
            fee_amount=float(data.get("fee_amount", data.get("fee", 0))),
            nmc_amount=float(data["nmc_amount"]) if data.get("nmc_amount") else None,
            recipient_address=data.get("recipient_address", data.get("destination_address", "")),
            reference_id=data.get("reference_id"),
            batch_id=data.get("batch_id"),
            tx_hash=data.get("tx_hash"),
            error_message=data.get("error_message"),
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
            type=data.get("event", data.get("type", "")),
            data=data.get("data", {}),
            created_at=data.get("timestamp", data.get("created_at")),
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
