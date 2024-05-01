from flask import request
from takehome.app import app
from takehome.models.card.Card import Card
from takehome.models.card.NewCard import NewCard
from pydantic import ValidationError

from takehome.models.card.NewCardControl import NewCardControl


@app.route("/card-controls", methods=["POST", "GET"])
def card_controls():
    if request.method == "GET":
        cards = Card.get()
        card_controls = [c.controls for c in cards if c.controls]
        flat_controls = []
        for controls in card_controls:
            flat_controls += [c.model_dump() for c in controls]
        return flat_controls, 200
    else:
        try:
            new_card_control = NewCardControl(**request.get_json())
            cards = Card.get(id=new_card_control.card_id)
            if not cards:
                return {"message": "Card not found."}, 404
            created = new_card_control.create()
        except ValidationError as e:
            return {
                "message": "Malformed body data. Please supply the correct properties."
            }, 400
        if created:
            return {"message": "Card control added to card."}, 200
        return {"message": "Card control failed to create."}, 500


@app.route("/card-controls/<id>/<label>", methods=["DELETE"])
def delete_card_controls(id, label):
    cards: list[Card] = Card.get(id)
    if not cards:
        return {"message": "Card not found."}, 404
    if cards[0].delete_control(label):
        return {"message": "Card control successfully deleted."}, 200
    return {"message": "Card control failed to delete."}, 500
