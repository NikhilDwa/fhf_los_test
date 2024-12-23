import requests

# TestRail API credentials and endpoint configuration
BASE_URL = "https://firsthelpfinancial.testrail.io/index.php?/projects/overview/7"
USERNAME = "anujpokharel@lftechnology"
PASSWORD = "Pogba@2055"
RUN_ID = "https://firsthelpfinancial.testrail.io/index.php?/tests/view/24914"

# Sample email content
email_content = """
Passed Tests
Test Case CA_NoITIN_LTV3_0-20_Luxury_600 DPMIN Passed
Test Case CA_NoITIN_LTV3_0-20_Luxury_AB_700LTB_PaidAuto DPMIN Passed
Test Case CA_NoITIN_LTV3_0-20_Luxury_A_700LTB DPMIN Passed
Test Case CA_NoITIN_LTV3_0-20_Luxury_B_700_PaidAuto DPMIN Passed
Test Case CA_NoITIN_LTV3_0-20_Luxury_C_700STB DPMIN Passed
Failed Tests
Test Case CA_NoITIN_LTV3_0-40_Luxury_A_700LTB DPMIN Failed
Test Case CA_NoITIN_LTV3_0-40_Luxury_B_700_PaidAuto DPMIN Failed
"""


# Parse email content
def parse_test_results(content):
    passed_tests = []
    failed_tests = []
    lines = content.strip().split('\n')
    passed_section = False
    failed_section = False

    for line in lines:
        if "Passed Tests" in line:
            passed_section = True
            failed_section = False
            continue
        elif "Failed Tests" in line:
            passed_section = False
            failed_section = True
            continue

        if passed_section and "Passed" in line:
            test_case = line.split(" Passed")[0].strip()
            passed_tests.append(test_case)
        elif failed_section and "Failed" in line:
            test_case = line.split(" Failed")[0].strip()
            failed_tests.append(test_case)

    return passed_tests, failed_tests


# Update test results in TestRail
def update_testrail(run_id, test_cases, status_id, note):
    for test_case in test_cases:
        # Find test ID by test case title (adjust if necessary)
        # For simplicity, assume `test_case` matches the TestRail case ID or title
        payload = {
            "status_id": status_id,
            "comment": note
        }
        response = requests.post(
            f"{BASE_URL}add_result_for_case/{run_id}/{test_case}",
            auth=(USERNAME, PASSWORD),
            json=payload
        )
        if response.status_code == 200:
            print(f"Test Case '{test_case}' updated successfully.")
        else:
            print(f"Failed to update Test Case '{test_case}'. Status code: {response.status_code}")


# Main function
def main():
    passed_tests, failed_tests = parse_test_results(email_content)

    # Add notes for passed and failed tests
    passed_note = f"These test cases passed: {', '.join(passed_tests)}"
    failed_note = f"These test cases failed: {', '.join(failed_tests)}"

    # Update TestRail for passed tests (status_id = 1 for 'Passed')
    update_testrail(RUN_ID, passed_tests, status_id=1, note=passed_note)

    # Update TestRail for failed tests (status_id = 5 for 'Failed')
    update_testrail(RUN_ID, failed_tests, status_id=5, note=failed_note)


# Run the main function
if __name__ == "__main__":
    main()
