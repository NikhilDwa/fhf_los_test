import csv
import random
from pathlib import Path

from core_acceptance_test import constants as c

input_file_name = "core_acceptance_input.csv"
output_file_name = "core_acceptance_output.csv"

base_path: Path = Path(__file__).resolve().parent
file_path = base_path.joinpath(input_file_name)

# Reading the input CSV file
with open(file_path, "r", newline="") as los_file:
    csv_reader = csv.DictReader(los_file)
    csv_data = [dict(row) for row in csv_reader]

# Writing the header to the output CSV file
with open(output_file_name, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(c.core_acceptance_column_headers)

# Iterating over each row in the CSV
for row in csv_data:
    if row["TESTCASE"] == "":
        continue

    acceptance_data_row = {"TESTCASE": row["TESTCASE"]}
    split_use_case = row["TESTCASE"].split("_")
    acceptance_data_row["EQUITY"] = split_use_case[-1]

    for column in c.core_acceptance_column_headers:
        if column in c.core_acceptance_input:
            if (
                isinstance(c.core_acceptance_input[column], list)
                and len(c.core_acceptance_input[column]) == 2
            ):
                acceptance_data_row[column] = random.randint(
                    c.core_acceptance_input[column][0], c.core_acceptance_input[column][1]
                )
            elif (
                isinstance(c.core_acceptance_input[column], str)
                and "," in c.core_acceptance_input[column]
            ):
                options = c.core_acceptance_input[column].split(",")
                acceptance_data_row[column] = random.choice(options).strip()
            else:
                acceptance_data_row[column] = c.core_acceptance_input[column]

    acceptance_data_row["VEHICLE_VALUE"] = acceptance_data_row["TOTAL_CASH_PRICE"]
    acceptance_data_row["AVG_TRADEIN_VALUE"] = acceptance_data_row["TOTAL_CASH_PRICE"]

    equity_str = acceptance_data_row["EQUITY"].strip()
    if equity_str.startswith("<"):
        upper_bound = float(equity_str[1:].strip())
        equity_range = [0, upper_bound - 2]
    elif "-" in equity_str:
        bounds = equity_str.split("-")
        lower_bound = float(bounds[0].strip())
        upper_bound = float(bounds[1].strip())
        equity_range = [lower_bound + 2, upper_bound - 2]
    elif equity_str.startswith(">"):
        lower_bound = float(equity_str[1:].strip())
        equity_range = [lower_bound + 2, 105]

    tax_base_columns = [
        "TOTAL_CASH_PRICE",
        "FHF_WARRANTY_CHECK",
        "FHF_GAP_CHECK",
        "WARRANTY",
        "GAP_INSURANCE",
        "HARD_ADD_ONS",
        "OTHER_PRODUCT_PRICE",
        "TIRE_AND_WHEEL_FEE",
        "DOC_FEE",
        "MAINTENANCE_FEE",
        "FREGIT_FEE",
        "STAMP_TAX",
    ]
    tax_base_sum = sum(float(acceptance_data_row.get(col, 0)) for col in tax_base_columns)
    sales_tax = 0.06 * tax_base_sum
    acceptance_data_row["SALES_TAX"] = sales_tax

    af_base_columns = [
        "TOTAL_CASH_PRICE",
        "TITLE_PREP_FEE",
        "REG_FEE",
        "DOC_FEE",
        "FHF_WARRANTY_CHECK",
        "FHF_GAP_CHECK",
        "WARRANTY",
        "GAP_INSURANCE",
        "HARD_ADD_ONS",
        "OTHER_PRODUCT_PRICE",
        "TIRE_AND_WHEEL_FEE",
        "SALES_TAX",
        "VSI",
    ]
    af_base_sum = sum(float(acceptance_data_row.get(col, 0)) for col in af_base_columns)
    down_payment = float(acceptance_data_row.get("DOWN_PAYMENT", 0))
    af = af_base_sum - down_payment
    acceptance_data_row["AF"] = af

    ltv_base_columns = [
        "FHF_WARRANTY_CHECK",
        "FHF_GAP_CHECK",
        "WARRANTY",
        "GAP_INSURANCE",
        "HARD_ADD_ONS",
        "OTHER_PRODUCT_PRICE",
        "MAINTENANCE_FEE",
        "FREGIT_FEE",
        "STAMP_TAX",
        "TIRE_AND_WHEEL_FEE",
    ]
    ltv_base_sum = sum(int(acceptance_data_row.get(col, 0)) for col in ltv_base_columns)
    af_value = int(acceptance_data_row.get("AF", 0))
    vehicle_value = int(acceptance_data_row.get("VEHICLE_VALUE", 1))  # Avoid division by zero
    ltv_3_lsl = round((af_value - ltv_base_sum) / vehicle_value * 100, 2)
    acceptance_data_row["LTV_3_LSL"] = ltv_3_lsl

    lower_bound, upper_bound = equity_range
    while True:
        total_cash_price = int(acceptance_data_row["TOTAL_CASH_PRICE"])
        acceptance_data_row["DOWN_PAYMENT"] = random.randint(0, total_cash_price)

        # Recalculate AF and LTV_3_LSL
        tax_base_sum = sum(float(acceptance_data_row.get(col, 0)) for col in tax_base_columns)
        acceptance_data_row["SALES_TAX"] = 0.06 * tax_base_sum
        af_base_sum = sum(float(acceptance_data_row.get(col, 0)) for col in af_base_columns)
        af = af_base_sum - float(acceptance_data_row.get("DOWN_PAYMENT", 0))
        acceptance_data_row["AF"] = af
        ltv_base_sum = sum(int(acceptance_data_row.get(col, 0)) for col in ltv_base_columns)
        ltv_3_lsl = round((int(acceptance_data_row["AF"]) - ltv_base_sum) / vehicle_value * 100, 2)
        acceptance_data_row["LTV_3_LSL"] = ltv_3_lsl

        if lower_bound <= ltv_3_lsl <= upper_bound:
            break

    # Writing each processed row to the CSV
    with open(output_file_name, mode="a", newline="") as file:
        fieldnames = [field for field in c.core_acceptance_column_headers]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        acceptance_data_row["SALES_TAX"] = round(acceptance_data_row["SALES_TAX"], 2)
        acceptance_data_row["AF"] = round(acceptance_data_row["AF"], 2)
        acceptance_data_row["LTV_3_LSL"] = round(acceptance_data_row["LTV_3_LSL"], 2)
        writer.writerow(acceptance_data_row)
