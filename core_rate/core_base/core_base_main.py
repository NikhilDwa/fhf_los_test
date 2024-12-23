import csv
from pathlib import Path

from core_rate.core_base import constants as c

input_file_name= "CANoITINPV.csv"
output_file_name = "core_base_output.csv"

base_path: Path = Path(__file__).resolve().parent
file_path = base_path.joinpath(input_file_name)

with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]

final_interest = []

for d in csv_data:
    split_use_case = d["TESTCASE"].split("_")

    if split_use_case[0] in c.dimension_rate_adjustment.keys():
        dimension_rate = c.dimension_rate_adjustment[split_use_case[0]]
    else:
        dimension_rate = c.dimension_rate_adjustment["Normal"]

    if split_use_case[0] in c.num_rate.keys():
        num_rate_data = c.num_rate[split_use_case[0]]
    else:
        num_rate_data = c.num_rate["Normal"]

    final_rate = 0
    state_usury_max_rate = 0
    min_rate = 0
    max_rate = 0
    rate_reduction = 0
    if "041" in d["LOAN_PROGRAM_ID"]:
        final_rate = c.base_rate["041"][split_use_case[0]]
        state_usury_max_rate = c.state_usury_max_rate["041"][split_use_case[0]]
        min_rate = c.min_rate["041"]
        min_rate = c.min_rate["041"]
        max_rate = c.max_rate["041"]
        dimension_rate = dimension_rate["041"]
        num_rate_data = num_rate_data["041"]
        rate_reduction = c.rate_reduction["041"]

    elif "042" in d["LOAN_PROGRAM_ID"]:
        final_rate = c.base_rate["042"][split_use_case[0]]
        state_usury_max_rate = c.state_usury_max_rate["042"][split_use_case[0]]
        min_rate = c.min_rate["042"]
        max_rate = c.max_rate["042"]
        dimension_rate = dimension_rate["042"]
        num_rate_data = num_rate_data["042"]
        rate_reduction = c.rate_reduction["042"]

    # Logic for using either dimension_rate or dimension_rate2
    if split_use_case[-1] == "None":
        final_rate = final_rate + dimension_rate["None_None"]
    # if "_AB_" in d["TESTCASE"]:
    #     final_rate = final_rate + dimension_rate["_AB_"]
    # if "700" in d["TESTCASE"]:
    #     final_rate = final_rate + dimension_rate["700"]
    if "AB_700LTB" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["AB_700LTB"]
    if "_B_700" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["B_700"]
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
    if "_600" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["600"]
    if "<550" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["<550"]
    if "PaidAuto" in d["TESTCASE"]:
        final_rate = final_rate + dimension_rate["PaidAuto"]
    if "66" in d["Term"]:
        final_rate = final_rate + dimension_rate["66"]
    if "72" in d["Term"]:
        final_rate = final_rate + dimension_rate["72"]

    second_rate = {}
    if "SSN" in d["TESTCASE"]:
        second_rate = num_rate_data["SSN"]
    if "_ITIN_" in d["TESTCASE"]:
        second_rate = num_rate_data["ITIN"]
    if "_NoITIN_" in d["TESTCASE"]:
        second_rate = num_rate_data["NoITIN"]

    if split_use_case[-1] == "None":
        final_rate = final_rate + second_rate["None_None"]
    if "<600" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["<600"]
    if "PaidAuto" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["PaidAuto"]
    if "700+" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["700+"]
    if "_600" in d["TESTCASE"]:
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
    if "_D_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["D"]
    if "<550" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["<550"]
    if "66" in d["Term"]:
        final_rate = final_rate + second_rate["66"]

    if (
        "72" in d["Term"]
        and "_ITIN_" in d["TESTCASE"]
        and "_600" in d["TESTCASE"]
        and "PaidAuto" in d["TESTCASE"]
    ):
        final_rate = final_rate + second_rate["72"]
    elif "72" in d["Term"] and "_ITIN_" in d["TESTCASE"] and "_700" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["72"]
    elif "72" in d["Term"] and "_ITIN_" in d["TESTCASE"]:
        final_rate = final_rate + second_rate["72itin"]
    elif "72" in d["Term"]:
        final_rate = final_rate + second_rate["72"]

    if int(d["Milage"]) < 5000 and 2025 - int(d["Age"]) <= 2:
        final_rate = final_rate + second_rate["new_<2yr_<5000miles"]

    # Rate reduction
    if "0-20" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["0-20"]
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
    if "_20_" in d["TESTCASE"]:
        final_rate = final_rate - rate_reduction["0-20"]

    final_rate = max(final_rate, min_rate)
    final_rate = min(final_rate, max_rate)
    final_rate = min(final_rate, state_usury_max_rate)
    final_rate = round(final_rate, 2)
    final_interest.append(
        {
            "INFO_ID": "",
            "USE_CASE": d["TESTCASE"],
            "RATE": "{'interest_rate': " + str(final_rate) + "}",
        }
    )

# Writing to CSV file
with open(output_file_name, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["INFO_ID", "USE_CASE", "RATE"])
    writer.writeheader()
    writer.writerows(final_interest)
