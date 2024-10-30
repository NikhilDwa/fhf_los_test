import csv

from core_rate.core_LTV import coreltv_constants as c

file_path = "C:/Users/Leapfrog/fhf_los_test/core_rate/core_LTV/LOS_5952_SC_All_New_AcceptanceTst.csv"

with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]

final_interest = []
for d in csv_data:
    # print(d)
    split_use_case = d["TESTCASE"].split("_")
    # print(split_use_case)

    vehicle_type = d.get("Vehicle_Type", "").lower()
    final_ltvmax = 0

    if "039" in d["LOAN_PROGRAM_ID"] and vehicle_type == "new":
        final_ltvmax = c.base_rate_Line3["039"]["new"]
        line3ltv_totalCashprice = c.total_Cash_Price["039"]
        line3_ltv_adjustment = c.line3_ltv_adjustment["039"]

    elif "039" in d["LOAN_PROGRAM_ID"] and vehicle_type == "used":
        final_ltvmax = c.base_rate_Line3["039"]["used"]
        line3ltv_totalCashprice = c.total_Cash_Price["039"]
        line3_ltv_adjustment = c.line3_ltv_adjustment["039"]


    elif "040" in d["LOAN_PROGRAM_ID"] and vehicle_type == "new":
        final_ltvmax = c.base_rate_Line3["040"]["new"]
        line3ltv_totalCashprice = c.total_Cash_Price["040"]
        line3_ltv_adjustment = c.line3_ltv_adjustment["040"]

    elif "040" in d["LOAN_PROGRAM_ID"] and vehicle_type == "used":
        final_ltvmax = c.base_rate_Line3["040"]["used"]
        line3ltv_totalCashprice = c.total_Cash_Price["040"]
        line3_ltv_adjustment = c.line3_ltv_adjustment["040"]
    # print(split_use_case)
    # # breakpoint()
    # vehicle_type = d.get("Vehicle_Type", "").lower()
    # if vehicle_type == "new" and split_use_case[0] == "CA":
    #     final_ltvmax = c.base_rate_Line3["CAnew"]
    # elif vehicle_type == "new":
    #     final_ltvmax = c.base_rate_Line3["new"]
    # elif vehicle_type == "used" and split_use_case[0] == "CA":
    #     final_ltvmax = c.base_rate_Line3["CAused"]
    # elif vehicle_type == "used":
    #     final_ltvmax = c.base_rate_Line3["used"]

    JBstates = [
        "IL",
        "MI",
        "CT",
        "MD",
        "VA",
        "NJ",
        "NH",
        "PA",
        "MA",
        "SC",
        "NC",
        "DE",
        "GA",
        "WI",
        "TN",
        "IN",
        "KY",
        "OH",
        "OK",
        "NY",
        "FL",
        "TX",
        "AL",
    ]

    KBstates = ["CO", "ID", "NV", "UT", "OR", "WA", "AZ", "CA"]


    # Logic for using either dimension_rate or dimension_rate2

    total_cash_price = float(d["Total_Cash_Price"])

    if total_cash_price <= 32000:
        final_ltvmax += line3ltv_totalCashprice["0-32000"]
    elif 32001 <= total_cash_price <= 42000:
        final_ltvmax += line3ltv_totalCashprice["32001-42000"]
    elif 42001 <= total_cash_price <= 57000:
        final_ltvmax += line3ltv_totalCashprice["42001-57000"]
    elif 57001 <= total_cash_price <= 72000:
        final_ltvmax += line3ltv_totalCashprice["57001-72000"]
    elif total_cash_price > 72000:
        final_ltvmax += line3ltv_totalCashprice["72001+"]

    if "_SSN_" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["SSN"]

    if "_NoITIN_" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["No_ITIN"]

    if "700" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["700"]

    if "_600" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["600"]

    if "Luxury" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["Luxury"]

    if "PaidAuto" in d["TESTCASE"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["PaidAuto"]

    if "72" in d["Term"]:
        final_ltvmax = final_ltvmax + line3_ltv_adjustment["72"]

    if split_use_case[0] in JBstates and vehicle_type == "new":
        final_ltvmax += 3
    elif split_use_case[0] in KBstates:
        final_ltvmax += 3

    final_ltvmax = round(final_ltvmax, 2)
    final_interest.append(
        {
            "INFO_ID": "",
            "USE_CASE": d["TESTCASE"],
            "RESULT": "{'line3_ltv_max': " + str(final_ltvmax) + "}",
        }
    )


output_file = "output.csv"

# Writing to CSV file
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["INFO_ID", "USE_CASE", "RESULT"])
    writer.writeheader()
    writer.writerows(final_interest)
