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

    $scope.big_metric.death_proportion = "0%";
    $scope.big_metric.ipt2_rate = "0%";
    $scope.big_metric.sp_stock_out_rate = "0%";

    $http.get('../../districts.json', {})
        .then(function(response) {
            $scope.districts = response.data;
        }, function (response) {
            console.log(response);
    });

    // $scope.showReg=function(option_index){
    //     $('.toggle-option').removeClass('active');
    //     $('#toggle-option-'+option_index).addClass('active');
    // }

    var parseDistrictName = function(district_id) {
        return $scope.districts[district];
    };

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
                var infant_deaths_data = [];
                var death_proportion_data = [];

                for (district in response.data) {

                    pr_result = computePositivityRate(response.data[district]);
                    testing_result = computeTestingRate(response.data[district]);
                    consumption = computeConsumptionRate(response.data[district]);
                    infant_deaths = computeInfantDeathRate(response.data[district]);
                    death_proportion = computeDeathProportionRate(response.data[district]);

                    positivity_data.push({
                        district: parseDistrictName(district),
                        positivity_rate:  pr_result.positivity_rate,
                        total_positive:  numberWithCommas(pr_result.total_positive),
                        reported_cases: numberWithCommas(pr_result.reported_cases)
                    });

                    infant_deaths_data.push({
                        district: parseDistrictName(district),
                        infant_death_rate: infant_deaths.result+"%",
                        inpatient_malaria_deaths: numberWithCommas(infant_deaths.numerator),
                        malaria_admissions: numberWithCommas(infant_deaths.denominator)
                    });

                    death_proportion_data.push({
                        district: parseDistrictName(district),
                        death_proportion: death_proportion.result+"%",
                        inpatient_malaria_deaths: numberWithCommas(death_proportion.numerator),
                        total_inpatient_deaths: numberWithCommas(death_proportion.denominator)
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
                    $scope.infant_deaths_data_table_results = infant_deaths_data;
                    $scope.death_proportion_data_table_results = death_proportion_data;

                }

                console.log(infant_deaths_data);

            }, function (response) {
                console.log(response);
        });

        $http.get('../../data.json?'+params+'&group=period', {})
            .then(function (response) {
                    $scope.chart_data = response.data;
                    $scope.updateCharts();
                    $scope.redrawCharts();
                }, function (response) {console.log(response);}
            );

        $scope.updateSingleChart = function(identifier, name, function_name, ymax) {
            var chart_data = [{'key': name, 'color':'#D90C17', 'values': []}];
            var counter = 0;
            var computeFunction = window[function_name];
            var labels = []

            for (period in $scope.chart_data) {
                computed = computeFunction($scope.chart_data[period]);
                chart_data[0]['values'].push({
                    x: counter,
                    y: computed.result
                });

                counter++;
                labels.push(generateLabelFromPeriod(period));
            }

            drawLineChart(identifier, chart_data, ymax, labels)
        };

        $scope.computeChartData = function() {

        }

        var addChartData = function(x, name, computeResult) {
            $scope.nv_chart_data[name][0]['values'].push({
                    x: x,
                    y: getComputeResult(computeResult)
                });
        }

        var periods = [];

        $scope.updateCharts = function() {
            $scope.nv_chart_data = {};
            $scope.nv_chart_data['infant_deaths'] = [{'key': 'Infant Death Rate', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['death_proportion'] = [{'key': 'Death Proportion', 'color':'#D90C17', 'values': []}];

            var most_recent_period = 0;
            var counter = 0;
            
            for (period in $scope.chart_data) {

                counter++;
                periods.push(generateLabelFromPeriod(period));

                addChartData(counter, 'infant_deaths', computeInfantDeathRate($scope.chart_data[period]));
                addChartData(counter, 'death_proportion', computeDeathProportionRate($scope.chart_data[period]));

                if (period > most_recent_period) {
                    $scope.big_metric.death_proportion = getComputeResult(computeDeathProportionRate(
                        $scope.chart_data[period]))+"%";

                    most_recent_period = period;
                }
            }
        };

        $scope.redrawCharts = function() {
            drawLineChart('#chart-infant-deaths', $scope.nv_chart_data['infant_deaths'], 10, periods)
            drawLineChart('#chart-death-proportion', $scope.nv_chart_data['death_proportion'], 100, periods)
        };
    };
});

