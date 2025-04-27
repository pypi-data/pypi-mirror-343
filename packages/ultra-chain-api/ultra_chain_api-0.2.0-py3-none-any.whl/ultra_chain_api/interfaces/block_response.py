from pydantic import BaseModel
from typing import List, Any


class Rate(BaseModel):
    timestamp: int
    price: str


class Data(BaseModel):
    exchange: str
    rates: List[Rate]
    volume: str


class Authorization(BaseModel):
    actor: str
    permission: str


class Action(BaseModel):
    account: str
    name: str
    authorization: List[Authorization]
    data: Data
    hex_data: str


class Transaction2(BaseModel):
    expiration: str
    ref_block_num: int
    ref_block_prefix: int
    max_net_usage_words: int
    max_cpu_usage_ms: int
    delay_sec: int
    context_free_actions: List[Any]
    actions: List[Action]


class Trx(BaseModel):
    id: str
    signatures: List[str]
    compression: str
    packed_context_free_data: str
    context_free_data: List[Any]
    packed_trx: str
    transaction: Transaction2


class Transaction(BaseModel):
    status: str
    cpu_usage_us: int
    net_usage_words: int
    trx: Trx


class BlockResponse(BaseModel):
    timestamp: str
    producer: str
    confirmed: int
    previous: str
    transaction_mroot: str
    action_mroot: str
    schedule_version: int
    new_producers: Any
    producer_signature: str
    transactions: List[Transaction]
    id: str
    block_num: int
    ref_block_prefix: int
