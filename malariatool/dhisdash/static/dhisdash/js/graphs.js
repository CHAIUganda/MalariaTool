var drawLineChart = function(selector, data, ymax, xLabels) {
    console.log(JSON.stringify(data));
    nv.addGraph(function() {
        chart = nv.models.lineChart()
            .options({
                duration: 300,
                useInteractiveGuideline: true
            })
        ;

        chart.forceY([0,ymax]);
        if(selector == "#chart-malaria-cases")
        {
            chart.yAxis.axisLabel("per 1000 pop")
        }
        else
        {
            chart.yAxis.axisLabel("%")
        }
        chart.xAxis.axisLabel("Period")
        chart.xAxis.tickFormat(function(p) {
            return xLabels[p];
        });

        d3.select(selector+' svg')
            .datum(data)
            .call(chart);
        nv.utils.windowResize(chart.update);
        return chart;
    });
};

var drawGraph = function(selector, data, ymax) {
    nv.addGraph( function(){
        var chart = nv.models.multiBarChart().color(["#D90C17","#607D8B"]);
            if(count($scope.chart_data)<=8) { chart.reduceXTicks(false); }

        chart.stacked(false);
        chart.showControls(false);
        chart.yAxis.tickFormat(d3.format(',.0d'));
        chart.forceY([0,ymax]);
        chart.tooltip.valueFormatter(function (d) { return d > 0 ? d : 0; });
        $(selector+' svg').html(" ");
        d3.select(selector+' svg').datum(data).transition().duration(500).call(chart);
        return chart;
    });
};

var drawLinePlusBarChart = function(selector, data, ymax) {
    nv.addGraph( function(){
        var chart = nv.models.linePlusBarChart().color(["#D90C17","#607D8B"]);
            if(count($scope.chart_data)<=8) { chart.reduceXTicks(false); }

        // chart.stacked(false);
        // chart.showControls(false);
        // chart.yAxis.tickFormat(d3.format(',.0d'));
        chart.forceY([0,ymax]);
        chart.tooltip.valueFormatter(function (d) { return d > 0 ? d : 0; });
        $(selector+' svg').html(" ");
        d3.select(selector+' svg').datum(data).transition().duration(500).call(chart);
        return chart;
    });
};

