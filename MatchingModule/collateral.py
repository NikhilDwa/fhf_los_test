import requests
from headers import headers  # Importing headers from the headers module


base_url = "https://restinternal.firsthelpfinancial.net"
api_endpoint = "https://apisdev.firsthelpfinancial.com/ords/mm/config/DEFAULT_VEHICLE_VALUATION"
state = "FL"


extended_url = f"{base_url}/ordswrapper?{api_endpoint}?filter_name=STATE&filter_value={state}"

response = requests.get(extended_url, headers=headers)

data = response.json()

config_items = data.get('items', [])

if config_items:
    config_value = config_items[0].get('config_value')
    print("Config Value:", config_value)
else:
    print("No config items found")
