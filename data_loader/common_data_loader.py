import csv
import random

from utils.logger_utils import Logger
from utils.path_utils import PathUtils


class CommonDataLoader:
    def __init__(self):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.column_name = []
        self.file_path = None
        self.csv_data = None
        self.start_id = None
        self.config_data = None
        self.count = 0

    def write_header_to_file(self):
        self.logger.info(f"inside write_header_to_file method..........")
        try:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                json_index = self.column_name.index("JSON")
                first_row = self.column_name[: json_index + 1] + [""] * (
                    len(self.column_name) - json_index - 2
                )
                writer.writerow(first_row)
                second_row = [""] * json_index + self.column_name[json_index + 1 :]
                writer.writerow(second_row)
            self.logger.info(f"Header written to file: {self.file_path}")
        except Exception as e:
            self.logger.exception(f"Failed to write CSV file: {e}")

    def process_csv_data(self, row_data):
        self.logger.info(f"inside process_csv_data method..........row_data")
        if "JSON" in row_data:
            del row_data["JSON"]
        row_data["ID"] = self.start_id
        self.start_id += 1
        return row_data

    def update_collateral_dict(self, row_data):
        self.logger.info(f"inside update_collateral_dict method..........row_data")
        row_data["YEAR"] = row_data["VEHICLE_YEAR"]
        if "Truck" in row_data["USE_CASE"]:
            row_data["VEHICLE_MAKE_TYPE"] = "Truck"
        else:
            row_data["VEHICLE_MAKE_TYPE"] = "Sedan"
        return row_data

    def update_info_dict(self, row_data):
        self.logger.info(f"inside update_info_dict method..........row_data")
        config = PathUtils().get_configuration()
        increment_fields = {
            "APPLICANT": config["APPLICANT_INPUT"]["start_id"],
            "COLLATERAL": config["COLLATERAL_INPUT"]["start_id"],
            "INFO": config["INFO_INPUT"]["start_id"],
            "STRUCTURE": config["STRUCTURE_INPUT"]["start_id"],
        }

        for field, start_id in increment_fields.items():
            row_data[field] = start_id + self.count

        self.count += 1
        row_data["TEST_NAME"] = row_data["USE_CASE"]
        split_use_case = row_data["USE_CASE"].split("_")
        if "700" in row_data["USE_CASE"]:
            row_data["FICO_SCORE_KEY"] = 1
        elif "600" in split_use_case:
            row_data["FICO_SCORE_KEY"] = 2
        elif "<550" in split_use_case:
            row_data["FICO_SCORE_KEY"] = 7
        elif "<600" in split_use_case:
            row_data["FICO_SCORE_KEY"] = 6
        elif "550-600" in row_data["USE_CASE"]:
            row_data["FICO_SCORE_KEY"] = 6
        elif split_use_case[-1] == "None":
            row_data["FICO_SCORE_KEY"] = 8
        elif split_use_case[-2] == "None" and split_use_case[-1] != "None":
            row_data["FICO_SCORE_KEY"] = 0
        else:
            row_data["FICO_SCORE_KEY"] = 0

        if "PaidAuto" in row_data["USE_CASE"]:
            row_data["PRIOR_AUTO_KEY"] = 3
        else:
            row_data["PRIOR_AUTO_KEY"] = 0

        if "LTB" in row_data["USE_CASE"]:
            row_data["GOOD_CREDIT_CUSTOMER"] = "Long Term Bureau"
        elif "STB" in row_data["USE_CASE"]:
            row_data["GOOD_CREDIT_CUSTOMER"] = "Short Term Bureau"
        else:
            row_data["GOOD_CREDIT_CUSTOMER"] = "NA"
        return row_data

    def write_to_csv(self):
        self.logger.info(f"inside write_to_csv method..........")
        try:
            with open(self.file_path, mode="a", newline="") as file:
                fieldnames = [field for field in self.column_name if field != "JSON"]
                if "ID" not in fieldnames:
                    fieldnames.append("ID")
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                for row in self.csv_data:
                    if row["USE_CASE"] == "":
                        continue
                    filtered_row = {}
                    for key in self.column_name:
                        if key in row and key not in self.config_data:
                            filtered_row[key] = row[key]
                        elif key in self.config_data:
                            if (
                                isinstance(self.config_data[key], str)
                                and "," in self.config_data[key]
                            ):
                                options = self.config_data[key].split(",")
                                filtered_row[key] = random.choice(options).strip()
                            else:
                                filtered_row[key] = self.config_data[key]
                        else:
                            filtered_row[key] = ""
                    filtered_row = self.process_csv_data(filtered_row)
                    if "collateral" in self.file_path.stem.lower():
                        filtered_row = self.update_collateral_dict(filtered_row)
                    if "info" in self.file_path.stem.lower():
                        filtered_row = self.update_info_dict(filtered_row)
                    writer.writerow(filtered_row)
            self.logger.info(f"CSV file has been written to {self.file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write CSV file: {e}")

    def execute_data_loading(self):
        self.logger.info(f"inside execute_data_loading method..........")
        self.write_header_to_file()
        self.write_to_csv()
