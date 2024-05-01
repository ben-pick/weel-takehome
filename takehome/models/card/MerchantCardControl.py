from decimal import Decimal
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

from takehome.models.card.CardControl import CardControl, ControlChoices


class MerchantCardControl(CardControl[str]):
    label: ControlChoices = ControlChoices.merchant

    def should_approve(self, transaction) -> bool:
        return self.value == transaction.merchant
