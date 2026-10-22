"""Request and output models; agent integration is deferred."""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """A customer's question."""

    question: str


class Refund(BaseModel):
    """A refund proposal and its outcome."""

    order_id: str
    amount: Decimal
    reason: str
    status: Literal["approved", "pending_review", "rejected"]


class ChatResponse(BaseModel):
    """An answer with an optional refund."""

    answer: str
    refund: Refund | None = None
