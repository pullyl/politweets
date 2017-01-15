
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
var z = d3.scaleOrdinal(d3.schemeCategory10);

var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.num); });

d3.csv("data.csv", type, function(error, data) {
	if (error) throw error;

	var parties = data.columns.slice(1).map(function(id) {
		return {
			id: id,
			values: data.map(function(d) {
				return {date: d.date, num:d[id]};
			})
		};
	});

	x.domain(d3.extent(data, function(d) {return d.date;}));
 
 y.domain([
    d3.min(parties, function(c) { return d3.min(c.values, function(d) { return d.num; }); }),
    d3.max(parties, function(c) { return d3.max(c.values, function(d) { return d.num; }); })
  ]);

   z.domain(parties.map(function(c) { return c.id; }));

 y.domain([
    d3.min(parties, function(c) { return d3.min(c.values, function(d) { return d.num; }); }),
    d3.max(parties, function(c) { return d3.max(c.values, function(d) { return d.num; }); })
  ]);

  z.domain(parties.map(function(c) { return c.id; }));

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))

  var party = g.selectAll(".party")
    .data(parties)
    .enter().append("g")
      .attr("class", "party");

  party.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return z(d.id); });

  party.append("text")
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.num) + ")"; })
      .attr("x", 3)
      .attr("dy", "0.35em")
      .style("font", "10px sans-serif")
      .text(function(d) { return d.id; });
});

function type(d, _, columns) {
  d.date = parseTime(d.date);
  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
  return d;
}
