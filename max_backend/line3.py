
def calculate_max_backend(line5_ltv_max,line3_ltv,avg_tradein_value):
    calculation = (line5_ltv_max - line3_ltv) / 100 * avg_tradein_value
    print(f'The max backend {calculation}')
    return


def main():
    line5_ltv_max = float(input("Enter the line5_ltv_max: ").strip())
    line3_ltv = float(input("Enter the line3_ltv: ").strip())
    avg_tradein_value = float(input("Enter the avg_tradein_value AF: ").strip())

    calculate_max_backend(line5_ltv_max,line3_ltv,avg_tradein_value)



if __name__ == "__main__":
    main()
