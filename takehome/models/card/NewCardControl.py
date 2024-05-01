from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ValidationError
import psycopg2
from takehome.models.card.CardControl import CardControl, ControlChoices
from takehome.models.card.CardControlCreator import CardControlCreator
from takehome.models.conn import conn


class NewCardControl(BaseModel):
    card_id: int
    label: ControlChoices
    value: str | Decimal | int

    def create(self) -> bool:
        try:
            CardControlCreator.create(
                label=self.label, value=self.value, card_id=self.card_id
            )
            with conn:
                with conn.cursor() as curs:
                    curs.execute(
                        f"UPDATE card SET {self.label.value} = %s WHERE id = %s",
                        (self.value, self.card_id),
                    )
        except (psycopg2.Error, ValidationError) as e:
            return False
        return True
