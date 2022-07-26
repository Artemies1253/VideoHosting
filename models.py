from datetime import datetime
from typing import Optional

import ormar

from db import metadata, database


class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database