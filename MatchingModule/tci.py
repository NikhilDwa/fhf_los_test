import requests

from headers import headers

extended_url = "https://restinternal.firsthelpfinancial.net/restservice?https://restdev.firsthelpfinancial.com/itemization/config/EXTENDED?"
state = "MA"
loanProgramId="Indirect_AutoIndirect_001_000_Core_008_041"
tci_url = "https://restinternal.firsthelpfinancial.net/restexternalportal?/v2/tci/applications"
appid = "56672"

url = f"{tci_url}/{appid}?transformName=MATCHING_MODULE"
url1 = f"{extended_url}state={state}&loanProgramId={loanProgramId}"



response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    current_fhf_loan_version = data.get("data", {}).get("CurrentFHFLoanVersion", None)

    if current_fhf_loan_version:
        #print("CurrentFHFLoanVersion:", current_fhf_loan_version)
        keys_list = list(current_fhf_loan_version.keys())
        #print(keys_list)
    else:
        print("CurrentFHFLoanVersion not found in the response.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

response = requests.get(url1, headers=headers)

if response.status_code == 200:
    data = response.json()
    config_items = data.get('data', {}).get('config', [])
    item_names = [item['itemName'] for item in config_items if 'itemName' in item]
    #print("Extracted Item Names:", item_names)
else:
    print("Failed to fetch data. Status code:", response.status_code)
    print("Response:", response.text)


matching_item_names = set(keys_list).intersection(set(item_names))

non_matching_item_names_1 = set(keys_list).difference(set(item_names))
non_matching_item_names_2 = set(item_names).difference(set(keys_list))

print("Matching Item Names:", matching_item_names)
print("----------------------------------------------------------------------")
print("TCI", non_matching_item_names_1)
print("----------------------------------------------------------------------")
print("Extended:", non_matching_item_names_2)