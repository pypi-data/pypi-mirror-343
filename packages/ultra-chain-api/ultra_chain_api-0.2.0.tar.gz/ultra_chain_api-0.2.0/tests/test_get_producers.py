from ultra_chain_api.interfaces.producer_response import ProducersResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_producers() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    producers_response = client.get_producers()

    assert isinstance(producers_response, ProducersResponse), "Expected list type"
    assert len(producers_response.rows) > 0, "Expected non-empty list"
