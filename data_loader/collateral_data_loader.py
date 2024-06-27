from utils.logger_utils import Logger
from utils.path_utils import PathUtils
from common.csv_file_constants import collateral_column_name
from data_loader.common_data_loader import CommonDataLoader


class CollateralDataLoader(CommonDataLoader):
    def __init__(self, csv_data, input_constants):
        super().__init__()
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.config_data = input_constants.COLLATERAL_INPUT
        self.start_id = self.config_data["start_id"]

        self.column_name = collateral_column_name
        self.file_path = PathUtils().get_csv_file_path(f"Collateral.csv")
        self.csv_data = csv_data
