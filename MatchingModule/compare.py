import requests

from headers import headers

extened_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/EXTENDED?"
simple_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/SIMPLE?"
state = "IL"
loanProgramId="Indirect_AutoIndirect_001_000_Core_008_041"
url1 = f"{extened_url}state={state}&loanProgramId={loanProgramId}"
url2 = f"{simple_url}state={state}&loanProgramId={loanProgramId}"


def get_item_names(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        config_items = data.get('data', {}).get('config', [])
        return [item['itemName'] for item in config_items if 'itemName' in item]
    else:
        print(f"Failed to fetch data from {url}. Status code:", response.status_code)
        return []

# Extract item names from both APIs
item_names_1 = get_item_names(url1)
item_names_2 = get_item_names(url2)

# Compare item names
matching_item_names = set(item_names_1).intersection(set(item_names_2))
non_matching_item_names_1 = set(item_names_1).difference(set(item_names_2))
non_matching_item_names_2 = set(item_names_2).difference(set(item_names_1))

# Print results
print("Matching Item Names:", matching_item_names)
print("---------------------------------")
print("Extended API but not in the Simple:", non_matching_item_names_1)
print("---------------------------------")
print("Simple API but not in the Extended:", non_matching_item_names_2)