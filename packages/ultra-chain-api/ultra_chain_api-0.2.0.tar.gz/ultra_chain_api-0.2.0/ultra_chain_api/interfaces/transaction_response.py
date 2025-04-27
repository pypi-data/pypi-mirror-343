from typing import Optional
from pydantic import BaseModel


class Header(BaseModel):
    action_mroot: str
    confirmed: int
    new_producers: Optional[None]
    previous: str
    producer: str
    schedule_version: int
    timestamp: int
    transaction_mroot: str


class Data(BaseModel):
    header: Header


class Act(BaseModel):
    account: str
    authorization: list[dict]
    data: Data
    name: str


class Receipt(BaseModel):
    auth_sequence: list[dict]
    global_sequence: str
    receiver: str
    recv_sequence: str


class Action(BaseModel):
    timestamp: str
    abi_sequence: int
    act: Act
    act_digest: str
    action_ordinal: int
    block_id: str
    block_num: int
    code_sequence: int
    cpu_usage_us: int
    creator_action_ordinal: int
    global_sequence: int
    net_usage_words: int
    producer: str
    receipts: list[Receipt]
    trx_id: str


class TransactionResponse(BaseModel):
    actions: list[Action]
    cached_lib: bool
    executed: bool
    lib: int
    query_time_ms: float
    trx_id: str
