from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime


class Permission2(BaseModel):
    actor: str
    permission: str


class Account(BaseModel):
    permission: Permission2
    weight: int


class RequiredAuth(BaseModel):
    threshold: int
    keys: List[Any]
    accounts: List[Account]
    waits: List[Any]


class LinkedAction(BaseModel):
    account: str
    action: str


class Permission(BaseModel):
    perm_name: str
    parent: str
    required_auth: RequiredAuth
    linked_actions: List[LinkedAction]


class NetLimit(BaseModel):
    used: int
    available: int
    max: int
    last_usage_update_time: datetime
    current_used: int


class CpuLimit(BaseModel):
    used: int
    available: int
    max: int
    last_usage_update_time: datetime
    current_used: int


class SubjectiveCpuBillLimit(BaseModel):
    used: int
    available: int
    max: int
    last_usage_update_time: datetime
    current_used: int


class AccountResponse(BaseModel):
    account_name: str
    head_block_num: int
    head_block_time: datetime
    privileged: bool
    last_code_update: datetime
    created: datetime
    core_liquid_balance: str
    ram_quota: int
    net_weight: int
    cpu_weight: int
    net_limit: NetLimit
    cpu_limit: CpuLimit
    ram_usage: int
    permissions: List[Permission]
    total_resources: Optional[Any] = None
    self_delegated_bandwidth: Optional[Any] = None
    refund_request: Optional[Any] = None
    subjective_cpu_bill_limit: SubjectiveCpuBillLimit
    eosio_any_linked_actions: List[Any]
