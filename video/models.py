from datetime import datetime
from typing import Optional, List

import ormar

from models import MainMata
from user.models import User


class Video(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    create_at: datetime = ormar.DateTime(default=datetime.now)
    user: Optional[User] = ormar.ForeignKey(User)
    like_count: int = ormar.Integer(default=0)
    like_user: Optional[List[User]] = ormar.ManyToMany(
        User, related_name="like_users"
    )
