var margin = {top: 20, right: 20, bottom:50, left:50},
             width = 900 - margin.left - margin.right,
             height = 500 - margin.top - margin.bottom;

var padding = 50;

var svg = d3.select("div.lineChart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y")


d3.dsv(",", "state-year-earthquakes.csv", function(d){
    return{
            year: d.year,
            state: d.state,
            region: d.region,
            count: +d.count
                  };
            }).then(function(data){
                var regions = d3.nest().key(function(d){                                                              //group by region
                                                        return d.region;
                                                       })
                                       .key(function(d){                                                             //group by year
                                                        return d.year;
                                                       })
                                       .rollup(function(v){                                                          //return the sum of count
                                                        return d3.sum(v, function(d){
                                                                                     return d.count;}
                                                                     );
                                                          })
                                       .entries(data);                                                               //return it as a direct entries

            
            var maxVal = d3.max(regions.map(d => d3.max(d.values.map(v => v.value))));                              //Max count value from regions array
            

           
            /////////////////////////////// SCALES AND AXES///////////////////////////////
            xScale = d3.scaleTime().domain([
                                            d3.min(data, function(d){return parseTime(d.year);}),
                                            d3.max(data, function(d){return parseTime(d.year);})
                                           ])
                                   .range([padding, width]);
            
            yScale = d3.scaleLinear().domain([0, maxVal]).range([height-padding, padding])

            xAxis = d3.axisBottom().scale(xScale).ticks(5);
            yAxis = d3.axisLeft().scale(yScale);

            ///////////////////////////////LINE GENERATORS ////////////////////////////////
            var lineGen = d3.line()
                              .x(function(d){return xScale(parseTime(d.key));})
                              .y(function(d){return yScale(d.value);})
                              //.curve(d3.curveMonotoneX);

            /////////////////////////// ADD THE AXES ///////////////////////////////////////
            svg.append("g")
               .attr("class", "x axis")
               .attr("transform", "translate(0," + (height-padding) + ")")
               .call(xAxis);

            svg.append("g")
               .attr("class", "y axis")
               .attr("transform", "translate(" + padding + ",0)")
               .call(yAxis);

            //////////////////////////// ADD THE LINES //////////////////////////////////////
            svg.append("path")
               .datum(regions[0].values)
               .attr("class", "southLine")
               .attr("d", lineGen);

            svg.append("path")
               .datum(regions[1].values)
               .attr("class", "westLine")
               .attr("d", lineGen)

            svg.append("path")
               .datum(regions[2].values)
               .attr("class", "northeastLine")
               .attr("d", lineGen)
            
            svg.append("path")
               .datum(regions[3].values)
               .attr("class", "midwestLine")
               .attr("d", lineGen)   
            
            //////////////////////// ADD MARKERS /////////////////////////////////////
            var markersSouth = svg.selectAll("circle.south").data(regions[0].values);
            var markersWest = svg.selectAll("circle.west").data(regions[1].values);
            var markersNorth = svg.selectAll("circle.north").data(regions[2].values);
            var markersMid = svg.selectAll("circle.mid").data(regions[3].values);
           
            var southBarChart = barChart(regions[0].key, data)
            var westBarChart = barChart(regions[1].key, data)
            var northBarChart = barChart(regions[2].key, data)
            var midBarChart = barChart(regions[3].key, data)

            markersSouth.enter()
                   .append("circle")
                   .attr("class", "point")
                   .attr('fill', 'green')       
                   .attr('stroke', 'white')
                   .attr('stroke-width', 2)
                   .attr("cx", function(d){return xScale(parseTime(d.key))})
                   .attr("cy", function(d){return yScale(d.value)})
                   .attr("r", 5)
                   .on("mouseover", function(d,i){
                      
                       d3.select(this).attr("r", 10);

                       southBarChart(d,i);
                      
                   })
                   .on("mouseout", function(){
                       d3.select(this).attr("r", 5);
                       d3.select("div.barChart").selectAll("*").remove();
                   });

            markersWest.enter()
                   .append("circle")
                   .attr("class", "point")
                   .attr('fill', 'purple')
                   .attr('stroke', 'white')
                   .attr('stroke-width', 2)
                   .attr("cx", function(d){return xScale(parseTime(d.key))})
                   .attr("cy", function(d){return yScale(d.value)})
                   .attr("r", 5)
                   .on("mouseover", function(d,i){
                      
                    d3.select(this).attr("r", 10);

                    westBarChart(d,i);
                   
                })
                .on("mouseout", function(){
                    d3.select(this).attr("r", 5);
                    d3.select("div.barChart").selectAll("*").remove();
                });

            markersNorth.enter()
                   .append("circle")
                   .attr("class", "point")
                   .attr('fill', 'blue')
                   .attr('stroke', 'white')
                   .attr('stroke-width', 2)
                   .attr("cx", function(d){return xScale(parseTime(d.key))})
                   .attr("cy", function(d){return yScale(d.value)})
                   .attr("r", 5)
                   .on("mouseover", function(d,i){
                      
                    d3.select(this).attr("r", 10);

                    northBarChart(d,i);
                   
                })
                .on("mouseout", function(){
                    d3.select(this).attr("r", 5);
                    d3.select("div.barChart").selectAll("*").remove();
                });

            markersMid.enter()
                   .append("circle")
                   .attr("class", "point")
                   .attr('fill', 'red')
                   .attr('stroke', 'white')
                   .attr('stroke-width', 2)
                   .attr("cx", function(d){return xScale(parseTime(d.key))})
                   .attr("cy", function(d){return yScale(d.value)})
                   .attr("r", 5)
                   .on("mouseover", function(d,i){
                      
                    d3.select(this).attr("r", 10);

                    midBarChart(d,i);
                   
                })
                .on("mouseout", function(){
                    d3.select(this).attr("r", 5);
                    d3.select("div.barChart").selectAll("*").remove();
                });
            

            /////////////////////// LEGEND /////////////////////////////////////////
            const colors = ['green', 'purple', 'blue', 'red'];
            
            var legend = svg.append("g")
                            .attr("height", padding)
                            .attr("width", 100)
                            .attr("transform", "translate(" + (width-(padding*1.5)) + "," + (padding * 2) + ")");

            legend.selectAll("circle.legend")
                  .data(regions)
                  .enter()
                  .append("circle")
                  .attr("cx", 0)
                  .attr("cy", function(d,i){return i * 25;})
                  .attr("r", 5)
                  .style("fill", function(d,i){return colors[i];});

            
            legend.selectAll("legend.text")
                  .data(regions)
                  .enter()
                  .append("text")
                  .attr("font-weight", "bold")
                  .attr("x", 12)
                  .attr("y", function(d,i){return i * 25 + 5 ;})
                  .text(function(d){return d.key;})

            ///////////////////////// TITLE /////////////////////////////////////
            svg.append("text")
               .attr("text-anchor", "middle")
               .attr("transform", "translate("+ (width/2) +","+padding/3+")")
               .attr("font-size", "40px")
               .attr("font-weight", "bolder")
               .text("US Earthquakes by Region 2011-2015");

            svg.append("text")
               .attr("text-anchor", "middle")
               .attr("transform", "translate("+ (width/2) +","+padding+")")
               .attr("font-size", "20px")
               .attr("font-weight", "bolder")
               .attr("stroke", "blue")
               .text("ksims35");
            

               

            }).catch( (error) => {
                console.error(error)
            });
            



