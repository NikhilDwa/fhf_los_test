import requests
from headers import headers

base_url = "https://restinternal.firsthelpfinancial.net"
api_endpoint = "https://apisdev.firsthelpfinancial.com/ords/mm/config/DEFAULT_VEHICLE_VALUATION"

states = ["AL", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "ID", "IL", "IN", "KY", "MA", "MD", "MI",
          "NC", "NH", "NJ", "NV", "NY", "OH", "OK", "OR", "PA", "SC", "TN", "TX", "UT", "VA", "WA", "WI"]

jd_power_states = []
kbb_states = []

for state in states:
    extended_url = f"{base_url}/ordswrapper?{api_endpoint}?filter_name=STATE&filter_value={state}"

    response = requests.get(extended_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        config_items = data.get('items', [])

        if config_items:
            config_value = config_items[0].get('config_value')
            if config_value == "JD_POWER":
                jd_power_states.append(state)
            elif config_value == "KBB":
                kbb_states.append(state)
        else:
            print(f"No config items found for {state}")
    else:
        print(f"Failed to fetch data for {state}. Status Code: {response.status_code}")

print("\nStates using JD Power:", jd_power_states)
print("States using KBB:", kbb_states)
