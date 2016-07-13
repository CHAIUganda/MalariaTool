var app = angular.module('dashboard', ['datatables'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('<%');
    $interpolateProvider.endSymbol('%>');
});

$(document).ready(function(){
    $('.tabs .desc').tooltip( {
		// delay: {show: 2000},
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

    $scope.big_metric.malaria_cases = "0%";
    $scope.big_metric.ipt2_rate = "0%";
    $scope.big_metric.act_stock_status = "0%";

    $http.get('../../districts.json', {})
        .then(function(response) {
            $scope.districts = response.data;
        }, function (response) {
            console.log(response);
    });

    var parseDistrictName = function(district_id) {
        return $scope.districts[district];
    };

    var addTableData = function(district, name, computeResult) {
        if ($scope.table_data == undefined) {
            $scope.table_data = {};
        }

        if (! (name in $scope.table_data)) {
            $scope.table_data[name] = [];
        }

        computeResult.district = parseDistrictName(district);
        $scope.table_data[name].push(computeResult);
    }

    $scope.updateData = function() {

        params = 'from_date='+$scope.filter.from_date+
            '&to_date='+$scope.filter.to_date+
            '&region='+$scope.filter.region+
            '&district='+$scope.filter.district+
            '&age_group='+$scope.filter.age_group;

        $http.get('../../data.json?'+params+'&group=district', {})
            .then(function (response) {
                for (district in response.data) {
                    addTableData(district, 'mortality_rate', computeMortalityRate(response.data[district]));
                    addTableData(district, 'malaria_deaths', computeMalariaDeathRate(response.data[district]));
                    addTableData(district, 'malaria_cases', computeMalariaCases(response.data[district]));
                }
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

        $scope.nv_chart_data = {};
        $scope.nv_chart_data['malaria_deaths'] = [{'key': 'Malaria Death Rate', 'color':'#D90C17', 'values': []}];
        $scope.nv_chart_data['mortality_rate'] = [{'key': 'Death Proportion', 'color':'#D90C17', 'values': []}];
        $scope.nv_chart_data['malaria_cases'] = [{'key': 'Malaria Cases', 'color':'#D90C17', 'values': []}];

        var addChartData = function(x, name, computeResult) {
            $scope.nv_chart_data[name][0]['values'].push({
                x: x,
                y: getComputeResult(computeResult)
            });
        }

        var periods = [];

        $scope.updateCharts = function() {
            var most_recent_period = 0;
            var counter = 0;
            
            for (period in $scope.chart_data) {

                periods.push(generateLabelFromPeriod(period));

                addChartData(counter, 'malaria_deaths', computeMalariaDeathRate($scope.chart_data[period]));
                addChartData(counter, 'mortality_rate', computeMortalityRate($scope.chart_data[period]));
                addChartData(counter, 'malaria_cases', computeMalariaCases($scope.chart_data[period]));

                counter++;

                if (period > most_recent_period) {
                    $scope.big_metric.malaria_cases = getComputeResult(computeMalariaCases(
                        $scope.chart_data[period]))+"%";

                    most_recent_period = period;
                }
            }
        };

        $scope.redrawCharts = function() {
            drawLineChart('#chart-malaria-deaths', $scope.nv_chart_data['malaria_deaths'], 3, periods)
            drawLineChart('#chart-mortality-rate', $scope.nv_chart_data['mortality_rate'], 100, periods)
            drawLineChart('#chart-malaria-cases', $scope.nv_chart_data['malaria_cases'], 100, periods)
        };
    };
});

