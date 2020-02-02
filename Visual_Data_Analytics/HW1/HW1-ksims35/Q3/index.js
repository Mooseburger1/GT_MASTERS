var margin = {top:20, right:20, bottom:50, left:50},
    width = 960 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var svg = d3.select("body")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y")


d3.dsv(",", "q3.csv", function(d){
  return{
    year: parseTime(d.year),
    running_total: +d.running_total
  };
}).then(function(data){


  ///////////////////////////////////////// GRAPH LAYOUT //////////////////////////////////////
  //set the domain and range scale for bar graph
  var Xscale = d3.scaleTime().domain([
                                      d3.min(data, function(d) { return d.year; }),
                                      d3.max(data, function(d) { return d.year; })
                                     ])
                             .range([10,width]);

  var Yscale = d3.scaleLinear().domain([0, d3.max(data, function(d){
                                                                    return d.running_total;
                                                                   })])
                               .range([height,0]);
 

  //create the axes for the graph
  var Xaxis = d3.axisBottom().scale(Xscale).ticks(data.length);
  var Yaxis = d3.axisLeft().scale(Yscale);

  
  ///////////////////////////////////////// Plot bars //////////////////////////////////////

  svg.selectAll("rect")                                                    //will append data to svg rectangles
     .data(data)                                                           //specify data to bind
     .enter()                                                              //begin cycling through the data
     .append("rect")                                                       //bind each data point to a svg rect html tag
     .attr("x", function(d,i){
                              return Xscale(d.year);                       //Set X location of each data point <rect> using Xscale function
                             })
     .attr("y", function(d){
       return Yscale(d.running_total);                                     //Set Y location of each data point <rect> using Yscale function
     })                                                                    
     .attr("width",10)                                                     //Set width attribute of each data point <rect>
     .attr("height", function(d,i){
                                return height - Yscale(d.running_total);   //Set Height of each data point using Yscale function
                                })
     .attr("class", "sbar");
  
///////////////////////////////////////// Plot Axes //////////////////////////////////////

// x - axis
svg.append("g").attr("class", "axis").attr("transform", "translate(0," + height + ")").call(Xaxis);

// Show every 3rd year on the X axis
var ticks = d3.selectAll(".tick text");
ticks.each(function(_, i){
  if (i % 3 != 0) d3.select(this).remove();
});

// y - axis
svg.append("g").call(Yaxis);
// title
svg.append("text")
   .attr("x", (width /2) - 200)
   .attr("y", 0 )
   .style("font-size", "26px")
   .text("Rebrickable Lego Sets by Year")
// my credentials
svg.append("text")
   .attr("x", width - 100)
   .attr("y", height + margin.bottom)
   .style("font-size", "16px")
   .text("ksims35")

}).catch( (error) => {
  console.error(error)
});