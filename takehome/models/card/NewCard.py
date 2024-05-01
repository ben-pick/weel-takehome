from decimal import Decimal
from pydantic import BaseModel
import psycopg2
from takehome.models.card.Card import Card
from takehome.models.card.CardControl import CardControl
from takehome.models.conn import conn
from uuid import uuid4


class NewCard(BaseModel):
    name: str
    email: str
    balance: Decimal

    def create(self) -> bool:
        try:
            with conn:
                with conn.cursor() as curs:
                    curs.execute(
                        "INSERT INTO card ( name, email, balance) VALUES (%s, %s, %s)",
                        (self.name, self.email, self.balance),
                    )
        except psycopg2.Error as e:
            return False
        return True
