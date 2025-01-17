from db.models import User, Subscribe
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from db.dao import BaseDAO


class UserDAO(BaseDAO[User]):
    model = User


class SubscribeDAO(BaseDAO[Subscribe]):
    model = Subscribe


class TelegramIDModel(BaseModel):
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class UserModel(TelegramIDModel):
    first_name: str | None
    last_name: str | None
    username: str | None
    date_subscribed: datetime


class SubscribedModel(TelegramIDModel):
    region: str


class CategoryModel(SubscribedModel):
    category: str

class GetUser(BaseModel):
    region: str
    category: str
