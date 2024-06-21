import glob

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
    csv_files_path = "/Users/nikhil/Documents/Leapfrog/los-test/temp/csv_files/*.csv"
    output_excel_file = PathUtils().get_temp_folder().joinpath("los_test.xlsx")

    csv_files = glob.glob(csv_files_path)

    with pd.ExcelWriter(output_excel_file, engine="openpyxl") as writer:
        for csv_file in csv_files:
            sheet_name = csv_file.split("/")[-1].split(".")[0]
            df = pd.read_csv(csv_file)
            df.rename(columns=lambda x: " " if "Unnamed" in x else x, inplace=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    all_csv_data = LosDataExtractor().get_csv_file_content()
    applicant_data_loader.ApplicantDataLoader(all_csv_data).execute_data_loading()
    collateral_data_loader.CollateralDataLoader(all_csv_data).execute_data_loading()
    info_data_loader.InfoDataLoader(all_csv_data).execute_data_loading()
    structure_data_loader.StructureDataLoader(all_csv_data).execute_data_loading()

    # merge_csv_file_to_one()


if __name__ == "__main__":
    main()
