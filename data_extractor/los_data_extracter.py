import os
import csv
from pathlib import Path
from typing import List, Dict, Optional

from utils.logger_utils import Logger
from utils.path_utils import PathUtils


class LosDataExtractor:
    def __init__(self):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.extension = ".csv"

    def get_file_list_with_string(self, file_string: str) -> List[str]:
        """
        Searches for files in the input_files directory that contain the specified string in their names.

        Args:
            file_string (str): The substring to search for in the file names.

        Returns:
            List[str]: A list of file names that contain specified substring. Returns an empty list if no files match.
        """
        self.logger.info(
            f"inside get_file_list_with_string method..........file_string: {file_string}"
        )
        input_file_path = PathUtils().get_temp_folder().joinpath("input_files")
        return [
            file
            for file in os.listdir(input_file_path)
            if file_string in file and file.endswith(self.extension)
        ]

    def get_chosen_file(self, list_of_files: List[str]) -> Optional[Path]:
        """
        Prompts the user to choose a file from a list of file names and returns the full path of the chosen file.

        Args:
            list_of_files (List[str]): A list of file names to choose from.

        Returns:
            Optional[Path]: The full path to the chosen file as a `Path` object.
        """
        self.logger.info(f"inside get_chosen_file method..........list_of_files: {list_of_files}")

        if not list_of_files:
            self.logger.warning("No files available to choose from.")
            return None

        if len(list_of_files) == 1:
            self.logger.info("Only one file found. Automatically selecting it.")
            chosen_file = list_of_files[0]
        else:
            for index, file_name in enumerate(list_of_files, start=1):
                print(f"{index}: {file_name}")
            chosen_file = self._prompt_user_choice(list_of_files)

        chosen_file_path = PathUtils().get_temp_folder().joinpath("input_files", chosen_file)
        self.logger.info(f"Chosen file path: {chosen_file_path}")
        return chosen_file_path

    def _prompt_user_choice(self, list_of_files: List[str]) -> str:
        """
        Prompts the user to choose a file from the provided list and returns the name of the chosen file.

        Args:
            list_of_files (List[str]): A list of file names from which the user will select one.

        Returns:
            str: The name of the chosen file.
        """
        self.logger.info(
            f"inside _prompt_user_choice method..........list_of_files: {list_of_files}"
        )
        while True:
            try:
                choice = int(input("Choose the file number: "))
                if 1 <= choice <= len(list_of_files):
                    return list_of_files[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(list_of_files)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_csv_file_content(self, file_path: Path) -> List[Dict]:
        """
        Reads the content of a CSV file and returns it as a list of dictionaries.

        Args:
            file_path (Path): The path to the CSV file to be read.

        Returns:
            List[Dict]: A list of dictionaries, with each dictionary representing a row in the CSV file.
        """
        self.logger.info(f"inside get_csv_file_content method..........file_path: {file_path}")
        try:
            with open(file_path,"r", newline="") as los_file:
                csv_reader = csv.DictReader(los_file)
                return [dict(row) for row in csv_reader]
        except Exception:
            self.logger.exception("Error occurred while reading CSV file content.")
            raise

    def process_los_data_extraction(self, file_string: str) -> List[Dict]:
        """
        Processes the LOS data extraction by finding files that contain a specific string, allowing the user to choose
        one, and then reading the contents of the chosen CSV file.

        Args:
            file_string (str): The substring to search for in file names.

        Returns:
            List[Dict]: A list of dictionaries representing the rows in the chosen CSV file.
        """
        self.logger.info(
            f"inside process_los_data_extraction method..........file_string: {file_string}"
        )
        file_list = self.get_file_list_with_string(file_string)
        chosen_file = self.get_chosen_file(file_list)
        if chosen_file is None:
            self.logger.warning("No file was chosen or available, returning empty list.")
            return []
        return self.get_csv_file_content(chosen_file)
