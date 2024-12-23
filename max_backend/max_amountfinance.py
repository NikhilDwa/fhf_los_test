from math import floor

def calculate_max_backend(max_amount_financed,current_amount_financed):
    allowed_max_backend = max_amount_financed - current_amount_financed
    calculated_max_backend = int(floor(allowed_max_backend / 50)) * 50
    print(f'The max backend {calculated_max_backend}')
    return


def main():
    max_amount_financed = float(input("Enter the max_amount_financed: ").strip())
    current_amount_financed = float(input("Enter the current_amount_financed: ").strip())


    calculate_max_backend(max_amount_financed,current_amount_financed)



if __name__ == "__main__":
    main()
