from ultra_chain_api import TestProducerEndpoint, UltraAPI


def test_get_currency_balance() -> None:
    client = UltraAPI(producer_endpoint=TestProducerEndpoint.SWEDEN.value)
    balance_response = client.get_currency_balance("eosio.token", "ultra.nft.ft", "UOS")

    assert isinstance(balance_response, list), "Expected list type"
    assert len(balance_response) == 1, "Expected length 1"
