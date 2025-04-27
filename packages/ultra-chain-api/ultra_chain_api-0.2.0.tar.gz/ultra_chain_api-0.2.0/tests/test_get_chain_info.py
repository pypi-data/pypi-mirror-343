from ultra_chain_api.interfaces.chain_info_response import ChainInfoResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_chain_info() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    chain_info = client.get_chain_info()

    assert isinstance(chain_info, ChainInfoResponse), "Expected ChainInfoResponse type"
