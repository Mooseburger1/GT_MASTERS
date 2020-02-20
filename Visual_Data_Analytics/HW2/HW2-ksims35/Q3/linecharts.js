var margin = {top: 20, right: 20, bottom:50, left:50},
             width = 900 - margin.left - margin.right,
             height = 700 - margin.top - margin.bottom;
var padding = 50;
var svg3a = d3.select("#div3a")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg3b = d3.select("#div3b")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg3c = d3.select("#div3c")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg3cb = d3.select("#div3cb")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y")


///////////////////////////////////// 3A ///////////////////////////////////////////////////////
d3.dsv(",", "earthquakes.csv", function(d){
    return{
        year: parseTime(d.year),
        eight: +d["8.0+"],
        seven: +d["7_7.9"],
        six: +d["6_6.9"],
        five: +d["5_5.9"],
        deaths: +d["Estimated Deaths"]
    
      };
}).then(function(data){
    

    n = data.length;                               //Number of data points
    // SCALE GENERATORS
    var xScale = d3.scaleTime()
                   .domain([
                            d3.min(data, function(d){return d.year;}),
                            d3.max(data, function(d){return d.year;})
                   ])
                   .range([padding, width]);
    
    var yScale = d3.scaleLinear()
                   .domain([
                            0,
                            d3.max(data, function(d){return d.five;})
                   ])
                   .range([height-padding, padding])
                   
    //AXES DRAWN FROM SCALE GENERATORS
    var Xaxis = d3.axisBottom().scale(xScale).ticks(data.length);
    var Yaxis = d3.axisLeft().scale(yScale);
    
    //LINE GENERATORS
    var five_line = d3.line()
                 .x(function(d){return xScale(d.year);})
                 .y(function(d){return yScale(d.five);})
                 .curve(d3.curveMonotoneX);

    var six_line = d3.line()
                     .x(function(d){return xScale(d.year);})
                     .y(function(d){return yScale(d.six);})
                     .curve(d3.curveMonotoneX);

    var seven_line = d3.line()
                      .x(function(d){return xScale(d.year);})
                      .y(function(d){return yScale(d.seven);})
                      .curve(d3.curveMonotoneX);

    var eight_line = d3.line()
                       .x(function(d){return xScale(d.year);})
                       .y(function(d){return yScale(d.eight);})
                       .curve(d3.curveMonotoneX);
    
    // ADD THE AXES
    svg3a.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + (height - padding) + ")")
       .call(Xaxis)

    svg3a.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate("+padding+",0)")
       .call(Yaxis)

    // ADD THE LINES
    svg3a.append("path")
       .datum(data)
       .attr("class", "five_line")
       .attr("d", five_line);

    svg3a.append("path")
       .datum(data)
       .attr("class", "six_line")
       .attr("d", six_line);

    svg3a.append("path")
       .datum(data)
       .attr("class", "seven_line")
       .attr("d", seven_line);

    svg3a.append("path")
       .datum(data)
       .attr("class", "eight_line")
       .attr("d", eight_line);

    //AXES LABELS
    svg3a.append("text")
       .attr("text-anchor", "middle")
       .attr("transform", "translate(" + (0) + "," + (height/2)+ ")rotate(-90)")
       .attr("font-size", "20px")
       .attr("font-weight", "bold")
       .text("Num of Earthquakes")

    svg3a.append("text")
       .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
       .attr("transform", "translate("+ (width/2) +","+(height-(padding/8))+")")  // centre below axis
       .attr("font-size", "20px")
       .attr("font-weight", "bold")
       .text("Year");

    svg3a.append("text")
       .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
       .attr("transform", "translate("+ (width/2) +","+padding/3+")")  // centre below axis
       .attr("font-size", "30px")
       .attr("font-weight", "bolder")
       .text("Earthquake Statistics for 2000-2015");
       
    //LEGEND
    var colors = [{"level":'5_5.9', "color":'#FFC300'}, {"level":'6_6.9', "color": '#FF5733'}, {"level":'7_7.9', "color":'#C70039'}, {"level":'8.0+', "color":'#900C3F'}]
    legend = svg3a.append("g")
                .attr("class", "legend")
                .attr("transform", "translate("+(width-(2 * padding)) +",30)")
                .attr("height", 100)
                .attr("width", 100);


    legend.selectAll("rect")
          .data(colors)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("y", function(d,i){return i * 25;})
          .attr("width", 50)
          .attr("height", 20)
          .style("fill", function(d){return d.color;})

    legend.selectAll("text")
          .data(colors)
          .enter()
          .append("text")
          .attr("x", 55)
          .attr("y", function(d,i){return i*25 + 17;})
          .attr("font-size", "20px")
          .attr("font-weight", "bold")
          .text(function(d){return d.level;})
}).catch( (error) => {
    console.error(error)
});







