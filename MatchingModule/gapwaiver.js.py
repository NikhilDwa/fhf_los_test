import requests
from headers import headers  # Importing headers from the headers module

# Define the URLs, states, and loan program ID
extened_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/EXTENDED?"
# simple_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/SIMPLE?"
states = ["AL","AZ","CA","CO","CT","DE","FL","GA","ID","IL","IN","KY","MA","MD","MI","NC","NH","NJ","NV","NY","OH","OK","OR","PA"]
loanProgramId = "Indirect_AutoIndirect_001_000_Core_008_041"


states_without_l5GapWaiver = []


for state in states:

    url1 = f"{extened_url}state={state}&loanProgramId={loanProgramId}"
    # url2 = f"{simple_url}state={state}&loanProgramId={loanProgramId}"

    try:
        response1 = requests.get(url1, headers=headers)
        # response2 = requests.get(url2, headers=headers)

        if response1.status_code == 200:
            data1 = response1.json()
            config_items = data1.get('data', {}).get('config', [])
            item_names = [item['itemName'] for item in config_items if 'itemName' in item]

            if 'l5GapWaiver' not in item_names:
                states_without_l5GapWaiver.append(state)
        else:
            print(
                f"Failed to fetch data for state: {state}, Status Codes: {response1.status_code}")

    except Exception as e:
        print(f"An error occurred for state {state}: {e}")

print("States without l5GapWaiver:", states_without_l5GapWaiver)
