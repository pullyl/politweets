//Draw chart
drawACAChart();

//Call resize function when window is resized
$(window).resize(function () {
    drawACAChart();
});


function drawACAChart() {
	[width, height, acaChart] = resizeACAChart(d3);

	//Setup the ranges
	var x = d3.scaleTime().range([0, width]);
	var y = d3.scaleLinear().range([height, 0]);	
	
	// Get the data
	d3.csv("data/acaobamacare.csv", function(error, data) {
	  if (error) throw error;
	
	  // format the data
	  data.forEach(function(d) {
	      d.sumOfACA = +d.sumOfACA;
		  d.sumOfObamaCare = +d.sumOfObamaCare;
	  });
	  
		
	  // Scale the range of the data
	  x.domain(d3.extent(data, function(d) { return d.sumOfACA; }));
	  y.domain([0, d3.max(data, function(d) { return d.sumOfObamaCare; })]);
	  	
	  // Add the scatterplot
	  acaChart.selectAll("dot")
	      .data(data)
	    .enter().append("circle")
	      .attr("r", 5)
	      .style('fill', function(d) { return circleColor(d.party); })
	      .attr("cx", function(d) { return x(d.sumOfACA); })
	      .attr("cy", function(d) { return y(d.sumOfObamaCare); });
	
	  // Add the X Axis
	  acaChart.append("g")
	      .attr("transform", "translate(0," + height + ")")
	      .call(d3.axisBottom(x));
	
	  // Add the Y Axis
	  acaChart.append("g")
	      .call(d3.axisLeft(y));			

	});
}

function circleColor(party) {
	console.log(party)
	if ( party == 'Republican') {
		return 'red';	
	} else if (party == 'Democrat') {
		return 'blue';
	} else {
		return 'green';
	}	
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