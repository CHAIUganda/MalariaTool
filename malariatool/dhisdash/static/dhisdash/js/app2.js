var app = angular.module('dashboard', ['datatables'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('<%');
    $interpolateProvider.endSymbol('%>');
});

app.controller('DashboardController', function($scope, $http) {
//    $scope.filter = {
//        from_date: 0,
//        to_date: 0,
//        region: 0,
//        district: 0,
//        age_group: 0,
//    };
//
    $scope.filter = {
        from_date: "201501",
        to_date: "201512",
        region: "3",
        district: "1",
        age_group: "1",
    };


    $scope.positivity_data_table_results = [];
    $scope.testing_data_table_results = [];
    $scope.positivity_rate_results = {}
    $scope.big_metric = {};
    $scope.big_metric.positivity_rate = 0;
    $scope.big_metric.testing_rate = 0;

    $http.get('../../districts.json', {})
        .then(function(response) {
            $scope.districts = response.data;
        }, function (response) {
            console.log(response);
    });

    var generate_label_from_period = function(period) {
        year = period.substr(2,2);
        month = Number(period.substr(4,2));

        var months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        return months[month] + "'"+year;
    };


    var computePositivityRate = function(data) {
        reported_cases = (data['rdt_done'] + data['microscopy_done'])
        positivity_rate = ((data['rdt_positive'] + data['microscopy_positive']) / reported_cases) * 100

        return {positivity_rate: positivity_rate.toFixed(1), reported_cases : reported_cases};
    };

    var computeTestingRate = function(data) {
        tests_done = (data['rdt_done'] + data['microscopy_done']);
        testing_rate = (tests_done / data['opd_malaria_total']) * 100;

        return testing_rate.toFixed(1);
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
                for (district in response.data) {

                    result = computePositivityRate(response.data[district]);

                    $scope.positivity_data_table_results.push({
                        district: $scope.districts[district],
                        positivity_rate:  result.positivity_rate,
                        reported_cases: result.reported_cases
                    });

                    testing_rate = computeTestingRate(response.data[district]);

                    $scope.testing_data_table_results.push({
                        district: $scope.districts[district],
                        testing_rate:  testing_rate,
                        malaria_total: response.data[district]['opd_malaria_total']
                    });
                }

            }, function (response) {
                console.log(response);
        });

        $http.get('../../data.json?'+params+'&group=period', {})
            .then(function (response) {
                var chart_data = [{'key': 'Positivity Rate', 'values': []}];
                var most_recent_period = 0;

                for (period in response.data) {

                    result = computePositivityRate(response.data[period]);

                    chart_data[0]['values'].push({'x':generate_label_from_period(period), 'y':result.positivity_rate});

                    if (period > most_recent_period) {
                        $scope.big_metric.positivity_rate = positivity_rate.toFixed(1) + '%';
                        most_recent_period = period;
                    }
                }

                nv.addGraph( function(){
                    var chart = nv.models.multiBarChart().color(["#F44336","#607D8B"]);
//                    if(count(srd.dbs)<=8) { chart.reduceXTicks(false); }

                    chart.yAxis.tickFormat(d3.format(',.0d'));
                    $('#positivity_rate svg').html(" ");
                    d3.select('#positivity_rate svg').datum(chart_data).transition().duration(500).call(chart);
                    return chart;
                });

            }, function (response) {
                console.log(response);
        });


    };

});


//window.onload=function(){
//    function DashboardController($scope) {
//        $scope.filter = {district:'unknown'};
//    }
//}

