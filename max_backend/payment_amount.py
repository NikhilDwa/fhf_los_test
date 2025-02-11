def calculate_amortization_amount(principal, interest_rate, period):

    interest_rate = interest_rate / 12 / 100
    x = (1 + interest_rate) ** period
    payment_amount = principal * (interest_rate * x) / (x - 1)
    print(f'The amortization amount per period is {payment_amount}')
    return


def main():
    principal = float(input("Enter the Amount finance amount: ").strip())
    interest_rate = float(input("Enter the annual interest rate (as percentage): ").strip())
    period = int(input("Enter the total number of terms: ").strip())

    calculate_amortization_amount(principal, interest_rate, period)


if __name__ == "__main__":
    main()
