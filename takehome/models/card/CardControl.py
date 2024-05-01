from decimal import Decimal
from enum import Enum
import psycopg2
from typing_extensions import Any
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar
from takehome.models.conn import conn


class ControlChoices(str, Enum):
    merchant = "merchant"
    category = "category"
    minimum = "minimum"
    maximum = "maximum"


T = TypeVar("T", bound=str | Decimal | int)


class CardControl(BaseModel, Generic[T]):
    value: T
    label: ControlChoices
    card_id: int

    def should_approve(self, transaction) -> bool:
        return False

    def delete(self) -> bool:
        try:
            with conn:
                with conn.cursor() as curs:
                    curs.execute(
                        f"UPDATE card SET {self.label.value} = NULL WHERE id = %s",
                        (self.card_id,),
                    )
        except psycopg2.Error as e:
            return False
        return True
