# main.py
from math import floor
from constant import core_max_backend_limiting_factors

def interim_max_backend(core_data, is_franchise, rate):
    base_backend = (
        core_data["base_backend_franchise"]
        if is_franchise
        else core_data["base_backend_independent"]
    )

    vehicle_value_threshold = core_data["vehicle_value_threshold"]

    avg_tradein_value = float(input("Please enter average tradein value?:"))

    increment_on_base_value = (
        0
        if avg_tradein_value <= vehicle_value_threshold
        else (avg_tradein_value - vehicle_value_threshold) / 10
    )
    backend_based_on_vehicle_threshold = base_backend + increment_on_base_value
    backend_based_on_rate = rate * avg_tradein_value

    interim_backend  =min(backend_based_on_vehicle_threshold, backend_based_on_rate)
    calculated_max_backend = int(floor(interim_backend / 50)) * 50
    print(f'The interim max backend is : {calculated_max_backend}')
    return


def fico_score_paid_auto_calculation(core_data):
    franchise_type = "false"
    paid_auto = 0

    is_franchise = input("Is franchise? yes/no:").strip().lower() == "yes"

    if is_franchise:
        franchise_type = "true"

    application_tin_type = input("What is the ssn no? ssn/itin/no itin").lower()
    paid_auto = 3 if input("Is paid auto? yes/no:").lower() == "yes" else 0

    key = franchise_type + "," + application_tin_type + "," + str(paid_auto)
    print(key)
    rate = core_data['for_fico_700_plus_and_paid_auto'].get(key, 0)
    interim_max_backend(core_data, is_franchise, rate)


def paid_auto_calculation(core_data):
    franchise_type = "false"
    paid_auto = 3 if input("Is paid auto? yes/no:").lower() == "yes" else 0

    is_franchise = input("Is franchise? yes/no:").strip().lower() == "yes"
    if is_franchise:
        franchise_type = "true"

    application_tin_type = input("What is the ssn no? ssn/itin/no itin").lower()
    key = franchise_type + "," + application_tin_type + "," + str(paid_auto)
    print(key)
    rate = core_data['for_paid_auto'].get(key, 0)
    interim_max_backend(core_data, is_franchise, rate)


def fico_score_calculation(core_data):
    franchise_type = "false"
    is_franchise = input("Is franchise? yes/no:").strip().lower() == "yes"
    if is_franchise:
        franchise_type = "true"

    application_tin_type = input("What is the ssn no? ssn/itin/no itin").lower()
    fico_score = input("What is your FICO score:").lower()
    key = franchise_type + "," + application_tin_type + "," + fico_score
    print(key)
    rate = core_data['for_fico_score'].get(key, 0)
    interim_max_backend(core_data, is_franchise, rate)

def is_fico_eligible():
    fico = "700" or ("600-700" and "Paid Auto")



def main():
    version = input("Enter the version (40 or 41): ")
    core_data = core_max_backend_limiting_factors.get(version)

    if not core_data:
        print("Invalid version entered. Exiting.")
        return

    if input("Is the FICO score 700 or above and Paid Auto type 3? (yes/no): ").lower() == 'yes':
        fico_score_paid_auto_calculation(core_data)
    elif input("Is the paid auto (yes/no): ").strip().lower() == 'yes':
        paid_auto_calculation(core_data)
    elif input("Is the FICO score (yes/no): ").strip().lower() == 'yes':
        fico_score_calculation(core_data)
    else:
        print("No valid calculation selected.")


if __name__ == "__main__":
    main()
