import constant as c


def get_user_input(prompt, value_type=str):
    while True:
        try:
            value = input(prompt)
            return value_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {value_type.__name__}.")


def calculate_ltv():
    loan_program_id = get_user_input("Enter Loan Program ID (039 or 040): ")
    vehicle_type = get_user_input("Enter Vehicle Type (new/used): ").lower()
    total_cash_price = get_user_input("Enter Total Cash Price: ", float)
    testcase = get_user_input("Enter TESTCASE (SSN, NoITIN, 700, 600, Luxury, PaidAuto, etc.): ")
    term = get_user_input("Enter Term (e.g., 72 for 72 months): ")
    state = get_user_input("Enter State (2-letter code, e.g., CA, TX): ")

    final_ltvmax = 0

    if loan_program_id in c.base_rate_Line3 and vehicle_type in c.base_rate_Line3[loan_program_id]:
        final_ltvmax = c.base_rate_Line3[loan_program_id][vehicle_type]
        line3ltv_totalCashprice = c.total_Cash_Price[loan_program_id]
        line3_ltv_adjustment = c.line3_ltv_adjustment[loan_program_id]
    else:
        print("Invalid Loan Program ID or Vehicle Type.")
        return

    # Cash Price Adjustments
    if total_cash_price <= 32000:
        final_ltvmax += line3ltv_totalCashprice["0-32000"]
    elif 32001 <= total_cash_price <= 42000:
        final_ltvmax += line3ltv_totalCashprice["32001-42000"]
    elif 42001 <= total_cash_price <= 57000:
        final_ltvmax += line3ltv_totalCashprice["42001-57000"]
    elif 57001 <= total_cash_price <= 72000:
        final_ltvmax += line3ltv_totalCashprice["57001-72000"]
    elif total_cash_price > 72000:
        final_ltvmax += line3ltv_totalCashprice["72001-99000"]

    # Adjustments based on TESTCASE
    for key in line3_ltv_adjustment:
        if key in testcase:
            final_ltvmax += line3_ltv_adjustment[key]

    # State-Based Adjustments
    JBstates = ["IL", "MI", "CT", "MD", "VA", "NJ", "NH", "PA", "MA", "SC", "NC", "DE", "GA", "WI", "TN", "IN", "KY",
                "OH", "OK", "NY", "FL", "TX", "AL"]
    KBstates = ["CO", "ID", "NV", "UT", "OR", "WA", "AZ", "CA"]

    if state in JBstates and vehicle_type == "new":
        final_ltvmax += 3
    elif state in KBstates:
        final_ltvmax += 3

    final_ltvmax = round(final_ltvmax, 2)
    print(f"Final LTV Max: {final_ltvmax}")


if __name__ == "__main__":
    calculate_ltv()