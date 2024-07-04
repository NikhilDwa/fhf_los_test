from pathlib import Path
from datetime import datetime

from utils.path_utils import PathUtils
from utils.string_utils import StringUtils
from data_extractor.los_data_extracter import LosDataExtractor
from services.usecase_to_data_generate_service import UseCaseToDataGenerateService


def main():
    user_input = input("Have you updated the asp use cases? (Y/N)").strip().lower()
    if user_input == "y":
        try:
            file_path = StringUtils().get_file_with_string("apr")
            if file_path:
                all_csv_data = LosDataExtractor().get_csv_file_content(file_path)
                today_date = datetime.now().strftime("%Y%m%d_%H%M%S%f")
                output_file_path = PathUtils.get_output_folder().joinpath(
                    Path(f"asp_acceptance_{today_date}.csv")
                )
                UseCaseToDataGenerateService(
                    output_file_path, all_csv_data
                ).generate_use_case_data()

        except Exception as e:
            print(f"An error occurred: {e}")
    elif user_input == "n":
        print("Please update the file and run again.")
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")


if __name__ == "__main__":
    main()
