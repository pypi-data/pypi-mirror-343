from ultra_chain_api.interfaces.block_response import BlockResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_block() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    block_response = client.get_block("0eb3fddf8f6930833f0f7a17bf85e507a18c99e4fecf301fcd990e8a57d6f5ec")

    assert isinstance(block_response, BlockResponse), "Expected BlockResponse type"
    assert block_response.id == "0eb3fddf8f6930833f0f7a17bf85e507a18c99e4fecf301fcd990e8a57d6f5ec", (
        "Block number mismatch"
    )
