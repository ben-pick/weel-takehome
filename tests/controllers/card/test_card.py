from decimal import Decimal
import pytest
from unittest.mock import Mock, patch
from takehome.models.card.Card import Card
from tests.resources.card import MOCK_CARDS

EXPECTED_GET_CARDS = {
    "message": [
        {
            "id": 1,
            "name": "Ben",
            "email": "test_email@gmail.com",
            "balance": "1234",
            "controls": [],
        },
        {
            "id": 2,
            "name": "Ben2",
            "email": "test_email2@gmail.com",
            "balance": "4321",
            "controls": [
                {"card_id": 2, "value": 1234, "label": "category"},
                {"card_id": 2, "value": "test", "label": "merchant"},
            ],
        },
    ]
}
PATCHED_GET_CARD = Mock()
PATCHED_CREATE_CARD = Mock()


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
def test_get_card(client):
    """Tests happy path for get card"""
    PATCHED_GET_CARD.return_value = MOCK_CARDS
    response = client.get("/cards")
    assert response.json == EXPECTED_GET_CARDS


@patch("takehome.models.card.NewCard.NewCard.create", PATCHED_CREATE_CARD)
def test_create_card(client):
    """Happy path for creating card"""
    PATCHED_CREATE_CARD.return_value = True

    response = client.post(
        "/cards", json={"name": "test", "email": "test@email.com", "balance": "1000.00"}
    )
    assert response.json == {"message": "Card successfully created."}
    assert response.status_code == 200


@patch("takehome.models.card.NewCard.NewCard.create", PATCHED_CREATE_CARD)
def test_create_card_invalid_json(client):
    """Bad path for creating card with invalid json"""
    PATCHED_CREATE_CARD.return_value = True
    malformed_res = {
        "message": "Malformed body data. Please supply the correct properties."
    }
    response = client.post("/cards", json={"name": "test", "balance": "asdf"})
    assert response.json == malformed_res
    assert response.status_code == 400
    response = client.post("/cards", json={"name": "test", "balance": "1000.00"})
    assert response.json == malformed_res
    assert response.status_code == 400


@patch("takehome.models.card.NewCard.NewCard.create", PATCHED_CREATE_CARD)
def test_create_card_non_json(client):
    """Bad path for creating card with wrong data type"""
    PATCHED_CREATE_CARD.return_value = True
    malformed_res = {
        "message": "Malformed body data. Please supply the correct properties."
    }
    response = client.post(
        "/cards", data={"name": "test", "email": "test@email.com", "balance": "1000.00"}
    )
    assert response.status_code == 415


@patch("takehome.models.card.NewCard.NewCard.create", PATCHED_CREATE_CARD)
def test_create_card_unexpected_error(client):
    """Bad path for creating card with unexpected error"""
    PATCHED_CREATE_CARD.return_value = False
    response = client.post(
        "/cards", json={"name": "test", "email": "test@email.com", "balance": "1000.00"}
    )
    assert response.json == {"message": "Card failed to create."}

    assert response.status_code == 500
