"""Refund age limits from docs/proposal.md."""

from datetime import date, timedelta

import pytest

from app import rules


@pytest.mark.parametrize("age_days", [31, 45, 365])
def test_orders_more_than_30_days_old_are_outside_refund_window(age_days: int) -> None:
    today = date(2026, 1, 15)
    order_date = today - timedelta(days=age_days)

    assert rules.is_within_refund_window(order_date, today=today) is False


@pytest.mark.parametrize("age_days", [0, 29, 30])
def test_orders_up_to_30_days_old_are_within_refund_window(age_days: int) -> None:
    today = date(2026, 1, 15)
    order_date = today - timedelta(days=age_days)

    assert rules.is_within_refund_window(order_date, today=today) is True
