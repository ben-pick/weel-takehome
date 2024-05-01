from decimal import Decimal
from takehome.models.transaction.Transaction import Transaction

MOCK_TRANSACTIONS = [
    Transaction(
        id=1,
        merchant="test1",
        category=1234,
        amount=Decimal("12.23"),
        approved=False,
        card_id=1,
    ),
    Transaction(
        id=2,
        merchant="test2",
        category=1234,
        amount=Decimal("12.23"),
        approved=True,
        card_id=2,
    ),
]
