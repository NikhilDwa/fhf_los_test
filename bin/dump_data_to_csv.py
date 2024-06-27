import glob
from pathlib import Path
from datetime import datetime

import pandas as pd

from utils.logger_utils import Logger
from utils.path_utils import PathUtils
from data_extractor.los_data_extracter import LosDataExtractor
from data_loader import (
    applicant_data_loader,
    collateral_data_loader,
    info_data_loader,
    structure_data_loader,
)


class DumpDataToCsv:
    def __init__(self, los_constants):
        log_namespace = self.__class__.__name__
        self.logger = Logger(log_namespace, f"{log_namespace}.log").get()
        self.los_constants = los_constants

    def get_file_with_string(self, search_string: str) -> Path | None:
        self.logger.info(
            f"Inside get_file_with_string method..........search_string: {search_string}."
        )
        folder = PathUtils.get_temp_folder()
        pattern = f"*{search_string}*"
        matching_files = [path for path in folder.glob(pattern) if path.is_file()]
        if matching_files:
            self.logger.info(f"File found: {matching_files[0]}")
            return matching_files[0]
        else:
            self.logger.info(f"No matching file found for search string: {search_string}")
            return None

    def get_data_load_csv(self, file_path: Path) -> None:
        self.logger.info(f"Inside get_data_load_csv method..........file_path: {file_path}.")
        try:
            all_csv_data = LosDataExtractor().get_csv_file_content(file_path)

            applicant_data_loader.ApplicantDataLoader(
                all_csv_data, self.los_constants
            ).execute_data_loading()
            collateral_data_loader.CollateralDataLoader(
                all_csv_data, self.los_constants
            ).execute_data_loading()
            info_data_loader.InfoDataLoader(
                all_csv_data, self.los_constants
            ).execute_data_loading()
            structure_data_loader.StructureDataLoader(
                all_csv_data, self.los_constants
            ).execute_data_loading()

        except Exception:
            self.logger.exception(
                f"An error occurred while loading CSV data from file {file_path}"
            )

    def merge_csv_file_to_one(self, output_file_path: Path) -> None:
        self.logger.info(
            f"Inside merge_csv_file_to_one method.........output_file_path: {output_file_path}."
        )
        try:
            csv_files_path = PathUtils.get_temp_folder().joinpath("csv_files/*.csv")
            today_date = datetime.now().strftime("%Y%m%d_%H%M%S%f")
            output_file_name = f"{output_file_path.stem}_{today_date}.xlsx".replace(
                " ", "_"
            ).lower()
            output_excel_file = PathUtils().get_output_folder().joinpath(output_file_name)

            csv_files = [Path(path.replace("\\", "/")) for path in glob.glob(str(csv_files_path))]

            with pd.ExcelWriter(output_excel_file, engine="openpyxl") as writer:
                for csv_file in csv_files:
                    sheet_name = csv_file.stem
                    df = pd.read_csv(csv_file)
                    df.rename(columns=lambda x: " " if "Unnamed" in x else x, inplace=True)
                    df.loc[1:, :] = df.loc[1:, :].fillna("NA")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            self.logger.info(f"CSV files merged successfully into {output_excel_file}")

        except Exception as e:
            self.logger.error(f"An error occurred while merging CSV files: {e}")
