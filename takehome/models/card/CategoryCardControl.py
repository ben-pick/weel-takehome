from decimal import Decimal
from typing_extensions import Any
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

from takehome.models.card.CardControl import CardControl, ControlChoices


class CategoryCardControl(CardControl[int]):
    label: ControlChoices = ControlChoices.category

    def should_approve(self, transaction) -> bool:
        return self.value == transaction.category
