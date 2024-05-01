from decimal import Decimal
import pytest
from unittest.mock import Mock, patch
from takehome.app import app
from takehome.models.card.Card import Card
from tests.resources.transaction import MOCK_TRANSACTIONS

PATCHED_CREATE_TRANSACTION = Mock()
PATCHED_GET_TRANSACTION = Mock()
EXPECTED_GET_TRANSACTIONS = [
    {
        "amount": "12.23",
        "approved": False,
        "card_id": 1,
        "category": 1234,
        "id": 1,
        "merchant": "test1",
    },
    {
        "amount": "12.23",
        "approved": True,
        "card_id": 2,
        "category": 1234,
        "id": 2,
        "merchant": "test2",
    },
]


@patch(
    "takehome.models.transaction.Transaction.Transaction.get", PATCHED_GET_TRANSACTION
)
def test_get_transactions(client):
    """Test happy path for get transaction"""
    PATCHED_GET_TRANSACTION.return_value = MOCK_TRANSACTIONS
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json == {"message": EXPECTED_GET_TRANSACTIONS}


@patch(
    "takehome.models.transaction.NewTransaction.NewTransaction.create",
    PATCHED_CREATE_TRANSACTION,
)
def test_create_transactions(client):
    """Test happy path for create transaction"""
    PATCHED_CREATE_TRANSACTION.return_value = True
    response = client.post(
        "/transactions",
        json={
            "merchant": "test_merchant",
            "merchant_category": "1234",
            "amount": "45.50",
            "card": "1",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Transaction approved."}


@patch(
    "takehome.models.transaction.NewTransaction.NewTransaction.create",
    PATCHED_CREATE_TRANSACTION,
)
def test_create_transactions_declined(client):
    """Test bad path for create transaction when declined"""
    PATCHED_CREATE_TRANSACTION.return_value = False
    response = client.post(
        "/transactions",
        json={
            "merchant": "test_merchant",
            "merchant_category": "1234",
            "amount": "45.50",
            "card": "1",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Transaction declined."}


@patch(
    "takehome.models.transaction.NewTransaction.NewTransaction.create",
    PATCHED_CREATE_TRANSACTION,
)
def test_create_transactions_invalid_json(client):
    """Test bad path for create transaction when invalid json passed"""
    PATCHED_CREATE_TRANSACTION.return_value = False
    malformed_res = {
        "message": "Malformed body data. Please supply the correct properties."
    }
    response = client.post(
        "/transactions",
        json={
            "merchant": "test_merchant",
            "merchant_category": "1234",
            "amount": "blah",
            "card": "1",
        },
    )
    assert response.status_code == 400
    assert response.json == malformed_res

    response = client.post(
        "/transactions",
        json={
            "merchant": "test_merchant",
            "merchant_category": "1234",
            "amount": "12.23",
        },
    )
    assert response.status_code == 400
    assert response.json == malformed_res
