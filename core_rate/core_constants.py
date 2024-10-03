# Rate constants
base_rate = {
    "SC": 20.9,
    "TX": 21.99,
    "FLCL1": 21.99,
    "FLCL2": 21.99,
    "FLCL3": 21.99,
    "FLCL4": 21.99,
    "FLCL5": 21.99,
    "CA":21.99
}

state_usury_max_rate = {
    "SC": 23.9,
    "TX": 24.99,
    "FLCL1": 16.78,
    "FLCL2": 17.99,
    "FLCL3": 17.99,
    "FLCL4": 23.99,
    "FLCL5": 24.99,
    "CA":99.99
}

min_rate = 9.99
max_rate_1 = 25.49
max_rate_2=24.99

dimension_rate_adjustment = {
    "None_None": 0,
    "PaidAuto": -3,
    "AB_700LTB": -5,
    "B_700": -3,
    "A_700LTB": -4,
    "C_700STB": -3,
    "D_700": -2,
    "Mileage": 1,
    "Luxury": 1,
    "<600": 0,
    "<550": 0,
    "PaidAuto_600": -6,
    "66": 0.5,
    "72": 1.5,
    "600": -1

}


dimension_rate_adjustmentCA = {
    "039": {
        "None_None": 0,
        "PaidAuto": -3,
        "AB_700LTB": -5,
        "B_700": -3,
        "A_700LTB": -4,
        "C_700STB": -3,
        "D_700": -2,
        "Mileage": 1,
        "Luxury": 1,
        "<600": 0,
        "<550": 0,
        "PaidAuto_600": -6,
        "66": 0.5,
        "72": 1.5,
        "600": -1,
        "max_rate":24.99
    },
    "040": {
        "None_None": 0,
        "PaidAuto": -3,
        "AB_700LTB": -5,
        "B_700": -3,
        "A_700LTB": -4,
        "C_700STB": -3,
        "D_700": -2,
        "Mileage": 1,
        "Luxury": 1,
        "<600": 0,
        "<550": 0,
        "PaidAuto_600": -6,
        "66": 0.5,
        "72": 1.5,
        "600": -3,
        "max_rate":25.49
    }
}




rate_reduction = {
    "0-20": 2.50,
    "20": 2.50,
    "20.01-30": 2.00,
    "30.01-40": 1.50,
    "40.01-50": 1.00,
    "50.01-60": 0.50,
    "60.01-70": 0.00,
    "70.01-80": 0.00,
    ">80.01": 0,
}

num_rate = {
    "ITIN": {
        "None_None": 0,
        "<600": 0,
        "PaidAuto": 0,
        "PaidAuto_600":0,
        "700": 0,
        "600": 0,
        "66": -0.5,
        "72": -1,
        "72itin":0,
        "Mileage": 1,
        "Luxury": 2,
        "AB": -3,
        "A": -0.5,
        "B": -2,
        "C": 0,
        "D": 0,
        "new_<2yr_<5000miles": -1,
        "<550":0
    },
    "NoITIN": {
        "None_None": 1.5,
        "<600": 1.5,
        "PaidAuto": 0,
        "PaidAuto_600":0,
        "600": 0,
        "66": 0,
        "72": 0,
        "Mileage": 1,
        "Luxury": 2,
        "AB": -1,
        "A": 0,
        "B": -1,
        "C": 0,
        "D": 0.5,
        "new_<2yr_<5000miles": -0.5,
        "<550":2
    },
    "SSN": {
        "None_None": 2,
        "<600": 2.5,
        "PaidAuto": 0,
        "PaidAuto_600": 0.5,
        "600":0.5,
        "66": 0,
        "72": 0,
        "Mileage": 2,
        "Luxury": 3,
        "AB": 0,
        "A": 1,
        "B": 0,
        "C": 0.5,
        "D": 0.5,
        "new_<2yr_<5000miles": -0.5,
        "<550":3.5
    },
}

fl_num_rate = {
    "ITIN": {
        "None_None": 0,
        "<600": 0,
        "PaidAuto": 0,
        "PaidAuto_600":0,
        "700": 0,
        "600": 0,
        "66": 0,
        "72": 0,
        "Mileage": 1,
        "Luxury": 2,
        "AB": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "new_<2yr_<5000miles": 0,
        "<550":0,
        "72itin":0
    },
    "NoITIN": {
        "None_None": 1.5,
        "<600": 1.5,
        "PaidAuto": 0,
        "PaidAuto_600":0,
        "600": 0,
        "66": 0,
        "72": 0,
        "Mileage": 1,
        "Luxury": 2,
        "AB": -1,
        "A": 0,
        "B": -1,
        "C": 0,
        "D": 0.5,
        "new_<2yr_<5000miles": -0.5,
        "<550":2
    },
    "SSN": {
        "None_None": 2,
        "<600": 2.5,
        "PaidAuto": 0,
        "700": 0,
        "PaidAuto_600": 0.5,
        "600":0.5,
        "66": 0,
        "72": 0,
        "Mileage": 2,
        "Luxury": 3,
        "AB": 0,
        "A": 1,
        "B": 0,
        "C": 0.5,
        "D": 0.5,
        "new_<2yr_<5000miles": -0.5,
        "<550":3.5
    },
}
