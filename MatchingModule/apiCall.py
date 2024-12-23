import requests

# Define the API endpoint and API key
api_url = "https://compliancewsqa.carletoninc.com/v1.1/rest/compliancereport"
api_key = "2246c43a-be6b-4ab3-b038-c50d562c96d7"

# Define the payload
payload ={
  "Source": "MM",
  "UniqueIdentifier": "58232",
  "IsRepull": "true",
  "User": "collectionsmanager",
  "SellingPrice": 53500.61,
  "VehicleYear": 2015,
  "VehicleType": "Used",
  "APR": 23.99,
  "AmountFinanced": 39500.61,
  "FinanceCharge": 28648.59,
  "TotalOfPayments": 68149.2,
  "TotalSalePrice": 53500.61,
  "ContractDate": "2024-12-17",
  "interestStartDate": "2024-12-17",
  "FirstPaymentDate": "2025-01-17",
  "MaturityDate": "2030-01-17",
  "Interest": 28648.59,
  "Principal": 39500.61,
  "CashDown": 14000,
  "Term": 60,
  "PaymentAmount": 1135.82,
  "DealerState": "IL"
}

# Set the headers with the API key
headers = {
    "ApiKey": api_key,
    "Content-Type": "application/json",
}

try:
    # Send the POST request
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

    # Parse the JSON response
    data = response.json()

    # Extract and print values that are 'No' or 'Yes'
    for key, value in data.items():
        if value in ["No", "Yes"]:
            print(f"{key}: {value}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
