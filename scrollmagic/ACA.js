//Draw chart
drawACAChart();

//Call resize function when window is resized
$(window).resize(function () {
    drawACAChart();
});


function drawACAChart() {
	[width, height, acaChart] = resizeACAChart(d3);

	//Setup the ranges
	var x = d3.scaleLinear().range([0, width]);
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
	      .attr("cy", function(d) { return y(d.sumOfObamaCare); })
	      .on("mouseover", function(d) {
       div.transition()
         .duration(200)
         .style("opacity", .9);
       div.html(d.twitter + "<br>" + d.sumOfACA + " ACA" + "<br>" + d.sumOfObamaCare + " OC")
         .style("left", (d3.event.pageX) + "px")
         .style("top", (d3.event.pageY - 28) + "px");
       })
     .on("mouseout", function(d) {
       div.transition()
         .duration(500)
         .style("opacity", 0);
         })
     .on("click", function(d){
        var url = "healthcare_twitter_details.php?twitter=" + d.twitter + "&party=" + d.party + "&aca=" + d.sumOfACA + "&oc=" + d.sumOfObamaCare;
        location.href = url;
	});
	
	  // Add the X Axis
	  acaChart.append("g")
	      .attr("transform", "translate(0," + height + ")")
	      .call(d3.axisBottom(x));
	  acaChart.append("text") .attr("class", "x label") .attr("text-anchor", "end") .attr("x", width) .attr("y", height + 28) .text("Tweets mentioning Affordable Care Act (# tweets)")
	
	  // Add the Y Axis
	  acaChart.append("g").call(d3.axisLeft(y));
	  acaChart.append("text") .attr("class", "y label") .attr("text-anchor", "end") 
	  	.attr("y", -40) .text("Tweets mentioning Obama Care (# tweets)").attr("dy", ".75em")
	  	.attr("transform", "rotate(-90)")
	      
	  			

	});
	
	// Define 'div' for tooltips
	var div = d3.select("body")
	.append("div")  // declare the tooltip div 
	.attr("class", "aca-tooltip")              // apply the 'tooltip' class
	.style("opacity", 0);  
}

function circleColor(party) {
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