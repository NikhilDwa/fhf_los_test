import requests

from headers import headers

extened_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/EXTENDED?"
simple_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/SIMPLE?"
state = "CA"
loanProgramId="Indirect_AutoIndirect_001_000_Core_008_041"
url1 = f"{extened_url}state={state}&loanProgramId={loanProgramId}"
url2 = f"{simple_url}state={state}&loanProgramId={loanProgramId}"


def get_item_constraints(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Extracting config items
        config_items = data.get('data', {}).get('config', [])
        # Printing constraints
        for item in config_items:
            constraints = item.get('constraints')
            if constraints:
                print(f"Item Name: {item.get('itemName')}")
                print(f"Constraints: {constraints}")
                print("-" * 50)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}. Error: {e}")

print(get_item_constraints(url1))
