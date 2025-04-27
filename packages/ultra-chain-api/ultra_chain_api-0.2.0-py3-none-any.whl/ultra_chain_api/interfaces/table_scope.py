from pydantic import BaseModel
from typing import List, Any


class BaseTableResponse(BaseModel):
    rows: List[Any]
    more: bool


class TableResponse(BaseTableResponse):
    next_key: str
