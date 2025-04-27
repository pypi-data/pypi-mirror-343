from typing import Any
from pydantic import BaseModel


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
    key_names: list[str]
    key_types: list[str]
    type: str


class Abi(BaseModel):
    version: str
    types: list[Any]
    structs: list[Struct]
    actions: list[Action]
    tables: list[Table]
    ricardian_clauses: list[Any]
    error_messages: list[Any]
    abi_extensions: list[Any]
    variants: list[Any]


class AbiResponse(BaseModel):
    account_name: str
    abi: Abi
