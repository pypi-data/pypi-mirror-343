from pydantic import BaseModel
from typing import Optional, Any


class ResaleShare(BaseModel):
    receiver: str
    basis_point: int


class FactoryResponse(BaseModel):
    id: int
    asset_manager: str
    asset_creator: str
    minimum_resell_price: str
    resale_shares: list[ResaleShare]
    mintable_window_start: Optional[Any]
    mintable_window_end: Optional[Any]
    trading_window_start: Optional[Any]
    trading_window_end: Optional[Any]
    recall_window_start: Optional[int]
    recall_window_end: Optional[Any]
    lockup_time: Optional[int]
    conditionless_receivers: list[str]
    stat: int
    factory_uri: str
    factory_hash: str
    max_mintable_tokens: int
    minted_tokens_no: int
    existing_tokens_no: int
    authorized_tokens_no: Optional[Any]
    account_minting_limit: Optional[int]
    transfer_window_start: Optional[Any]
    transfer_window_end: Optional[Any]
    default_token_uri: str
    default_token_hash: str
    lock_hash: int
