from flask import request
from takehome.app import app
from takehome.models.card.Card import Card
from takehome.models.card.NewCard import NewCard
from pydantic import ValidationError


@app.route("/cards", methods=["POST", "GET"])
def cards():
    if request.method == "POST":
        try:
            created = NewCard(**request.get_json()).create()

        except ValidationError as e:
            return {
                "message": "Malformed body data. Please supply the correct properties."
            }, 400
        if created:
            return {"message": "Card successfully created."}, 200
        return {"message": "Card failed to create."}, 500
    else:
        cards = Card.get()
        return {"message": [c.model_dump() for c in cards]}, 200
