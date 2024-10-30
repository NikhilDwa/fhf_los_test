import csv

from core_rate.core_LTV_downper import coredp_constants as c

file_path = "C:/Users/Leapfrog/fhf_los_test/core_rate/core_LTV_downper/CANoITINPV.csv"

with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]


final_interest = []
for d in csv_data:
    # print(d)
    split_use_case = d["TESTCASE"].split("_")
    # print(split_use_case)


    # Logic for using either dimension_rate or dimension_rate2

    vehicle_type = d.get("Vehicle_Type", "").lower()
    final_ltvmax = 0

    if "009" in d["LOAN_PROGRAM_ID"]:
        final_ltvmax = c.base_rate_Line5["009"]
        dp_totalCashprice = c.total_Cash_Price["009"]
        dp_adjustment = c.dp_adjustment["009"]

    elif "040" in d["LOAN_PROGRAM_ID"]:
        final_ltvmax = c.base_rate_Line5["040"]
        dp_totalCashprice = c.total_Cash_Price["040"]
        dp_adjustment = c.dp_adjustment["040"]

    total_cash_price = float(d["Total_Cash_Price"])

    if total_cash_price <= 32000:
        final_ltvmax += dp_totalCashprice["0-32000"]
    elif 32001 <= total_cash_price <= 42000:
        final_ltvmax += dp_totalCashprice["32001-42000"]
    elif 42001 <= total_cash_price <= 57000:
        final_ltvmax += dp_totalCashprice["42001-57000"]
    elif 57001 <= total_cash_price <= 72000:
        final_ltvmax += dp_totalCashprice["57001-72000"]
    elif total_cash_price > 72000:
        final_ltvmax += dp_totalCashprice["72001+"]

    if "_SSN_" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["SSN"]

    if "_NoITIN_" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["No_ITIN"]

    if "Luxury" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["Luxury"]

    if "PaidAuto" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["PaidAuto"]

    if "700" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["700"]

    if "_600" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + dp_adjustment["600"]

    # if split_use_case[0] in JBstates and vehicle_type == "new":
    #     final_ltvmax += 3
    # elif split_use_case[0] in KBstates:
    #     final_ltvmax+=3

    final_ltvmax = max(final_ltvmax, 10)
    final_ltvmax = round(final_ltvmax, 2)
    final_interest.append(
        {
            "INFO_ID": "",
            "USE_CASE": d["TESTCASE"],
            "RESULT": "{'percent_down_min': " + str(final_ltvmax) + "}",
        }
    )


output_file = "output.csv"

# Writing to CSV file
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["INFO_ID", "USE_CASE", "RESULT"])
    writer.writeheader()
    writer.writerows(final_interest)
