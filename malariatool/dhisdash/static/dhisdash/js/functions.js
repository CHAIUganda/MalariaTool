

var getComputeResult = function(d) {
    return d.result;
}

var computeHelper = function(result, numerator, denominator) {
    result = isFinite(result) ? result : 0.0;
    
    return {result: result.toFixed(1),
        numerator: numberWithCommas(numerator),
        denominator: numberWithCommas(denominator)
    }
}

var computeHelperPostivityRate = function(result, numerator, denominator, rdt, microscopy) {
    result = isFinite(result) ? result : 0.0;

    return {result: result.toFixed(1),
        numerator: numberWithCommas(numerator),
        denominator: numberWithCommas(denominator),
        rdt: numberWithCommas(rdt),
        microscopy: numberWithCommas(microscopy)
    }
}

var computeHelperTestingRate = function(test_rate, test_positivity_rate, test_negative_treated_rate, total_tested, tested_positive, tested_negative, total_suspected, tested_negative_treated) {
    test_rate = isFinite(test_rate) ? test_rate : 0.0;
    test_positivity_rate = isFinite(test_positivity_rate) ? test_positivity_rate : 0.0;
    test_negative_treated_rate = isFinite(test_negative_treated_rate) ? test_negative_treated_rate : 0.0;

    return {test_rate: test_rate.toFixed(1),
        test_positivity_rate: test_positivity_rate.toFixed(1),
        test_negative_treated_rate: test_negative_treated_rate.toFixed(1),
        total_tested: numberWithCommas(total_tested),
        tested_positive: numberWithCommas(tested_positive),
        tested_negative: numberWithCommas(tested_negative),
        total_suspected: numberWithCommas(total_suspected),
        tested_negative_treated: numberWithCommas(tested_negative_treated)
    }
}

var computeMalariaDeathRate = function(data) {
    var rate = (data['inpatient_malaria_deaths'] / data['malaria_admissions']) * 100;
    return computeHelper(rate, data['inpatient_malaria_deaths'], data['malaria_admissions']);
}

var computeMortalityRate = function(data) {
    var rate = (data['inpatient_malaria_deaths']/ data['total_inpatient_deaths']) * 100;
    return computeHelper(rate, data['inpatient_malaria_deaths'], data['total_inpatient_deaths']);
}

var computeMalariaCases = function(data) {
    var rate = (data['opd_malaria_cases']/ data['population']) * 100;
    return computeHelper(rate, data['opd_malaria_cases'], data['population']);
}

var computeWeeklyMalariaCases = function(data) {
    var rate = (data['malaria_cases_wep']/ data['population']) * 1000;
    return computeHelper(rate, data['malaria_cases_wep'], data['population']);
}

var computeWeeklyPositivityRate = function(data) {
    var rate = (data['number_tested_positive'] / data['number_tested']) * 100;
    return computeHelper(rate, data['number_tested_positive'], data['number_tested']);
}

var computePositivityRate = function(data) {
    var number_tested = (data['rdt_done'] + data['microscopy_done']);
    var total_positive = (data['rdt_positive'] + data['microscopy_positive']);
    var positivity_rate = (total_positive / number_tested) * 100;

    return computeHelperPostivityRate(positivity_rate, total_positive, number_tested, data['rdt_done'], data['microscopy_done']);
};

var computeWeeklyTestingRate = function(data) {
    var total_tested = (data['number_tested']);
    var total_suspected = (data['number_suspected']);
    var tested_positive = (data['number_tested_positive']);
    var tested_negative = (data['number_tested'] - data['number_tested_positive']);
    var tested_negative_treated = (data['number_treated_tested_negative']);
    var test_rate = (total_tested / total_suspected) * 100;
    var test_positivity_rate = (tested_positive / total_tested) * 100;
    var test_negative_treated_rate = (tested_negative_treated / tested_negative) * 100;

    return computeHelperTestingRate(test_rate, test_positivity_rate, test_negative_treated_rate, total_tested, tested_positive, tested_negative, total_suspected, tested_negative_treated);
};