///////////////////////////////////// 3B ///////////////////////////////////////////////////////
d3.dsv(",", "earthquakes.csv", function(d){
    return{
        year: parseTime(d.year),
        eight: +d["8.0+"],
        seven: +d["7_7.9"],
        six: +d["6_6.9"],
        five: +d["5_5.9"],
        deaths: +d["Estimated Deaths"]
    
      };
}).then(function(data){
    

    n = data.length;                               //Number of data points

    // SCALE GENERATORS
    var xScale = d3.scaleTime()
                   .domain([
                            d3.min(data, function(d){return d.year;}),
                            d3.max(data, function(d){return d.year;})
                   ])
                   .range([padding, width]);
    
    var yScale = d3.scaleLinear()
                   .domain([
                            0,
                            d3.max(data, function(d){return d.five;})
                   ])
                   .range([height-padding, padding])
                   
    //AXES DRAWN FROM SCALE GENERATORS
    var Xaxis = d3.axisBottom().scale(xScale).ticks(data.length);
    var Yaxis = d3.axisLeft().scale(yScale);
    
    //LINE GENERATORS
    var five_line = d3.line()
                 .x(function(d){return xScale(d.year);})
                 .y(function(d){return yScale(d.five);})
                 .curve(d3.curveMonotoneX);

    var six_line = d3.line()
                     .x(function(d){return xScale(d.year);})
                     .y(function(d){return yScale(d.six);})
                     .curve(d3.curveMonotoneX);

    var seven_line = d3.line()
                      .x(function(d){return xScale(d.year);})
                      .y(function(d){return yScale(d.seven);})
                      .curve(d3.curveMonotoneX);

    var eight_line = d3.line()
                       .x(function(d){return xScale(d.year);})
                       .y(function(d){return yScale(d.eight);})
                       .curve(d3.curveMonotoneX);

    // SCALER FOR DATA POINT SIZE
    var deathSizer = d3.scaleLinear().domain([0, d3.max(data, function(d){return d.deaths;})]).range([50,500])
    
    // ADD THE AXES
    svg3b.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + (height - padding) + ")")
       .call(Xaxis)

    svg3b.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate("+padding+",0)")
       .call(Yaxis)

    // ADD THE LINES
    svg3b.append("path")
       .datum(data)
       .attr("class", "five_line")
       .attr("d", five_line);

    svg3b.append("path")
       .datum(data)
       .attr("class", "six_line")
       .attr("d", six_line);

    svg3b.append("path")
       .datum(data)
       .attr("class", "seven_line")
       .attr("d", seven_line);

    svg3b.append("path")
       .datum(data)
       .attr("class", "eight_line")
       .attr("d", eight_line);

    //ADD THE SYMBOLS
    var symbols = svg3b.selectAll("circle").data(data)
    

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FFC300')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolCircle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.five) + ")"; });


    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FF5733')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolTriangle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.six) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#C70039')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolDiamond).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.seven) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#900C3F')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolSquare).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.eight) + ")"; });

    //AXES LABELS
    svg3b.append("text")
         .attr("text-anchor", "middle")
         .attr("transform", "translate(" + (0) + "," + (height/2)+ ")rotate(-90)")
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Num of Earthquakes")

    svg3b.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+(height-(padding/8))+")")  // centre below axis
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Year");

    svg3b.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+padding/3+")")  // centre below axis
         .attr("font-size", "30px")
         .attr("font-weight", "bolder")
         .text("Earthquake Statistics for 2000-2015 with Symbols");
       
    //LEGEND
    var colors = [{"level":'5_5.9', "color":'#FFC300'}, {"level":'6_6.9', "color": '#FF5733'}, {"level":'7_7.9', "color":'#C70039'}, {"level":'8.0+', "color":'#900C3F'}]
    legend = svg3b.append("g")
                  .attr("class", "legend")
                  .attr("transform", "translate("+(width-(2 * padding)) +",30)")
                  .attr("height", 100)
                  .attr("width", 100);


    legend.selectAll("rect")
          .data(colors)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("y", function(d,i){return i * 25;})
          .attr("width", 50)
          .attr("height", 20)
          .style("fill", function(d){return d.color;})

    legend.selectAll("text")
          .data(colors)
          .enter()
          .append("text")
          .attr("x", 55)
          .attr("y", function(d,i){return i*25 + 17;})
          .attr("font-size", "20px")
          .attr("font-weight", "bold")
          .text(function(d){return d.level;})
}).catch( (error) => {
    console.error(error)
});





