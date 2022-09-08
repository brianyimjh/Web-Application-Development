// Set the dimensions of the canvas / graph
var margin = {top: 20, right: 30, bottom: 80, left: 50},
    width = 900 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.timeParse("%Y-%m-%d");

// Set the ranges
var x = d3.scaleTime().range([0, width])
var y = d3.scaleLinear().range([height, 0]);

// Define the axes
var xAxis = d3.axisBottom(x).tickFormat(d3.timeFormat("%Y-%m-%d"));
var yAxis = d3.axisLeft(y);

// Define the line
var line = d3.line()	
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });
    
// Adds the svg canvas
var svg = d3.select("#my_dataviz")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.json("/database", function(error, data) {
  if (error) throw error;

  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.value = +d.value;
  });

  function sortByDateAscending(a, b) {
    return a.date - b.date;
  }

  data = data.sort(sortByDateAscending);

  // Scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.value; })]);

  // Nest the records by email
  var dataNest = d3.nest()
      .key(function(d) {return d.email;})
      .entries(data);

  var color = d3.scaleOrdinal(d3.schemeCategory10);  // set the colour scale

  legendSpace = width/dataNest.length; // spacing for legend

  // Loop through each email / key
  dataNest.forEach(function(d,i) { 

      svg.append("path")
          .attr("class", "line")
          .style("stroke", function() { // Add the colours dynamically
              return d.color = color(d.key); })
          .attr("d", line(d.values));

      // Add the Legend
      svg.append("text")
          .attr("x", (legendSpace/2)+i*legendSpace) // spacing
          .attr("y", height + (margin.bottom/2)+ 5)
          .attr("class", "legend")    // style the legend
          .style("fill", function() { // dynamic colours
              return d.color = color(d.key); })
          .text(d.key);

  });

  // Add the X Axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  // Add the Y Axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

});
