from typing import Optional

import ormar

from models import MainMata
from user.models import User


class Follower(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    publisher: User = ormar.ForeignKey(User, related_name="subscribers")
    subscriber: User = ormar.ForeignKey(User, related_name="publisher")