///////////////////////////////////// 3C ///////////////////////////////////////////////////////
d3.dsv(",", "earthquakes.csv", function(d){
    return{
        year: parseTime(d.year),
        eight: +d["8.0+"],
        seven: +d["7_7.9"],
        six: +d["6_6.9"],
        five: +d["5_5.9"],
        deaths: +d["Estimated Deaths"]
    
      };
}).then(function(data){
    

    n = data.length;                               //Number of data points

    // SCALE GENERATORS
    var xScale = d3.scaleTime()
                   .domain([
                            d3.min(data, function(d){return d.year;}),
                            d3.max(data, function(d){return d.year;})
                   ])
                   .range([padding, width]);
    
    var yScale = d3.scaleSqrt()
                   .domain([
                            0,
                            d3.max(data, function(d){return d.five;})
                   ])
                   .range([height-padding, padding])
                   
    //AXES DRAWN FROM SCALE GENERATORS
    var Xaxis = d3.axisBottom().scale(xScale).ticks(data.length);
    var Yaxis = d3.axisLeft().scale(yScale);
    
    //LINE GENERATORS
    var five_line = d3.line()
                 .x(function(d){return xScale(d.year);})
                 .y(function(d){return yScale(d.five);})
                 .curve(d3.curveMonotoneX);

    var six_line = d3.line()
                     .x(function(d){return xScale(d.year);})
                     .y(function(d){return yScale(d.six);})
                     .curve(d3.curveMonotoneX);

    var seven_line = d3.line()
                      .x(function(d){return xScale(d.year);})
                      .y(function(d){return yScale(d.seven);})
                      .curve(d3.curveMonotoneX);

    var eight_line = d3.line()
                       .x(function(d){return xScale(d.year);})
                       .y(function(d){return yScale(d.eight);})
                       .curve(d3.curveMonotoneX);

    // SCALER FOR DATA POINT SIZE
    var deathSizer = d3.scaleLinear().domain([0, d3.max(data, function(d){return d.deaths;})]).range([50,500])
    
    // ADD THE AXES
    svg3c.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + (height - padding) + ")")
       .call(Xaxis)

    svg3c.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate("+padding+",0)")
       .call(Yaxis)

    // ADD THE LINES
    svg3c.append("path")
       .datum(data)
       .attr("class", "five_line")
       .attr("d", five_line);

    svg3c.append("path")
       .datum(data)
       .attr("class", "six_line")
       .attr("d", six_line);

    svg3c.append("path")
       .datum(data)
       .attr("class", "seven_line")
       .attr("d", seven_line);

    svg3c.append("path")
       .datum(data)
       .attr("class", "eight_line")
       .attr("d", eight_line);

    //ADD THE SYMBOLS
    var symbols = svg3c.selectAll("circle").data(data)
    

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FFC300')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolCircle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.five) + ")"; });


    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FF5733')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolTriangle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.six) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#C70039')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolDiamond).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.seven) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#900C3F')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolSquare).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.eight) + ")"; });

    //AXES LABELS
    svg3c.append("text")
         .attr("text-anchor", "middle")
         .attr("transform", "translate(" + (0) + "," + (height/2)+ ")rotate(-90)")
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Num of Earthquakes")

    svg3c.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+(height-(padding/8))+")")  // centre below axis
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Year");

    svg3c.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+padding/3+")")  // centre below axis
         .attr("font-size", "25px")
         .attr("font-weight", "bolder")
         .text("Earthquake Statistics for 2000-2015 (Square root Scale)");
       
    //LEGEND
    var colors = [{"level":'5_5.9', "color":'#FFC300'}, {"level":'6_6.9', "color": '#FF5733'}, {"level":'7_7.9', "color":'#C70039'}, {"level":'8.0+', "color":'#900C3F'}]
    legend = svg3c.append("g")
                  .attr("class", "legend")
                  .attr("transform", "translate("+(width-(2 * padding)) +",30)")
                  .attr("height", 100)
                  .attr("width", 100);


    legend.selectAll("rect")
          .data(colors)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("y", function(d,i){return i * 25;})
          .attr("width", 50)
          .attr("height", 20)
          .style("fill", function(d){return d.color;})

    legend.selectAll("text")
          .data(colors)
          .enter()
          .append("text")
          .attr("x", 55)
          .attr("y", function(d,i){return i*25 + 17;})
          .attr("font-size", "20px")
          .attr("font-weight", "bold")
          .text(function(d){return d.level;})
}).catch( (error) => {
    console.error(error)
});





