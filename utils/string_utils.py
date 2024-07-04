from utils.logger_utils import Logger
from utils.path_utils import PathUtils


class StringUtils:
    def __init__(self):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()

    def get_file_with_string(self, search_string: str):
        self.logger.info(
            f"inside get_file_with_string method..........search_string: {search_string}."
        )
        # Normalize the search string to lowercase
        search_string_lower = search_string.lower()

        folder = PathUtils.get_temp_folder()
        matching_files = [
            path
            for path in folder.glob("*")
            if path.is_file() and search_string_lower in path.name.lower()
        ]
        if matching_files:
            self.logger.info(f"File found: {matching_files[0]}")
            return matching_files[0]
        else:
            self.logger.info(f"No matching file found for search string: {search_string}")
            return None
