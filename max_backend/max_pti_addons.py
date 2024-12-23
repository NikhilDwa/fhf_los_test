
def calculate_max_pti_addon(interest_rate, term, combined_gmi, vehicle_af, vsi):

    #pti = 0.3
    pti = 0.22 #independent and franchise is also 0.22 when GPS is 2.0

    x = (1 + interest_rate) ** term
    max_amount_financed = pti * combined_gmi * (x - 1) / (interest_rate * x)
    max_pti_allowed_addons = max(max_amount_financed - vehicle_af - vsi, 0)
    print(f'The max pti allowed addons {max_pti_allowed_addons}')
    return

def main():
    interest_rate = float(input("Enter the annual interest rate as a percentage (e.g., 5 for 5%): ").strip()) / 12 / 100
    term = int(input("Enter the term (in months): ").strip())
    combined_gmi = float(input("Enter the combined GMI: ").strip())
    vehicle_af = float(input("Enter the vehicle AF: ").strip())
    vsi = float(input("Enter the VSI: ").strip())

    calculate_max_pti_addon(interest_rate, term, combined_gmi, vehicle_af, vsi)



if __name__ == "__main__":
    main()
