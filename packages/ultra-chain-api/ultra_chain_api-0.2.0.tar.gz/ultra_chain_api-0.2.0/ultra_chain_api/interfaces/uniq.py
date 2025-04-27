from typing import Optional
from pydantic import BaseModel


class Uniq(BaseModel):
    id: int
    token_factory_id: int
    mint_date: str
    serial_number: int
    uos_payment: float
    uri: Optional[str]
    hash: Optional[str]
