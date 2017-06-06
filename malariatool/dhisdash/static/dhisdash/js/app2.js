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

    $scope.big_metric.malaria_cases = "0%";
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

        // Assign dimensions for map container
            var width = 500,
                height = 500;
            var field = "result";

            var valueFormat = d3.format(",");

            // Define a geographical projection
            // Also, set initial zoom to show the features
            var projection	= d3.geo.mercator()
                .scale(1);

            // Prepare a path object and apply the projection to it
            var path = d3.geo.path()
                .projection(projection);

            // We prepare an object to later have easier access to the data.
            var dataById = d3.map();

            //Define quantize scale to sort data values into buckets of color
            //Colors by Cynthia Brewer (colorbrewer2.org), 9-class YlGnBu

            var color = d3.scale.quantize()
                                //.range(d3.range(9),map(function(i) { return 'q' + i + '-9';}));
                            .range([    "#a50026",
                                        "#d73027",
                                        "#f46d43",
                                        "#fdae61",
                                        "#fee08b",
                                        "#ffffbf",
                                        "#d9ef8b",
                                        "#a6d96a",
                                        "#66bd63",
                                        "#1a9850",
                                        "#006837" ]);

        $http.get('../../data.json?'+params+'&group=district', {})
            .then(function (response) {
                $scope.table_data = {};


                for (district in response.data) {
                    addTableData(district, 'mortality_rate', computeMortalityRate(response.data[district]));
                    addTableData(district, 'malaria_deaths', computeMalariaDeathRate(response.data[district]));
                    addTableData(district, 'malaria_cases', computeMalariaCases(response.data[district]));
                    addTableData(district, 'positivity_rate', computePositivityRate(response.data[district]));
                    addTableData(district, 'ipt2_uptake', computeIPT2Uptake(response.data[district]));
                    addTableData(district, 'sp_stock_status', computeSPStockStatus(response.data[district]));
                    addTableData(district, 'act_stock_status', computeACTStockStatus(response.data[district]));
                }
                $scope.notifyTablesLoaded();

                var data = $scope.table_data['positivity_rate'];

                //Set input domain for color scale
                    color.domain([
                        d3.min(data, function(d) { return +d[field]; }),
                        d3.max(data, function(d) { return +d[field]; })

                        ]);

                    // This maps the data of the CSV so it can be easily accessed by
                    // the ID of the district, for example: dataById[2196]
                    dataById = d3.nest()
                      .key(function(d) { return d.id; })
                      .rollup(function(d) { return d[0]; })
                      .map(data);

                    // Load features from GeoJSON
                    d3.json('static/dhisdash/data/ug_districts2.geojson', function(error, json) {


                        // Get the scale and center parameters from the features.
                        var scaleCenter = calculateScaleCenter(json);

                        // Apply scale, center and translate parameters.
                        projection.scale(scaleCenter.scale)
                                .center(scaleCenter.center)
                                .translate([width/2, height/2]);

                        // Merge the coverage data amd GeoJSON into a single array
                        // Also loop through once for each coverage score data value

                        for (var i=0; i < data.length ; i++ ) {

                            // Grab district name
                            var dist = data[i].district;
                            var pos = dist.indexOf(" ");
                            var dataDistrict = dist.substring(0, pos).toUpperCase();
                            //var dataDistrict = data[i].district;

                            //Grab data value, and convert from string to float
                            var dataValue = +data[i][field];

                            //Find the corresponding district inside GeoJSON
                            for (var j=0; j < json.features.length ; j++ ) {

                                // Check the district reference in json
                                var jsonDistrict = json.features[j].properties.dist;

                                if (dataDistrict == jsonDistrict) {

                                    //Copy the data value into the GeoJSON
                                    json.features[j].properties.field = dataValue;

                                    //Stop looking through JSON
                                    break;
                                }
                            }
                        }



                        // Create SVG inside map container and assign dimensions
                        //svg.selectAll("*").remove();
                        //d3.select("#map").selectAll("*").remove();
                        var svg = d3.select("#map")
                            .append('svg')
                            .attr("width", width)
                            .attr("height", height);

                        // Add a <g> element to the SVG element and give a class to style later
                        svg.append('g')
                            .attr('class', 'features')
                        // Bind data and create one path per GeoJSON feature
                        svg.selectAll("path")
                            .data(json.features)
                            .enter()
                            .append("path")
                            .attr("d", path)
                            .on("mouseover", hoveron)
                            .on("mouseout", hoverout)
                            .style("cursor", "pointer")
                            .style("stroke", "#777")
                            .style("fill", function(d) {

                                // Get data value

                                var value = d.properties.field;

                                if (value) {
                                    // If value exists ...
                                    return color(value);
                                } else {
                                    // If value is undefines ...
                                    return "#ccc";
                                }
                            });



                    }); // End d3.json

                    // Logic to handle hover event when its firedup
                        var hoveron = function(d) {
                            console.log('d', d, 'event', event);
                            var div = document.getElementById('tooltip');
                            div.style.left = event.pageX + 'px';
                            div.style.top = event.pageY + 'px';


                            //Fill yellow to highlight
                            d3.select(this)
                                .style("fill", "white");

                            //Show the tooltip
                            d3.select("#tooltip")
                                .style("opacity", 1);

                            //Populate name in tooltip
                            d3.select("#tooltip .name")
                                .text(d.properties.dist);

                            //Populate value in tooltip
                            d3.select("#tooltip .value")
                                .text(valueFormat(d.properties.field) + "%");
                        }

                        var hoverout = function(d) {

                            //Restore original choropleth fill
                            d3.select(this)
                                .style("fill", function(d) {
                                    var value = d.properties.field;
                                    if (value) {
                                        return color(value);
                                    } else {
                                        return "#ccc";
                                    }
                                });

                            //Hide the tooltip
                            d3.select("#tooltip")
                                .style("opacity", 0);

                        }

            }, function (response) {
                console.log(response);
                $scope.notifyTablesLoaded();
        });

        function calculateScaleCenter(features) {
                // Get the bounding box of the paths (in pixels) and calculate a scale factor based on box and map size
                var bbox_path = path.bounds(features),
                    scale = 0.95 / Math.max(
                        (bbox_path[1][0] - bbox_path[0][0]) / width,
                        (bbox_path[1][1] - bbox_path[0][1]) / height
                        );

                // Get the bounding box of the features (in map units) and use it to calculate the center of the features.
                var bbox_feature = d3.geo.bounds(features),
                    center = [
                        (bbox_feature[1][0] + bbox_feature[0][0]) / 2,
                        (bbox_feature[1][1] + bbox_feature[0][1]) / 2];

                return {
                    'scale':scale,
                    'center':center
                };
            }

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

        var addChartData = function(x, name, computeResult) {
            $scope.nv_chart_data[name][0]['values'].push({
                x: x,
                y: getComputeResult(computeResult)
            });
        }

        var monthly_periods = [];
        var weekly_periods = [];

        $scope.updateCharts = function() {
            $scope.nv_chart_data = {};
            $scope.nv_chart_data['malaria_deaths'] = [{'key': 'Malaria Death Rate', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['mortality_rate'] = [{'key': 'Mortality Rate', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['malaria_cases'] = [{'key': 'Weekly Malaria Cases', 'color':'#D90C17', 'values': []}];
            $scope.nv_chart_data['positivity_rate'] = [{'key': 'Weekly Positivity Rate', 'color':'#D90C17', 'values': []}];
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

                    addChartData(month_counter, 'malaria_deaths', computeMalariaDeathRate(period_data));
                    addChartData(month_counter, 'mortality_rate', computeMortalityRate(period_data));
                    // addChartData(month_counter, 'positivity_rate', computePositivityRate($scope.chart_data[period]));
                    addChartData(month_counter, 'ipt2_uptake', computeIPT2Uptake(period_data));
                    addChartData(month_counter, 'sp_stock_status', computeSPStockStatus(period_data));
                    addChartData(month_counter, 'act_stock_status', computeACTStockStatus(period_data));

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

                    addChartData(week_counter, 'malaria_cases', computeWeeklyMalariaCases(period_data));
                    addChartData(week_counter, 'positivity_rate', computeWeeklyPositivityRate(period_data));

                    // Did not compare the biggest because of natuaral language comparison
                    // E.g. 2010W10 < 2010W2 returns true
                    // 
                    $scope.big_metric.malaria_cases = getComputeResult(computeWeeklyMalariaCases(
                            period_data))+"%";

                    week_counter++;
                }

                
            }
        };

        $scope.redrawCharts = function() {
            drawLineChart('#chart-malaria-deaths', $scope.nv_chart_data['malaria_deaths'], 3, monthly_periods);
            drawLineChart('#chart-mortality-rate', $scope.nv_chart_data['mortality_rate'], 100, monthly_periods);
            drawLineChart('#chart-malaria-cases', $scope.nv_chart_data['malaria_cases'], 2, weekly_periods);
            drawLineChart('#chart-positivity-rate', $scope.nv_chart_data['positivity_rate'], 100, weekly_periods);
            drawLineChart('#chart-ipt2-uptake', $scope.nv_chart_data['ipt2_uptake'], 100, monthly_periods);
            drawLineChart('#chart-sp-stock-status', $scope.nv_chart_data['sp_stock_status'], 100, monthly_periods);
            drawLineChart('#chart-act-stock-status', $scope.nv_chart_data['act_stock_status'], 100, monthly_periods);
        };
    
    };
});

