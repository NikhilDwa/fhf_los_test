import requests
from headers import headers  # Importing headers from the headers module

# Define the URLs, states, and loan program ID
extened_url = "https://restinternal.firsthelpfinancial.net/ordswrapper?https://apisdev.firsthelpfinancial.com/ords/mm/stipulations/689"

response1 = requests.get(extened_url, headers=headers)
data = response1.json()

config_items = data.get('items', [])

# Extract 'stip_name' values
stip_names = [item['stip_name'] for item in config_items if 'stip_name' in item]
print(stip_names)
