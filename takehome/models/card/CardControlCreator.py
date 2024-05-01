from pydantic import BaseModel
from takehome.models.card.CardControl import ControlChoices
from takehome.models.card.CategoryCardControl import CategoryCardControl
from takehome.models.card.MaxCardControl import MaxCardControl
from takehome.models.card.MerchantCardControl import MerchantCardControl
from takehome.models.card.MinCardControl import MinCardControl


class CardControlCreator(BaseModel):
    @staticmethod
    def create(**kwargs):
        label = kwargs.get("label")
        if label == ControlChoices.merchant:
            return MerchantCardControl(**kwargs)
        elif label == ControlChoices.category:
            return CategoryCardControl(**kwargs)
        elif label == ControlChoices.maximum:
            return MaxCardControl(**kwargs)
        else:
            return MinCardControl(**kwargs)
