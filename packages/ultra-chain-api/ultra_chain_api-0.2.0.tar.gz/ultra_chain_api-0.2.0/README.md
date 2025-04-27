# Ultra Chain API Python

Ultra Chain Api Python is a Python wrapper for the Ultra chain API. It provides an easy-to-use interface for developers to seamlessly integrate Ultra blockchain functionalities into their Python applications.
DOCS: https://developers.ultra.io/products/chain-api/

## Installation

```bash
pip install ultra-chain-api
```

## Usage

```python
from ultra_chain_api import UltraAPI

# You can also import the producers
# from ultra_chain_api import MainProducerEndpoint
# client = UltraAPI(producer_endpoint=MainProducerEndpoint.SWEDEN.value)


client = UltraAPI(producer_endpoint="producer endpoint url")
response = client.get_info()
print(response)
```

## License

This project is licensed under the MIT License.
