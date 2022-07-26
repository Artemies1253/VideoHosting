from typing import Optional

import ormar

from models import MainMata


class User(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    email: Optional[str] = ormar.String(max_length=100)
    full_name: Optional[str] = ormar.String(max_length=100)
    disabled: bool = ormar.Boolean(default=False)
    hashed_password: str = ormar.String(max_length=100)
