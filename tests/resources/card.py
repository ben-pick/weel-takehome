from decimal import Decimal

from takehome.models.card.Card import Card
from takehome.models.card.CategoryCardControl import CategoryCardControl
from takehome.models.card.MerchantCardControl import MerchantCardControl

from takehome.models.transaction.Transaction import Transaction

MOCK_CARDS = [
    Card(
        id=1,
        name="Ben",
        email="test_email@gmail.com",
        balance=Decimal("1234"),
        controls=[],
    ),
    Card(
        id=2,
        name="Ben2",
        email="test_email2@gmail.com",
        balance=Decimal("4321"),
        controls=[
            CategoryCardControl(card_id=2, value=1234),
            MerchantCardControl(card_id=2, value="test"),
        ],
    ),
]
