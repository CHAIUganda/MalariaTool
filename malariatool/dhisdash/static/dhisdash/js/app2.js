var app = angular.module('dashboard', ['datatables'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('<%');
    $interpolateProvider.endSymbol('%>');
});

$(document).ready(function(){
    $('.tabs .desc').tooltip( {
		delay: {show: 2000},
		track: true,
		fade: 250,
		container: 'body',
		placement: 'bottom'
	} );
});

app.controller('DashboardController', function($scope, $http) {
    $scope.filter = {
        from_date: "0",
        to_date: "0",
        region: "0",
        district: "0",
        age_group: "0",
    };

    default_periods = getDefaultPeriods();
    $scope.filter.from_date = default_periods.from
    $scope.filter.to_date = default_periods.to

    $scope.positivity_rate_results = {}
    $scope.big_metric = {};

    $scope.big_metric.positivity_rate = "0%";
    $scope.big_metric.testing_rate = "0%";
    $scope.big_metric.consumption_rate = "0:0";
    $scope.big_metric.IPT1 = "0%";
    $scope.big_metric.IPT2 = "0%";
    $scope.big_metric.total_positive = "0";
    $scope.big_metric.total_treated = "0";

    $http.get('../../districts.json', {})
        .then(function(response) {
            $scope.districts = response.data;
        }, function (response) {
            console.log(response);
    });

    $scope.showReg=function(option_index){
        $('.toggle-option').removeClass('active');
        $('#toggle-option-'+option_index).addClass('active');
    }

    $scope.updateData = function() {

        params = 'from_date='+$scope.filter.from_date+
            '&to_date='+$scope.filter.to_date+
            '&region='+$scope.filter.region+
            '&district='+$scope.filter.district+
            '&age_group='+$scope.filter.age_group;

        $http.get('../../data.json?'+params+'&group=district', {})
            .then(function (response) {
                $scope.data_table_results = [];

                var positivity_data = [];
                var testing_data= [];
                var consumption_data = [];

                for (district in response.data) {

                    pr_result = computePositivityRate(response.data[district]);
                    testing_result = computeTestingRate(response.data[district]);
                    consumption = computeConsumptionRate(response.data[district]);

                    positivity_data.push({
                        district: parseDistrictName(district),
                        positivity_rate:  pr_result.positivity_rate,
                        total_positive:  numberWithCommas(pr_result.total_positive),
                        reported_cases: numberWithCommas(pr_result.reported_cases)
                    });

                    testing_data.push({
                        district: parseDistrictName(district),
                        testing_rate:  testing_result.testing_rate,
                        total_tests:  numberWithCommas(testing_result.total_tests),
                        malaria_total: numberWithCommas(response.data[district]['opd_malaria_total'])
                    });

                    consumption_data.push({
                        district: parseDistrictName(district),
                        consumption_rate:  consumption.ratio,
                        act_consumed:  numberWithCommas(consumption.act_consumed),
                        malaria_total: numberWithCommas(response.data[district]['opd_malaria_total'])
                    });

                    $scope.positivity_data_table_results = positivity_data;
                    $scope.testing_data_table_results = testing_data;
                    $scope.consumption_data_table_results = consumption_data;

                }

            }, function (response) {
                console.log(response);
        });

        $http.get('../../data.json?'+params+'&group=period', {})
            .then(function (response) {
                    $scope.chart_data = response.data;
                    $scope.updateCharts();
                }, function (response) {console.log(response);}
            );

        $scope.updateCharts = function() {
            var positivity_chart_data = [{'key': 'Positivity Rate', 'values': []}];
            var testing_chart_data = [{'key': 'Testing Rate', 'values': []}];
            var consumption_chart_data = [{'key': 'Consumption Ratio', 'values': []}];
            var most_recent_period = 0;

            for (period in $scope.chart_data) {
                pr_result = computePositivityRate($scope.chart_data[period]);
                testing_result = computeTestingRate($scope.chart_data[period]);
                consumption = computeConsumptionRate($scope.chart_data[period]);
                ipt1 = computeIPT1($scope.chart_data[period]);
                ipt2 = computeIPT2($scope.chart_data[period]);
                total_positive = computeTotalPositive($scope.chart_data[period]);
                total_treated = computeTotalTreated($scope.chart_data[period]);

                positivity_chart_data[0]['values'].push({
                    'x':generateLabelFromPeriod(period),
                    'y':pr_result.positivity_rate
                });

                testing_chart_data[0]['values'].push({
                    'x':generateLabelFromPeriod(period),
                    'y':testing_result.testing_rate
                });

                consumption_chart_data[0]['values'].push({
                    'x':generateLabelFromPeriod(period),
                    'y':consumption.percentage
                });

                if (period > most_recent_period) {
                    $scope.big_metric.positivity_rate = pr_result.positivity_rate+"%";
                    $scope.big_metric.testing_rate = testing_result.testing_rate+"%";
                    $scope.big_metric.consumption_rate = consumption.ratio;
                    $scope.big_metric.IPT1 = ipt1+"%";
                    $scope.big_metric.IPT2 = ipt2+"%";
                    $scope.big_metric.total_positive = numberWithCommas(total_positive);
                    $scope.big_metric.total_treated = numberWithCommas(total_treated);
                    most_recent_period = period;
                }
            }

            drawGraph('#positivity-rate-chart', positivity_chart_data)
            drawGraph('#testing-rate-chart', testing_chart_data)
            drawGraph('#consumption-rate-chart', consumption_chart_data)

        };

        var drawGraph = function(selector, data) {
            nv.addGraph( function(){
                var chart = nv.models.multiBarChart().color(["#D90C17","#607D8B"]);
                    if(count($scope.chart_data)<=8) { chart.reduceXTicks(false); }

                chart.stacked(false);
                chart.showControls(false);
                chart.yAxis.tickFormat(d3.format(',.0d'));
                chart.forceY([0,100]);
                chart.tooltip.valueFormatter(function (d) { return d > 0 ? d : 0; });
                $(selector+' svg').html(" ");
                d3.select(selector+' svg').datum(data).transition().duration(500).call(chart);
                return chart;
            });
        };

        var computePositivityRate = function(data) {
            var reported_cases = (data['rdt_done'] + data['microscopy_done']);
            var total_positive = (data['rdt_positive'] + data['microscopy_positive']);
            var positivity_rate = (total_positive / reported_cases) * 100;

            return {positivity_rate: positivity_rate.toFixed(1),
                reported_cases : reported_cases,
                total_positive : total_positive
            };
        };

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

        var generateLabelFromPeriod = function(period) {
            year = period.substr(2,2);
            month = Number(period.substr(4,2));

            var months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
            return months[month] + "'"+year;
        };

        var parseDistrictName = function(district_id) {
//            return $scope.districts[district].replace(" District", "");
            return $scope.districts[district];
        };

        var count=function(json_obj){
            return Object.keys(json_obj).length;
        }

        function numberWithCommas(x) {
            if (x == undefined) return 0;
            return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }

    };
});

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
