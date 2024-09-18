import csv

from common.core_result import *
from data_extractor.los_data_extracter import LosDataExtractor

filepath = "C:/Users/Leapfrog/fhf_los_test/temp/core_acceptance_test.csv"



def nthSubStringIndex(s, str, n):
    sep = s.split(str, n)
    if len(sep) <= n:
        return -1
    return len(s) - len(sep[-1]) - len(str)

def testcasedata(testname,age,term,vectype,milage):
    #print(testname)
    testcasename_split = testname.split('_')
    state_name = testcasename_split[0]
    identityno = testcasename_split[1]
    range = testcasename_split[3]
    is_milage = "mileage" in testcasename_split[4].casefold()
    is_luxury = "luxury" in testcasename_split[4].casefold()
    fifth_location = nthSubStringIndex(testname,'_', 5)+1
    fico_score = testname[fifth_location:]
    data = {
        "state_name": state_name,
        "identityno":identityno,
        "range":range,
        "is_milage":is_milage,
        "is_luxury":is_luxury,
        "fico_score":fico_score,
        "age":age,
        "term":term,
        "vectype":vectype,
        "milage":milage

    }
    return data

def RunCoreLogic(id):
    csv_data = LosDataExtractor().get_csv_file_content(filepath)
    writedata = []
    for c in csv_data:
        testdata = testcasedata(c["USE_CASE"], c["VEHICLE_YEAR"], c["REQUESTED_TERM"], c["VEHICLE_CONDITION"], c["MILEAGE"])
        rate = base_rate[testdata["state_name"]]
        if (testdata["is_milage"]):
            rate = rate + rateadjustment["Mileage"]
        if (testdata["is_luxury"]):
            rate = rate + rateadjustment["Luxury"]
        #print(testdata["fico_score"])
        ra = rateadjustment[testdata["fico_score"]]
        rate = rate + ra

        ra = rateadjustment.get(testdata["term"])
        if (ra is not None):
            rate = rate + ra

        type = testdata["identityno"]
        if testdata["state_name"] in ["FLCL1", "FLCL2", "FLCL3", "FLCL4", "FLCL5"]:
            rates = flnumrate[type]
        else:
            rates = numrate[type]
        fico_score_splitted = testdata["fico_score"].split("_")
        if (testdata["fico_score"] == "None"):
            rate = rate + rates["None"]
        if ("<600" in testdata["fico_score"]):
            rate = rate + rates["<600"]
        elif ("600" in testdata["fico_score"]):
            rate = rate + rates["600"]

        if ("700" in testdata["fico_score"]):
            rate = rate + rates["700"]

        if ("A" in fico_score_splitted):
            rate = rate + rates["A"]
        if ("B" in fico_score_splitted):
            rate = rate + rates["B"]
        if ("C" in fico_score_splitted):
            rate = rate + rates["C"]
        if ("D" in fico_score_splitted):
            rate = rate + rates["D"]
        if ("AB" in fico_score_splitted):
            rate = rate + rates["AB"]

        if (testdata["is_milage"]):
            rate = rate + rates["Milage"]
        if (testdata["is_luxury"]):
            rate = rate + rates["Luxury"]
        if (testdata["term"] == 66 or testdata["term"] == 72):
            rate = rate + rates[testdata["term"]]

        if (testdata["vectype"] == "New" and testdata["milage"] < "5000" and (
                testdata["age"] == "2024" or testdata["age"] == "2025")):
            rate = rate + rates["new"]

        ra = ltb_rate_reduction[testdata["range"]]
        rate = rate - ra
        rate = max(min_rate, rate)
        rate = min(max_rate, rate)
        rate = min(state_usary_rate[testdata["state_name"]], rate)
        writedata.append({
            "ID": id,
            "USE_CASE": c["USE_CASE"],
            "RESULT": f"{{'interest_rate':{rate:0.2f}}}"
        })
        id = id + 1
    return writedata
#RunCoreLogic(1)