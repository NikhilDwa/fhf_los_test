
def calculate_max_second_auto_addons(interest_rate, term, second_auto_payment, vehicle_af, vsi):

    x = (1 + interest_rate) ** term
    max_amount_financed = (second_auto_payment * 1.1) * (x - 1) / (interest_rate * x)
    print(max(max_amount_financed - vehicle_af - vsi, 0))
    return

def main():
    interest_rate = float(input("Enter the annual interest rate as a percentage (e.g., 5 for 5%): ").strip()) / 12 / 100
    term = int(input("Enter the term (in months): ").strip())
    vehicle_af = float(input("Enter the vehicle AF: ").strip())
    second_auto_payment = float(input("Enter the second_auto_payment: ").strip())
    vsi = float(input("Enter the VSI: ").strip())
    calculate_max_second_auto_addons(interest_rate, term, second_auto_payment, vehicle_af,vsi)



if __name__ == "__main__":
    main()
