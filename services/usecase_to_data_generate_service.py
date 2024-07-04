import csv
import random

from utils.logger_utils import Logger
from common.file_headers import aspire_column_name
from common.aspire_acceptance_constants import aspire_acceptance_input


class UseCaseToDataGenerateService:
    def __init__(self, file_path, csv_data):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.file_path = file_path
        self.csv_data = csv_data

    def write_header_to_csv(self, column_list):
        self.logger.info(
            f"inside write_header_to_csv method..........file_path: {self.file_path}, column_list."
        )
        with self.file_path.open(mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_list)
        self.logger.info(f"Header written to {self.file_path}")

    def calculate_sales_tax(self, acceptance_data_row):
        self.logger.info(f"inside calculate_sales_tax method..........acceptance_data_row")
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

    def calculate_af(self, acceptance_data_row):
        self.logger.info(f"inside calculate_af method..........acceptance_data_row")
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

    def calculate_ltv_3_lsl(self, acceptance_data_row):
        self.logger.info(f"inside calculate_ltv_3_lsl method..........acceptance_data_row")
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
        vehicle_value = int(
            acceptance_data_row.get("VEHICLE_VALUE", 1)
        )  # To avoid division by zero

        ltv_3_lsl = round((af_value - ltv_base_sum) / vehicle_value * 100, 2)
        acceptance_data_row["LTV_3_LSL"] = ltv_3_lsl

    def parse_equity_range(self, input_str):
        self.logger.info(f"inside parse_equity_range method..........input_str: {input_str}")
        input_str = input_str.strip()

        if input_str.startswith("<"):
            upper_bound = float(input_str[1:].strip())
            return [0, upper_bound - 2]

        elif "-" in input_str:
            bounds = input_str.split("-")
            if len(bounds) != 2:
                raise ValueError("Invalid range format")

            lower_bound = float(bounds[0].strip())
            upper_bound = float(bounds[1].strip())
            return [lower_bound + 2, upper_bound - 2]

        elif input_str.startswith(">"):
            lower_bound = float(input_str[1:].strip())
            return [lower_bound + 2, 105]

        else:
            raise ValueError("Invalid input format")

    def choose_down_payment_for_equity(self, equity_range, acceptance_data_row):
        self.logger.info(
            f"inside choose_down_payment_for_equity method..........equity_range: {equity_range}, acceptance_data_row"
        )
        lower_bound, upper_bound = equity_range
        while True:
            # Randomly choose a DOWN_PAYMENT within the possible range of TOTAL_CASH_PRICE
            total_cash_price = int(acceptance_data_row["TOTAL_CASH_PRICE"])
            acceptance_data_row["DOWN_PAYMENT"] = random.randint(0, total_cash_price)

            # Recalculate AF and LTV_3_LSL with the new DOWN_PAYMENT
            self.calculate_sales_tax(acceptance_data_row)
            self.calculate_af(acceptance_data_row)
            self.calculate_ltv_3_lsl(acceptance_data_row)

            ltv_3_lsl = acceptance_data_row["LTV_3_LSL"]

            if lower_bound <= ltv_3_lsl <= upper_bound:
                break

    def get_acceptance_data(self, use_case):
        self.logger.info(f"inside get_acceptance_data method..........use_case: {use_case}")
        acceptance_data_row = {"USE_CASE": use_case["USE_CASE"]}
        split_use_case = use_case["USE_CASE"].split("_")
        acceptance_data_row["EQUITY"] = split_use_case[-1]
        for column in aspire_column_name:
            if column in aspire_acceptance_input:
                if (
                    isinstance(aspire_acceptance_input[column], list)
                    and len(aspire_acceptance_input[column]) == 2
                    and all(isinstance(i, int) for i in aspire_acceptance_input[column])
                ):
                    acceptance_data_row[column] = random.randint(
                        aspire_acceptance_input[column][0], aspire_acceptance_input[column][1]
                    )
                elif (
                    isinstance(aspire_acceptance_input[column], str)
                    and "," in aspire_acceptance_input[column]
                ):
                    options = aspire_acceptance_input[column].split(",")
                    acceptance_data_row[column] = random.choice(options).strip()
                else:
                    acceptance_data_row[column] = aspire_acceptance_input[column]
        acceptance_data_row["VEHICLE_VALUE"] = acceptance_data_row["TOTAL_CASH_PRICE"]
        acceptance_data_row["AVG_TRADEIN_VALUE"] = acceptance_data_row["TOTAL_CASH_PRICE"]

        equity = self.parse_equity_range(acceptance_data_row["EQUITY"])
        self.choose_down_payment_for_equity(equity, acceptance_data_row)

        return acceptance_data_row

    def write_data_to_csv(self):
        self.logger.info(f"inside write_data_to_csv method..........")
        with open(self.file_path, mode="a", newline="") as file:
            fieldnames = [field for field in aspire_column_name]
            for row in self.csv_data:
                if row["USE_CASE"] == "":
                    continue
                acceptance_data = self.get_acceptance_data(row)
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(acceptance_data)

    def generate_use_case_data(self):
        self.logger.info(f"inside generate_use_case_data method..........")
        self.write_header_to_csv(aspire_column_name)
        self.write_data_to_csv()
