from pydantic import BaseModel


class Key(BaseModel):
    key: str
    weight: int


class ProducerAuthority(BaseModel):
    threshold: int
    keys: list[Key]


class Row(BaseModel):
    owner: str
    producer_authority: tuple[int, ProducerAuthority]
    url: str
    total_votes: str
    producer_key: str


class ProducersResponse(BaseModel):
    rows: list[Row]
    total_producer_vote_weight: str
    more: str
