from pydantic import BaseModel


class FactoryGroupResponse(BaseModel):
    id: int
    manager: str
    uri: str
    hash: str
    factories: list[int]
    uos_payment: int
