# perigon
The Perigon API provides access to comprehensive news and web content data. To use the API, simply sign up for a Perigon Business Solutions account to obtain your API key. Your available features may vary based on your plan. See the Authentication section for details on how to use your API key.

For more information, please visit [https://docs.perigon.io/discuss](https://docs.perigon.io/discuss)

## Installation & Usage

```bash
# You can install this package via pip:
pip install perigon
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

## Authentication
Please refer to the documentation for authentication methods.

```python

import perigon
from perigon import ApiException
from pprint import pprint


# Initialize the API client with your API key
client = perigon.ApiClient(api_key="YOUR_API_KEY")

# Create an instance of the API class
api_instance = perigon.V1Api(client)
id = 'id_example' # str | 

# Synchronous API call
try:
    # Journalists ID
    api_response = api_instance.get_journalist_by_id(id)
    print("The response of V1Api->get_journalist_by_id:\n")
    pprint(api_response)
except ApiException as e:
    print("Exception when calling V1Api->get_journalist_by_id: %s\n" % e)

# Asynchronous API call
import asyncio

async def call_api_async():
    try:
        api_response = await api_instance.get_journalist_by_id_async(id)
        print("The async response of V1Api->get_journalist_by_id_async:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling V1Api->get_journalist_by_id_async: %s\n" % e)

# Run the async function
asyncio.run(call_api_async())

```


## License
This project is licensed under the MIT License - see the LICENSE file for details.
