//Draw chart
drawACAChart();

//Call resize function when window is resized
$(window).resize(function () {
    drawACAChart();
});


function drawACAChart() {
	[width, height, acaChart] = resizeACAChart(d3);

	var parseTime = d3.timeParse("%b-%y");
	
	var x = d3.scaleTime().rangeRound([0, width]);
	var y = d3.scaleLinear().rangeRound([height, 0]);
	
	console.log(width);
	console.log(height);
	
	var line_dem = d3.line()
	    .x(function(d) { return x(d.date); })
	    .y(function(d) { return y(d.dem); });
	
	var line_rep = d3.line()
	    .x(function(d) { return x(d.date); })
	    .y(function(d) { return y(d.rep); });
	
	d3.csv("data/immigration_data_dems.csv", function(d) {
	  d.date = parseTime(d.date);
	  d.dem = +d.dem;
	  return d;
	}, function(error, data) {
	  if (error) throw error;
	
	  x.domain(d3.extent(data, function(d) { return d.date; }));
	  y.domain(d3.extent(data, function(d) { return d.dem; }));
	
	  acaChart.append("g")
	      .attr("class", "axis axis--x")
	      .attr("transform", "translate(0," + height + ")")
	      .call(d3.axisBottom(x));
	
	  acaChart.append("g")
	      .attr("class", "axis axis--y")
	      .call(d3.axisLeft(y))
	
	  acaChart.append("path")
	      .datum(data)
	      .attr("class", "line_dem")
	      .attr("stroke", "purple")
	      .attr("d", line_dem);
	});
	
	
	d3.csv("data/immigration_data_reps.csv", function(d) {
	  d.date = parseTime(d.date);
	  d.rep = +d.rep;
	  return d;
	}, function(error, data) {
	  if (error) throw error;
	
	  x.domain(d3.extent(data, function(d) { return d.date; }));
	
	  acaChart.append("g")
	      .attr("class", "axis axis--x")
	      .attr("transform", "translate(0," + height + ")")
	      .call(d3.axisBottom(x));
	
	  acaChart.append("g")
	      .attr("class", "axis axis--y")
	      .call(d3.axisLeft(y))
	
	  acaChart.append("path")
	      .datum(data)
	      .attr("class", "line_rep")
	      .attr("stroke", "green")
	      .attr("d", line_rep);
	});
	
}

/* 	Size chart		*/
function resizeACAChart(d3) {
	console.log("resizing the ACA window");
    // Set the dimensions of the canvas / graph
    width = window.innerWidth * .6 - 20,
    height = width*.6
    
    document.getElementById("aca-chart").style.height = height + "px";
	document.getElementById("aca-chart").style.width = width + "px";
    
    console.log("ACA resize width:  " + width);
    console.log("ACA resize height: " + height);

    d3.select("#aca-chart-id").remove();
    
    var svg1 = d3.select("#aca-chart").append("svg").attr("id","aca-chart-id"),
    margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = +width - margin.left - margin.right,
    height = +height - margin.top - margin.bottom;
    acaChart = svg1.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
          
	return [width, height, acaChart];
}