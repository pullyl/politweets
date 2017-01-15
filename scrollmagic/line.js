var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%b-%y");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line_dem = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.dem); });

var line_rep = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.rep); });

d3.csv("data_dems.csv", function(d) {
  d.date = parseTime(d.date);
  d.dem = +d.dem;
  return d;
}, function(error, data) {
  if (error) throw error;

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain(d3.extent(data, function(d) { return d.dem; }));

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))

  g.append("path")
      .datum(data)
      .attr("class", "line_dem")
      .attr("stroke", "blue")
      .attr("d", line_dem);
});


d3.csv("data_reps.csv", function(d) {
  d.date = parseTime(d.date);
  d.rep = +d.rep;
  return d;
}, function(error, data) {
  if (error) throw error;

  x.domain(d3.extent(data, function(d) { return d.date; }));
  // y.domain(d3.extent(data, function(d) { return d.rep; }));

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))

  g.append("path")
      .datum(data)
      .attr("class", "line_rep")
      .attr("stroke", "red")
      .attr("d", line_rep);
});