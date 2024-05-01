from decimal import Decimal
import psycopg2
from pydantic import BaseModel
from takehome.models.card.Card import Card
from takehome.models.conn import conn


class NewTransaction(BaseModel):
    merchant: str
    merchant_category: int
    amount: Decimal
    card: int

    def create(self) -> bool:
        cards: list[Card] = Card.get(id=self.card)
        if not cards:
            return False
        card = cards[0]
        approved_controls = [c for c in card.controls if c.should_approve(self)]
        approved = len(approved_controls) == len(card.controls)
        if not approved:
            return False
        try:
            with conn:
                with conn.cursor() as curs:
                    # Assume card can go negative
                    curs.execute(
                        "INSERT INTO transaction (merchant, category, amount, approved, card_id) VALUES (%s, %s, %s, %s, %s)",
                        (
                            self.merchant,
                            self.merchant_category,
                            self.amount,
                            approved,
                            card.id,
                        ),
                    )
                    curs.execute(
                        "UPDATE card SET balance = balance - %s WHERE id = %s",
                        (self.amount, card.id),
                    )

        except psycopg2.Error:
            return False
        return True
