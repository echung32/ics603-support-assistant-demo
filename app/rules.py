"""Refund business rules from docs/proposal.md."""

from datetime import date


def is_within_refund_window(order_date: date, *, today: date) -> bool:
    """Return whether the order is no more than 30 days old."""
    return (today - order_date).days <= 30
