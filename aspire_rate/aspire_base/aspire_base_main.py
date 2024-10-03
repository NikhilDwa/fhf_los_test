import csv
from pathlib import Path

from aspire_rate.aspire_base import constants as c

input_file_name = "aspire_base_input.csv"
output_file_name = "aspire_base_output.csv"

base_path: Path = Path(__file__).resolve().parent
file_path = base_path.joinpath(input_file_name)

with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]

final_interest = []

for d in csv_data:
    split_use_case = d["TESTCASE"].split("_")
    final_rate = 0

    p_tire = {}
    value = {}
    r_tire = {}
    ltv_value = {}
    state_usury_max_rate = {}
    if "039" in d["LOAN_PROGRAM_ID"]:
        p_tire = c.p_tire["039"]
        value = c.value["039"]
        r_tire = c.r_tire["039"]
        ltv_value = c.ltv_value["039"]
        state_usury_max_rate = c.state_usury_max_rate["039"]
    elif "040" in d["LOAN_PROGRAM_ID"]:
        p_tire = c.p_tire["040"]
        value = c.value["040"]
        r_tire = c.r_tire["040"]
        ltv_value = c.ltv_value["040"]
        state_usury_max_rate = c.state_usury_max_rate["040"]

    p_tire_data = p_tire[split_use_case[0]]
    value_data = value[split_use_case[3]]
    compare_value = ltv_value[split_use_case[0]][split_use_case[4]]

    final_rate = p_tire_data - value_data - compare_value

    min_rate = r_tire[split_use_case[1]]["min_apr"]
    max_rate = r_tire[split_use_case[1]]["max_apr"]
    state_usury_max_rate = state_usury_max_rate[split_use_case[2]]

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
