from ultra_chain_api import MainProducerEndpoint, UltraAPI


def test_get_uniqs() -> None:
    client = UltraAPI(producer_endpoint=MainProducerEndpoint.SWEDEN.value)
    uniqs_response = client.get_uniqs("aq1sr2zx3rt4")
    assert isinstance(uniqs_response, list), "Expected list type"
    assert len(uniqs_response) > 0, "Expected non-empty list"
