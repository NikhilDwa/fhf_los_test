from pathlib import Path
from common import core_constants
from bin.dump_data_to_csv import DumpDataToCsv


def main():
    dump_data_to_csv = DumpDataToCsv(core_constants)
    user_input = input("Have you updated the core constants? (Y/N)").strip().lower()
    if user_input == "y":
        try:
            file_path = dump_data_to_csv.get_file_with_string("core")
            if file_path:
                dump_data_to_csv.get_data_load_csv(file_path)
                core_info_data = core_constants.INFO_INPUT
                output_file_path = Path(
                    f"core_{core_info_data['REGISTRATION_STATE']}_{core_info_data['APPLICATION_TIN_TYPE']}"
                )
                dump_data_to_csv.merge_csv_file_to_one(output_file_path)
                print("CSV files merged successfully.")
            else:
                print("No file found with 'core' in the name.")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif user_input == "n":
        print("Please update the constants file and run again.")
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")


if __name__ == "__main__":
    main()
