from decimal import Decimal
from typing import Optional

from sqlalchemy.sql.sqltypes import DECIMAL

from pydantic import BaseModel



class User(BaseModel):
    id: int
    username: str
