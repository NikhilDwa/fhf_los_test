from common.core_constants import INFO_INPUT
from utils.logger_utils import Logger
from utils.path_utils import PathUtils
from common.constants import RESULT
from common.file_headers import result_column_name
from data_loader.common_data_loader import CommonDataLoader


class ResultDataLoader(CommonDataLoader):
    def __init__(self, csv_data, input_constants):
        super().__init__()
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.start_id = INFO_INPUT["start_id"]

        self.column_name = result_column_name
        self.config_data = {}
        self.file_path = PathUtils().get_csv_file_path(RESULT)
        self.csv_data = csv_data