var computeIPT2Uptake = function(data) {
    var rate = (data['number_receiving_ipt2']/ data['number_attending_anc1']) * 100;
    return computeHelper(rate, data['number_receiving_ipt2'], data['number_attending_anc1']);
};

var computeSPStockStatus = function(data) {
    var rate = (data['stock_outs_of_sp']/ data['submitted_sp']) * 100;
    return computeHelper(rate, data['stock_outs_of_sp'], data['submitted_sp']);
};

var computeACTStockStatus = function(data) {
    var rate = (data['stock_outs_of_act']/ data['submitted_act']) * 100;
    return computeHelper(rate, data['stock_outs_of_act'], data['submitted_act']);
};

/*var computeRDTStockStatus = function(data) {
    var rate = (data['stock_outs_of_rdt']/ data['submitted_rdt']) * 100;
    return computeHelper(rate, data['stock_outs_of_rdt'], data['submitted_rdt']);
};*/

var computeTestingRate = function(data) {
    var tests_done = (data['rdt_done'] + data['microscopy_done']);
    var testing_rate = (tests_done / data['opd_malaria_total']) * 100;
    if (isNaN(testing_rate)) testing_rate = 0;

    return {testing_rate: testing_rate.toFixed(1), total_tests : tests_done};
};

var computeConsumptionRate = function(data) {
    act_consumed = (data['act_consumed'] == undefined) ? 0 : data['act_consumed'];
    opd_malaria_total = (data['opd_malaria_total_all_ages'] == undefined) ? 0 : data['opd_malaria_total_all_ages'];
    act_consumed_weighted = act_consumed / 17;

    ratio_big = Math.round(Number(act_consumed_weighted / opd_malaria_total));
    if (isNaN(ratio_big)) ratio_big = 0;

    ratio = ratio_big + ":1";
    percentage = (act_consumed_weighted / opd_malaria_total) * 100;

    return {ratio: ratio, percentage: percentage.toFixed(1), act_consumed: act_consumed};
};

var computeIPT1 = function(data) {
    if ((data['a6_first_dose'] == undefined) || (data['a1_first_visit'] == undefined)) {
        return 0;
    }

    result = (data['a6_first_dose'] / data['a1_first_visit']) * 100;
    return result.toFixed(1);
};

var computeIPT2 = function(data) {
    if ((data['a7_first_dose'] == undefined) || (data['a1_first_visit'] == undefined)) {
        return 0;
    }

    result = (data['a7_first_dose'] / data['a1_first_visit']) * 100;
    return result.toFixed(1);
};

var computeTotalPositive = function(data) {
    return data['rdt_positive'] + data['microscopy_positive'];
};

var computeTotalTreated = function(data) {
    return data['malaria_treated'];
};



var count=function(json_obj){
    return Object.keys(json_obj).length;
}

function numberWithCommas(x) {
    if (x == undefined) return 0;
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var isMonthPeriod = function(period) {
    if (period[4] == 'W') {
        return false;
    }
    return true;
}

var generateLabelFromPeriod = function(period) {
    year = period.substr(2,2);
    month = Number(period.substr(4,2));

    var months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
    return months[month] + "'"+year;
};

var generateLabelFromWeeklyPeriod = function(period, data) {
    if (! isMonthPeriod(period)) {
        return data['months_from_weeks'];
    }
}

var getPeriodString = function(year, month) {
    if (month < 10) {
        return year + "0" + month;
    } else {
        return year + "" +  month;
    }
};

var getDefaultPeriods = function() {
    var date = new Date();
    current_month = date.getMonth()+1;
    current_year = date.getFullYear();

    return {
        to: getPeriodString(current_year, current_month),
        from: getPeriodString(current_year-1, current_month)
    };
};