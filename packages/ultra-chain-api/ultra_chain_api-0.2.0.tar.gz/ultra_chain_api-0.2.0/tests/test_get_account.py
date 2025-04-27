from ultra_chain_api.interfaces.account_response import AccountResponse
from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_account() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    account_response = client.get_account("ultra")

    assert isinstance(account_response, AccountResponse), "Expected AccountResponse type"
    assert account_response.account_name == "ultra", "Account name mismatch"
