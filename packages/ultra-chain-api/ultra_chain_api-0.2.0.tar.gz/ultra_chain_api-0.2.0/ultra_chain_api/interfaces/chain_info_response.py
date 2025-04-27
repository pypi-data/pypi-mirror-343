from pydantic import BaseModel


class ChainInfoResponse(BaseModel):
    server_version: str
    chain_id: str
    head_block_num: int
    last_irreversible_block_num: int
    last_irreversible_block_id: str
    head_block_id: str
    head_block_time: str
    head_block_producer: str
    virtual_block_cpu_limit: int
    virtual_block_net_limit: int
    block_cpu_limit: int
    block_net_limit: int
    server_version_string: str
    fork_db_head_block_num: int
    fork_db_head_block_id: str
    server_full_version_string: str
    total_cpu_weight: int
    total_net_weight: int
    earliest_available_block_num: int
    last_irreversible_block_time: str
