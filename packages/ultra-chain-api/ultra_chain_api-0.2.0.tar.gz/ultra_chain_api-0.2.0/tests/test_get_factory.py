from ultra_chain_api.api.api import MainProducerEndpoint
from ultra_chain_api.interfaces.factory_response import FactoryResponse
from ultra_chain_api import UltraAPI
from ultra_chain_api.api.api import FactoryTable


def test_get_factory() -> None:
    client = UltraAPI(producer_endpoint=MainProducerEndpoint.SWEDEN.value)
    factory_response = client.get_factory(2212, FactoryTable.FACTORY_B)

    assert isinstance(factory_response, FactoryResponse), "Expected FactoryResponse type"
