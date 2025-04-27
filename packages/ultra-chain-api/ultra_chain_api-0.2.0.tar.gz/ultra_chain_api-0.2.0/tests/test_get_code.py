from ultra_chain_api.interfaces.code_response import CodeResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_code() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    code_response = client.get_code("ultra.tools")

    assert isinstance(code_response, CodeResponse), "Expected str type"
