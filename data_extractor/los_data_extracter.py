import csv
from typing import List, Dict

from utils.logger_utils import Logger


class LosDataExtractor:
    def __init__(self):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()

    def get_csv_file_content(self, file_path) -> List[Dict]:
        self.logger.info(f"inside get_csv_file_content method..........los_file_path: {file_path}")
        try:
            with open(file_path, "r", newline="") as los_file:
                csv_reader = csv.DictReader(los_file)
                list_of_dicts = [dict(row) for row in csv_reader]
            return list_of_dicts
        except Exception:
            self.logger.exception(f"Error occurred while getting content from csv file.")
            raise
