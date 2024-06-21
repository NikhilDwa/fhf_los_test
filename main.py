import glob
from datetime import datetime

import pandas as pd

from utils.path_utils import PathUtils
from data_extractor.los_data_extracter import LosDataExtractor
from data_loader import (
    applicant_data_loader,
    collateral_data_loader,
    info_data_loader,
    structure_data_loader,
)


def merge_csv_file_to_one():
    config: dict = PathUtils().get_configuration()
    config_data: dict = config["INFO_INPUT"]

    csv_files_path = "/Users/nikhil/Documents/Leapfrog/los-test/temp/csv_files/*.csv"
    today_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{config_data['REGISTRATION_STATE']}_{config_data['APPLICATION_TIN_TYPE']}_{today_date}.xlsx"
    output_excel_file = PathUtils().get_temp_folder().joinpath(output_file_name)

    csv_files = glob.glob(csv_files_path)

    with pd.ExcelWriter(output_excel_file, engine="openpyxl") as writer:
        for csv_file in csv_files:
            sheet_name = csv_file.split("/")[-1].split(".")[0]
            df = pd.read_csv(csv_file)
            df.rename(columns=lambda x: " " if "Unnamed" in x else x, inplace=True)
            df.iloc[1:].fillna("NA", inplace=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    user_input = input("Have to updated config data? (Y/N)")
    if user_input == "Y" or user_input == "y":
        all_csv_data = LosDataExtractor().get_csv_file_content()
        applicant_data_loader.ApplicantDataLoader(all_csv_data).execute_data_loading()
        collateral_data_loader.CollateralDataLoader(all_csv_data).execute_data_loading()
        info_data_loader.InfoDataLoader(all_csv_data).execute_data_loading()
        structure_data_loader.StructureDataLoader(all_csv_data).execute_data_loading()

        merge_csv_file_to_one()
    else:
        print("Please, update the config file and run again.")


if __name__ == "__main__":
    main()
