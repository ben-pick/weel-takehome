from decimal import Decimal
import pytest
from unittest.mock import Mock, patch
from takehome.app import app
from takehome.models.card.Card import Card
from tests.resources.card import MOCK_CARDS

EXPECTED_GET_CARD_CONTROLS = [
    {"card_id": 2, "label": "category", "value": 1234},
    {"card_id": 2, "label": "merchant", "value": "test"},
]
PATCHED_GET_CARD = Mock()
PATCHED_CREATE_CARD_CONTROL = Mock()
PATCHED_DELETE_CARD_CONTROL = Mock()


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
def test_get_card_controls(client):
    """Tests happy path for get card controls"""
    PATCHED_GET_CARD.return_value = MOCK_CARDS
    response = client.get("/card-controls")
    assert response.json == EXPECTED_GET_CARD_CONTROLS


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
@patch(
    "takehome.models.card.NewCardControl.NewCardControl.create",
    PATCHED_CREATE_CARD_CONTROL,
)
def test_create_card_control(client):
    """Tests happy path for create card control"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[0]]
    PATCHED_CREATE_CARD_CONTROL.return_value = True
    response = client.post(
        "/card-controls", json={"label": "minimum", "value": 1234, "card_id": 1}
    )
    assert response.json == {"message": "Card control added to card."}
    assert response.status_code == 200


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
def test_create_card_control_card_not_found(client):
    """Tests bad path for create card control when card is not found"""
    PATCHED_GET_CARD.return_value = []
    response = client.post(
        "/card-controls", json={"label": "minimum", "value": 1234, "card_id": 1}
    )
    assert response.json == {"message": "Card not found."}
    assert response.status_code == 404


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
def test_create_card_control_card_invalid_json(client):
    """Tests bad path for create card control when invalid json passed"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[0]]
    malformed_res = {
        "message": "Malformed body data. Please supply the correct properties."
    }
    response = client.post(
        "/card-controls",
        json={
            "label": "minimum",
            "value": 1234,
        },
    )
    assert response.json == malformed_res
    assert response.status_code == 400
    response = client.post(
        "/card-controls", json={"label": "minimum", "value": "blah", "card_id": 1}
    )

    assert response.status_code == 500

    response = client.post(
        "/card-controls", json={"label": "maximum", "value": "blah", "card_id": 1}
    )

    assert response.status_code == 500
    response = client.post(
        "/card-controls", json={"label": "category", "value": "blah", "card_id": 1}
    )
    assert response.status_code == 500


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
def test_create_card_control_card_non_json(client):
    """Tests bad path for create card control when unsupported data type passed"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[0]]
    response = client.post(
        "/card-controls",
        data={
            "label": "minimum",
            "value": 1234,
        },
    )
    assert response.status_code == 415


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
@patch(
    "takehome.models.card.NewCardControl.NewCardControl.create",
    PATCHED_CREATE_CARD_CONTROL,
)
def test_create_card_control_card_unexpected_error(client):
    """Tests bad path for create card control when unexpected error"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[0]]
    PATCHED_CREATE_CARD_CONTROL.return_value = False
    response = client.post(
        "/card-controls", json={"label": "minimum", "value": 1234, "card_id": 1}
    )
    assert response.status_code == 500
    assert response.json == {"message": "Card control failed to create."}


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
@patch("takehome.models.card.Card.Card.delete_control", PATCHED_DELETE_CARD_CONTROL)
def test_delete_card_controls(client):
    """Tests happy path for delete card controls"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[1]]
    PATCHED_DELETE_CARD_CONTROL.return_value = True
    response = client.delete("/card-controls/2/category")
    assert response.status_code == 200
    assert response.json == {"message": "Card control successfully deleted."}


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
@patch("takehome.models.card.Card.Card.delete_control", PATCHED_DELETE_CARD_CONTROL)
def test_delete_card_controls_card_not_found(client):
    """Tests bad path for delete card controls where card is not found"""
    PATCHED_GET_CARD.return_value = []
    response = client.delete("/card-controls/2/category")
    assert response.status_code == 404
    assert response.json == {"message": "Card not found."}


@patch("takehome.models.card.Card.Card.get", PATCHED_GET_CARD)
@patch("takehome.models.card.Card.Card.delete_control", PATCHED_DELETE_CARD_CONTROL)
def test_delete_card_controls_unexpected_error(client):
    """Tests bad path for delete card controls where unexpected error"""
    PATCHED_GET_CARD.return_value = [MOCK_CARDS[1]]
    PATCHED_DELETE_CARD_CONTROL.return_value = False
    response = client.delete("/card-controls/2/category")
    assert response.status_code == 500
    assert response.json == {"message": "Card control failed to delete."}
