from decimal import Decimal
import psycopg2
from pydantic import BaseModel
from takehome.models.conn import conn


class Transaction(BaseModel):
    id: int
    merchant: str
    category: int
    amount: Decimal
    approved: bool
    card_id: int

    @staticmethod
    def get():
        try:
            with conn:
                with conn.cursor() as curs:
                    curs.execute(
                        "SELECT id, merchant, category, amount, approved, card_id FROM transaction"
                    )
                    rows = curs.fetchall()
                    transactions = []
                    for row in rows:
                        [id, merchant, category, amount, approved, card_id] = row
                        transactions.append(
                            Transaction(
                                id=id,
                                merchant=merchant,
                                category=category,
                                amount=amount,
                                approved=approved,
                                card_id=card_id,
                            )
                        )
                    return transactions
        except psycopg2.Error as e:
            return []
