from typing import Any
from pydantic import BaseModel
from ultra_chain_api.interfaces.abi_response import Abi


class Field(BaseModel):
    name: str
    type: str


class Struct(BaseModel):
    name: str
    base: str
    fields: list[Field]


class Action(BaseModel):
    name: str
    type: str
    ricardian_contract: str


class Table(BaseModel):
    name: str
    index_type: str
    key_names: list[Any]
    key_types: list[Any]
    type: str


class CodeResponse(BaseModel):
    account_name: str
    code_hash: str
    wast: str
    wasm: str
    abi: Abi
