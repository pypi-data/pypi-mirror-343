from ultra_chain_api.interfaces.abi_response import AbiResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_abi() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    abi_response = client.get_abi("ultra.tools")

    assert isinstance(abi_response, AbiResponse), "Expected AbiResponse type"
    assert abi_response.account_name == "ultra.tools", "Account name mismatch"
