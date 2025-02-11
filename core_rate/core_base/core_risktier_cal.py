import csv
from pathlib import Path


def calculate_risk_tier(average_fico_score, customer_tier, paid_auto, customer_merged_score):

    if customer_merged_score >= 670:
        merged_score_range = ">=670"
    elif 650 <= customer_merged_score <= 669:
        merged_score_range = "[650..669]"
    elif 620 <= customer_merged_score <= 649:
        merged_score_range = "[620..649]"
    elif 580 <= customer_merged_score <= 619:
        merged_score_range = "[580..619]"
    elif customer_merged_score < 580:
        merged_score_range = "<580"
    else:
        merged_score_range = "Unknown"


    if average_fico_score >= 700:
        if customer_tier in ["Long Term Bureau", "Short Term Bureau", "NA"]:
            if paid_auto == 3:
                if merged_score_range == ">=670":
                    return 1
                elif merged_score_range == "[650..669]":
                    return 1
                elif merged_score_range == "[620..649]":
                    return 2
                elif merged_score_range == "[580..619]":
                    return 3
                else:
                    return 4
            else:
                if merged_score_range == ">=670":
                    return 1
                elif merged_score_range == "[650..669]":
                    return 2
                elif merged_score_range == "[620..649]":
                    return 3
                elif merged_score_range == "[580..619]":
                    return 4
                else:
                    return 4
    elif 650 <= average_fico_score <= 699:
        if merged_score_range == ">=670":
            return 1
        elif merged_score_range == "[650..669]":
            return 2
        elif merged_score_range == "[620..649]":
            return 3
        elif merged_score_range == "[580..619]":
            return 4
        else:
            return 4
    elif 600 <= average_fico_score <= 649:
        if merged_score_range == ">=670":
            return 2
        elif merged_score_range == "[650..669]":
            return 3
        elif merged_score_range == "[620..649]":
            return 4
        elif merged_score_range == "[580..619]":
            return 4
        else:
            return 5
    elif 550 <= average_fico_score <= 599:
        if merged_score_range == ">=670":
            return 4
        elif merged_score_range == "[650..669]":
            return 4
        elif merged_score_range == "[620..649]":
            return 5
        elif merged_score_range == "[580..619]":
            return 5
        else:
            return 5
    else:
        if merged_score_range == ">=670":
            return 3
        elif merged_score_range == "[650..669]":
            return 4
        elif merged_score_range == "[620..649]":
            return 4
        elif merged_score_range == "[580..619]":
            return 5
        else:
            return 5

# Input and output file paths
input_file_name = "Scorecard Logic-Test File.csv"
output_file_name = "risk_tier_output.csv"

base_path = Path(__file__).resolve().parent
file_path = base_path.joinpath(input_file_name)

# Read input CSV file
with open(file_path, "r", newline="") as input_file:
    csv_reader = csv.DictReader(input_file)
    csv_data = [dict(row) for row in csv_reader]

# Calculate Risk Tier for each row
final_risk_tiers = []
for row in csv_data:
    average_fico_score = int(row["AverageFicoScore"])
    customer_tier = row["CustomerTier"]
    paid_auto = int(row["Paidauto"])
    customer_merged_score = int(row["CustomerMergedScore"])

    risk_tier = calculate_risk_tier(average_fico_score, customer_tier, paid_auto, customer_merged_score)

    final_risk_tiers.append({
        "TESTCASE": row["TESTCASE"],
        "AverageFicoScore": average_fico_score,
        "CustomerTier": customer_tier,
        "PaidAuto": paid_auto,
        "CustomerMergedScore": customer_merged_score,
        "RiskTier": "{'risk_tier': " + str(risk_tier) + "}",
    })

# Write output CSV file
with open(output_file_name, mode="w", newline="") as output_file:
    fieldnames = ["TESTCASE", "AverageFicoScore", "CustomerTier", "PaidAuto", "CustomerMergedScore", "RiskTier"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(final_risk_tiers)

print(f"Risk Tier calculation completed. Results saved to {output_file_name}")