//////// CLOSURE FUNCTON FOR BARCHAR MOUSEOVER
function barChart(r, da){
                        let region = r;   // Region as set by closure function
                        let data = da;    // Placeholder for full CSV data
                        return (d,i) => {
                                                
                                                
                                                var year = d.key;   
                                                /////////////////// FILTER AND SORT DATA FOR YEAR AND REGION ////////////////////////
                                                var filteredData = data.filter(d => (d.region == region) & (d.year == year.toString()))
                                                                       .sort(function (a,b){ 
                                                                                            if (a.count > b.count) return -1; 
                                                                                            if (a.count < b.count) return 1; 
                                                                                            if (a.state > b.state) return -1; 
                                                                                            if (a.state < b.state) return 1;
                                                                                          });

                                                
                                                
                                                
                                                const barHeight = 15;
                                                const width = 900;
                                                const height = filteredData.length * (barHeight * 2);
                                                const margin = { top: 50, right: 30, bottom: 20, left: 100 };

                                            

                                                const container = d3.select("div.barChart");

                                                // container.selectAll("*").remove()
                                                
                                                const chart = container.append('svg')
                                                    .style('width', width)
                                                    .attr('height', height)
                                                    .attr('transform', `translate(0, ${-80})`)
                                                const xScale = d3.scaleLinear()
                                                    .range([0, width - margin.left - margin.right])
                                                    .domain([0, d3.max(filteredData, d => d.count)]);
                                                
                                                const yScale = d3.scaleBand()
                                                    .range([0, height - margin.top - margin.bottom])
                                                    .domain(filteredData.map(d => d.state));
                                                
                                                // const color = d3.scaleOrdinal()
                                                //     .range(d3.schemeCategory10)
                                                //     .domain(filteredData.map(d => d.state));
                                                
                                                const yAxis = chart.append('g')
                                                    .call(d3.axisLeft(yScale))
                                                    .attr('transform', `translate(${margin.left}, ${margin.top})`);

                                                const xAxis = chart.append('g')
                                                                   .call(d3.axisBottom(xScale))
                                                                   .attr("transform", `translate(${margin.left}, ${(height-margin.bottom)})`);
                                                
                                                chart.selectAll('.bar')
                                                    .data(filteredData)
                                                    .enter()
                                                    .append('rect')
                                                    .attr('class', 'bar')
                                                    .attr('fill', "blue")
                                                    .attr('stroke', "black")
                                                    .attr('height', barHeight)
                                                    .attr('width', d => xScale(d.count))
                                                    .attr('x', margin.left + 1)
                                                    .attr('y', d => yScale(d.state) + (barHeight / 2) + 50);
                                                
                                                chart.selectAll('.label')
                                                    .data(filteredData)
                                                    .enter()
                                                    .append('text')
                                                    .attr('class', 'label')
                                                    .attr('alignment-baseline', 'middle')
                                                    .attr('x', d => xScale(d.count) + margin.left + 5)
                                                    .attr('y', d => yScale(d.state) + (barHeight) + 50)
                                                    .style('font-size', '12px')
                                                    .style('font-weight', 'bold')
                                                    .text(d => d.count);

                                                chart.append("text")
                                                     .attr("text-anchor", "middle")
                                                     .attr("transform", "translate("+ (width/2) +","+(50/2)+")")
                                                     .attr("font-size", "20px")
                                                     .attr("font-weight", "bolder")
                                                     .text(`${region} Region Earthquakes ${year}`);


                                                yAxis.selectAll('text').style('font-size', '12px').style('font-weight', 'bolder');
                                                xAxis.selectAll('text').style('font-size', '12px').style('font-weight', 'bolder')
};}