///////////////////////////////////// 3Cb ///////////////////////////////////////////////////////
d3.dsv(",", "earthquakes.csv", function(d){
    return{
        year: parseTime(d.year),
        eight: +d["8.0+"],
        seven: +d["7_7.9"],
        six: +d["6_6.9"],
        five: +d["5_5.9"],
        deaths: +d["Estimated Deaths"]
    
      };
}).then(function(data){
    

    n = data.length;                               //Number of data points

    // SCALE GENERATORS
    var xScale = d3.scaleTime()
                   .domain([
                            d3.min(data, function(d){return d.year;}),
                            d3.max(data, function(d){return d.year;})
                   ])
                   .range([padding, width]);
    
    var yScale = d3.scaleLog().clamp(true)
                   .domain([
                            0.9,
                            d3.max(data, function(d){return d.five;})
                   ])
                   .range([height-padding, padding])
                   
                   
    //AXES DRAWN FROM SCALE GENERATORS
    var Xaxis = d3.axisBottom().scale(xScale).ticks(data.length);
    var Yaxis = d3.axisLeft().scale(yScale);
    
    //LINE GENERATORS
    var five_line = d3.line()
                 .x(function(d){return xScale(d.year);})
                 .y(function(d){return yScale(d.five);})
                 .curve(d3.curveMonotoneX);

    var six_line = d3.line()
                     .x(function(d){return xScale(d.year);})
                     .y(function(d){return yScale(d.six);})
                     .curve(d3.curveMonotoneX);

    var seven_line = d3.line()
                      .x(function(d){return xScale(d.year);})
                      .y(function(d){return yScale(d.seven);})
                      .curve(d3.curveMonotoneX);

    var eight_line = d3.line()
                       .x(function(d){return xScale(d.year);})
                       .y(function(d){return yScale(d.eight);})
                       .curve(d3.curveMonotoneX);

    // SCALER FOR DATA POINT SIZE
    var deathSizer = d3.scaleLinear().domain([0, d3.max(data, function(d){return d.deaths;})]).range([50,500])
    
    // ADD THE AXES
    svg3cb.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + (height - padding) + ")")
       .call(Xaxis)

    svg3cb.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate("+padding+",0)")
       .call(Yaxis)

    // ADD THE LINES
    svg3cb.append("path")
       .datum(data)
       .attr("class", "five_line")
       .attr("d", five_line);

    svg3cb.append("path")
       .datum(data)
       .attr("class", "six_line")
       .attr("d", six_line);

    svg3cb.append("path")
       .datum(data)
       .attr("class", "seven_line")
       .attr("d", seven_line);

    svg3cb.append("path")
       .datum(data)
       .attr("class", "eight_line")
       .attr("d", eight_line);

    //ADD THE SYMBOLS
    var symbols = svg3cb.selectAll("circle").data(data)
    

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FFC300')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolCircle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.five) + ")"; });


    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#FF5733')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolTriangle).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.six) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#C70039')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolDiamond).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.seven) + ")"; });

    symbols.enter()
           .append("path")
           .attr("class", "point")
           .attr('fill', '#900C3F')
           .attr('stroke', '#000')
           .attr('stroke-width', 1)
           .attr("d", d3.symbol().type(d3.symbolSquare).size(function(d){return deathSizer(d.deaths)}))
           .attr("transform", function(d) { return "translate(" + xScale(d.year) + "," + yScale(d.eight) + ")"; });

    //AXES LABELS
    svg3cb.append("text")
         .attr("text-anchor", "middle")
         .attr("transform", "translate(" + (0) + "," + (height/2)+ ")rotate(-90)")
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Num of Earthquakes")

    svg3cb.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+(height-(padding/8))+")")  // centre below axis
         .attr("font-size", "20px")
         .attr("font-weight", "bold")
         .text("Year");

    svg3cb.append("text")
         .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
         .attr("transform", "translate("+ (width/2) +","+padding/3+")")  // centre below axis
         .attr("font-size", "30px")
         .attr("font-weight", "bolder")
         .text("Earthquake Statistics for 2000-2015 (Log Scale)");
       
    //LEGEND
    var colors = [{"level":'5_5.9', "color":'#FFC300'}, {"level":'6_6.9', "color": '#FF5733'}, {"level":'7_7.9', "color":'#C70039'}, {"level":'8.0+', "color":'#900C3F'}]
    legend = svg3cb.append("g")
                  .attr("class", "legend")
                  .attr("transform", "translate("+(width-(2 * padding)) +",120)")
                  .attr("height", 100)
                  .attr("width", 100);


    legend.selectAll("rect")
          .data(colors)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("y", function(d,i){return i * 20;})
          .attr("width", 40)
          .attr("height", 10)
          .style("fill", function(d){return d.color;})

    legend.selectAll("text")
          .data(colors)
          .enter()
          .append("text")
          .attr("x", 52)
          .attr("y", function(d,i){return i*19 + 10;})
          .attr("font-size", "12px")
          .attr("font-weight", "bold")
          .text(function(d){return d.level;})
}).catch( (error) => {
    console.error(error)
});
