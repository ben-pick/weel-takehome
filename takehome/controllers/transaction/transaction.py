from flask import request
from takehome.app import app
from takehome.models.card.Card import Card
from takehome.models.transaction.NewTransaction import NewTransaction
from pydantic import ValidationError

from takehome.models.transaction.Transaction import Transaction


@app.route("/transactions", methods=["POST", "GET"])
def transactions():
    if request.method == "POST":
        try:
            created = NewTransaction(**request.get_json()).create()
        except ValidationError as e:
            return {
                "message": "Malformed body data. Please supply the correct properties."
            }, 400
        if created:
            return {"message": "Transaction approved."}, 200
        return {"message": "Transaction declined."}, 400
    else:
        transactions = Transaction.get()
        return {"message": [t.model_dump() for t in transactions]}, 200
