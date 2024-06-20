from data_extractor.los_data_extracter import LosDataExtractor
from data_loader import (
    applicant_data_loader,
    collateral_data_loader,
    info_data_loader,
    structure_data_loader,
)


def main():
    all_csv_data = LosDataExtractor().get_csv_file_content()
    applicant_data_loader.ApplicantDataLoader(all_csv_data).execute_data_loading()
    collateral_data_loader.CollateralDataLoader(all_csv_data).execute_data_loading()
    info_data_loader.InfoDataLoader(all_csv_data).execute_data_loading()
    structure_data_loader.StructureDataLoader(all_csv_data).execute_data_loading()


if __name__ == "__main__":
    main()
