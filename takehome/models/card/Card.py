from decimal import Decimal
from enum import Enum
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

from takehome.models.card.CardControl import CardControl, ControlChoices
from takehome.models.card.CardControlCreator import CardControlCreator
from takehome.models.conn import conn


class Card(BaseModel):
    id: int
    name: str
    email: str
    balance: Decimal
    controls: list[CardControl]

    @staticmethod
    def get(id: int | None = None):
        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                    query = "SELECT * FROM card"
                    if id:
                        query = f"{query} WHERE id = %s"
                        curs.execute(
                            query,
                            str(id),
                        )
                    else:
                        curs.execute(query)
                    rows = curs.fetchall()
                    cards = []
                    for row in rows:
                        controls = []
                        for col in row:
                            try:
                                label = ControlChoices(col)
                                controls.append(
                                    CardControlCreator.create(
                                        label=label, value=row[col], card_id=row["id"]
                                    )
                                )
                            except ValueError as e:
                                pass
                        cards.append(
                            Card(
                                id=row["id"],
                                name=row["name"],
                                email=row["email"],
                                balance=row["balance"],
                                controls=controls,
                            )
                        )
                    return cards
        except psycopg2.Error:
            return []

    def delete_control(self, label: ControlChoices) -> bool:
        matching_choices = [c for c in self.controls if c.label == label]
        if not matching_choices:
            return False
        return matching_choices[0].delete()
