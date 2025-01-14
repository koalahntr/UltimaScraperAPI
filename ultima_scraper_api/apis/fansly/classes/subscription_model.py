from datetime import datetime
from typing import TYPE_CHECKING, Any

from ultima_scraper_api.apis.fansly.classes.user_model import create_user
from ultima_scraper_api.models.subscription_model import BaseSubscriptionModel

if TYPE_CHECKING:
    import ultima_scraper_api

    auth_types = ultima_scraper_api.auth_types
    user_types = ultima_scraper_api.user_types


class SubscriptionModel(BaseSubscriptionModel):
    def __init__(
        self, data: dict[str, Any], user: "create_user", subscriber: "auth_types"
    ) -> None:
        self.price: int = data["price"]
        self.created_at: datetime = datetime.fromtimestamp(data["createdAt"] / 1000)
        self.ends_at: datetime = datetime.fromtimestamp(data["endsAt"] / 1000)
        self.user = user
        self.subscriber = subscriber
        self.__raw__ = data

    def is_active(self):
        return True if self.created_at > self.ends_at else False

    def get_authed(self):
        return self.subscriber.get_authed()

    def get_price(self):
        return self.price

    def resolve_expires_at(self):
        return self.ends_at
