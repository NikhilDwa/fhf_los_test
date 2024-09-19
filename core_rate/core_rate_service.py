import csv

from core_rate import core_constants as c

file_path = "/Users/nikhil/Documents/Leapfrog/new/fhf_los_test/core_rate/core_rate.csv"

with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]


final_interest = []
for d in csv_data:
    split_use_case = d["TESTCASE"].split("_")
    final_rate = c.base_rate[split_use_case[0]]
    state_usury_max_rate = c.state_usury_max_rate[split_use_case[0]]

    # For rate calculation
    dimension_rate = c.dimension_rate_adjustment

    if "None_None" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["None_None"]
    if "AB_700LTB_PaidAuto" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["AB_700LTB_PaidAuto"]
    if "B_700_PaidAuto" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["B_700_PaidAuto"]
    if "A_700LTB" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["A_700LTB"]
    if "C_700STB" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["C_700STB"]
    if "D_700" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["D_700"]
    if "Mileage" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["Mileage"]
    if "Luxury" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["Luxury"]
    if "<600" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["<600"]
    if "<500" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["<500"]
    if "PaidAuto_600" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["PaidAuto_600"]
    if "66" in d["Term"]:
        final_rate = final_rate + dimension_rate["66"]
    if "72" in d["Term"]:
        final_rate = final_rate + dimension_rate["72"]

    second_rate = {}
    if "FL" in d["TESTCASE"][0]:
        second_rate = c.fl_num_rate
    else:
        second_rate = c.num_rate
    if "SSN" in d["TESTCASE"]:
        second_rate = second_rate["SSN"]
    if "ITIN" in d["TESTCASE"]:
        second_rate = second_rate["ITIN"]
    if "NOITIN" in d["TESTCASE"]:
        second_rate = second_rate["NoITIN"]

    if "None_None" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["None_None"]
    if "<600" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["<600"]
    if "PaidAuto" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["PaidAuto"]
    if "700+" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["700+"]
    if "600" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["600"]
    if "Mileage" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["Mileage"]
    if "Luxury" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["Luxury"]
    if "_AB_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["AB"]
    if "_A_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["A"]
    if "_B_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["B"]
    if "_C_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["C"]
    if "_C_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["D"]
    if "66" in d["Term"]:
        final_rate = final_rate + second_rate["66"]
    if "72" in d["Term"]:
        final_rate = final_rate + second_rate["72"]

    if d["Vehicle_Type"] == "New" and int(d["Milage"]) < 5000 and 2025 - int(d["Age"]) <= 1:
        final_rate = final_rate + second_rate["new_<2yr_<5000miles"]

    # Rate reduction
    rate_reduction = c.rate_reduction
    if "0-20" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["0-20"]
    elif "20" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["20"]
    if "20.01-30" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["20.01-30"]
    if "30.01-40" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["30.01-40"]
    if "40.01-50" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["40.01-50"]
    if "50.01-60" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["50.01-60"]
    if "60.01-70" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["60.01-70"]
    if "70.01-80" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["70.01-80"]

    final_rate = max(final_rate, c.min_rate)
    final_rate = min(final_rate, c.max_rate)
    final_rate = min(final_rate, state_usury_max_rate)
    final_rate = rounded_value = round(final_rate, 2)
    final_interest.append(
        {
            "INFO_ID": "",
            "USE_CASE": d["TESTCASE"],
            "RATE": "{interest_rate: " + str(final_rate) + "}",
        }
    )


output_file = "output.csv"

# Writing to CSV file
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["INFO_ID", "USE_CASE", "RATE"])
    writer.writeheader()
    writer.writerows(final_interest)
