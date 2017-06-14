var app = angular.module('dashboard', ['datatables'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('<%');
    $interpolateProvider.endSymbol('%>');
});

$(document).ready(function(){
    var tooltip = {
        // delay: {show: 2000},
        track: true,
        fade: 250,
        container: 'body',
        placement: 'bottom'
    };

    $('.tabs .desc').tooltip(tooltip);
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

    $scope.big_metric.malaria_cases = "0";
    $scope.big_metric.ipt2_uptake = "0%";
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
        if (! (name in $scope.table_data)) {
            $scope.table_data[name] = [];
        }

        computeResult.district = parseDistrictName(district);
        $scope.table_data[name].push(computeResult);
    }

    $scope.hideSpinnerModal = function() {
        if ($scope.charts_loaded && $scope.tables_loaded) {
            $('#spinner-modal').modal('hide');   
        }
    }

    $scope.notifyChartsLoaded = function() {
        $scope.charts_loaded = true;   
        $scope.hideSpinnerModal();
    }

    $scope.notifyTablesLoaded = function() {
        $scope.tables_loaded = true;   
        $scope.hideSpinnerModal();
    }

    $scope.updateData = function() {

        $('#spinner-modal').modal('show');
        $scope.tables_loaded = false;
        $scope.charts_loaded = false;

        params = 'from_date='+$scope.filter.from_date+
            '&to_date='+$scope.filter.to_date+
            '&region='+$scope.filter.region+
            '&district='+$scope.filter.district+
            '&age_group='+$scope.filter.age_group;

        $http.get('../../data.json?'+params+'&group=district', {})
            .then(function (response) {
                $scope.table_data = {};

                for (district in response.data) {
                    addTableData(district, 'mortality', computeMortalityRate(response.data[district]));
                    addTableData(district, 'malaria_deaths', computeMalariaDeathRate(response.data[district]));
                    addTableData(district, 'malaria_cases', computeWeeklyMalariaCases(response.data[district]));
                    addTableData(district, 'testing', computeWeeklyTestingRate(response.data[district]));
                    addTableData(district, 'ipt2_uptake', computeIPT2Uptake(response.data[district]));
                    addTableData(district, 'sp_stock_status', computeSPStockStatus(response.data[district]));
                    addTableData(district, 'act_stock_status', computeACTStockStatus(response.data[district]));
                }
                $scope.notifyTablesLoaded();

            }, function (response) {
                console.log(response);
                $scope.notifyTablesLoaded();
        });

        $http.get('../../data.json?'+params+'&group=period', {})
            .then(function (response) {
                    $scope.chart_data = response.data;
                    $scope.updateCharts();
                    $scope.redrawCharts();
                    $scope.notifyChartsLoaded();

                }, function (response) {
                    console.log(response);
                    $scope.notifyChartsLoaded();
                }
            );

        var addChartData = function(x, name, key, computeResult) {
            for (var i = 0; i < $scope.nv_chart_data[name].length; i++){
                if($scope.nv_chart_data[name][i]['key'] == key){
                    $scope.nv_chart_data[name][i]['values'].push({
                        key: key,
                        x: x,
                        y: getComputeResult(computeResult)
                    });
                }
            }
        }

        var monthly_periods = [];
        var weekly_periods = [];

        $scope.updateCharts = function() {
            $scope.nv_chart_data = {};
            $scope.nv_chart_data['malaria_deaths'] = [{'key': 'Malaria Death Rate', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['mortality'] = [{'key': 'Mortality Rate', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['malaria_cases'] = [{'key': 'Weekly Malaria Cases', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['testing'] = [
                {'key': 'Weekly Testing Rate', 'color':'#D90C17', 'values': []},
                {'key': 'Weekly Test Positivity Rate', 'color':'#2ca02c', 'values': []},
                {'key': 'Weekly Tested Negative Treated Rate', 'color':'#7777ff', 'values': []}
            ];
            $scope.nv_chart_data['ipt2_uptake'] = [{'key': 'IPT2 Uptake', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['sp_stock_status'] = [{'key': 'SP Stock Status', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['act_stock_status'] = [{'key': 'ACT Stock Status', 'color':'#D90C17', 'values': []}];

            var most_recent_period = 0;
            var month_counter = 0;
            var week_counter = 0;
            
            for (period in $scope.chart_data) {
                var period_data = $scope.chart_data[period];

                if (isMonthPeriod(period)) {        
                    monthly_periods.push(generateLabelFromPeriod(period));

                    addChartData(month_counter, 'malaria_deaths', 'Malaria Death Rate', computeMalariaDeathRate(period_data));
                    addChartData(month_counter, 'mortality', 'Mortality Rate', computeMortalityRate(period_data));
                    // addChartData(month_counter, 'positivity_rate', computePositivityRate($scope.chart_data[period]));
                    addChartData(month_counter, 'ipt2_uptake', 'IPT2 Uptake', computeIPT2Uptake(period_data));
                    addChartData(month_counter, 'sp_stock_status', 'SP Stock Status', computeSPStockStatus(period_data));
                    addChartData(month_counter, 'act_stock_status', 'ACT Stock Status', computeACTStockStatus(period_data));

                    if (period > most_recent_period) {
                        $scope.big_metric.ipt2_uptake = getComputeResult(computeIPT2Uptake(
                            period_data))+"%";

                        $scope.big_metric.act_stock_status = getComputeResult(computeACTStockStatus(
                            period_data))+"%";

                        most_recent_period = period;
                    }

                    month_counter++;

                } else {
                    console.log(computeWeeklyPositivityRate($scope.chart_data[period]));
                    weekly_periods.push(generateLabelFromWeeklyPeriod(period, period_data));

                    addChartData(week_counter, 'malaria_cases', 'Weekly Malaria Cases', computeWeeklyMalariaCases(period_data));
                    addChartData(week_counter, 'testing', 'Weekly Testing Rate', computeWeeklyTestRate(period_data));
                    addChartData(week_counter, 'testing', 'Weekly Test Positivity Rate', computeWeeklyTestPositivityRate(period_data));
                    addChartData(week_counter, 'testing', 'Weekly Tested Negative Treated Rate', computeWeeklyTestNegativeTreatedRate(period_data));


                    // Did not compare the biggest because of natuaral language comparison
                    // E.g. 2010W10 < 2010W2 returns true
                    // 
                    $scope.big_metric.malaria_cases = getComputeResult(computeWeeklyMalariaCases(
                            period_data));

                    week_counter++;
                }
                
            }

        };

        $scope.redrawCharts = function() {
            drawLineChart('#chart-malaria-deaths', $scope.nv_chart_data['malaria_deaths'], 3, monthly_periods);
            drawLineChart('#chart-mortality', $scope.nv_chart_data['mortality'], 100, monthly_periods);
            drawLineChart('#chart-malaria-cases', $scope.nv_chart_data['malaria_cases'], 20, weekly_periods);
            drawLineChart('#chart-testing', $scope.nv_chart_data['testing'], 200, weekly_periods);
            drawLineChart('#chart-ipt2-uptake', $scope.nv_chart_data['ipt2_uptake'], 100, monthly_periods);
            drawLineChart('#chart-sp-stock-status', $scope.nv_chart_data['sp_stock_status'], 100, monthly_periods);
            drawLineChart('#chart-act-stock-status', $scope.nv_chart_data['act_stock_status'], 100, monthly_periods);
        };
    
    };
});

