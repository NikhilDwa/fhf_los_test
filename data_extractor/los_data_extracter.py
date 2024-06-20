import csv
from typing import List, Dict

from utils.logger_utils import Logger
from utils.path_utils import PathUtils


class LosDataExtractor:
    def __init__(self):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        config: dict = PathUtils().get_configuration()
        self.los_file_path: dict = config["LOS_FILE_PATH"]

    def get_csv_file_content(self) -> List[Dict]:
        self.logger.info(f"inside get_csv_file_content method..........")
        try:
            with open(self.los_file_path["file_path"], "r", newline="") as los_file:
                csv_reader = csv.DictReader(los_file)
                list_of_dicts = [dict(row) for row in csv_reader]
            return list_of_dicts
        except Exception:
            self.logger.exception(f"Error occurred while getting content from csv file.")
            raise
