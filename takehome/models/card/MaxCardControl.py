from decimal import Decimal
from pydantic import BaseModel, validator
from typing import Generic, List, Optional, TypeVar

from takehome.models.card.CardControl import CardControl, ControlChoices


class MaxCardControl(CardControl[Decimal]):
    label: ControlChoices = ControlChoices.maximum

    @validator("value")
    def value_must_be_greater_than_zero(cls, v):
        assert v > 0
        return v

    def should_approve(self, transaction) -> bool:
        return self.value >= transaction.amount
