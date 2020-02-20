var margin = {top: 20, right: 20, bottom:50, left:50},
             width = 900 - margin.left - margin.right,
             height = 500 - margin.top - margin.bottom;

var padding = 20;

var parseTime = d3.timeParse("%Y")


d3.dsv(",", "earthquake.csv", function(d){
    return{
            year: d.Year,
            state: d.State,
            seven: +d['7.0+'],
            six: +d['6_6.9'],
            five: +d['5_5.9']
            
            
                  };
            }).then(function(data){
                                    
                                    //////////////// DATA CONSTANTS ////////////////////////
                                    const cols = d3.keys(d3.values(data)[0]).slice(2);
                                    const years = d3.set(data.map(d => d.year)).values();
                                    const states = d3.set(data.map(d => d.state)).values();

                                    ///////////////////////// SCALES /////////////////////////////////
                                    const xScale = d3.scaleBand()
                                                     .domain(data.map(d => d.state))
                                                     .range([margin.left, width-padding]);

                                    const yScale = d3.scaleLinear()
                                                     .range([height, padding]);

                                    const colorScale = d3.scaleOrdinal()
                                                     .domain([cols])
                                                     .range(['#f2b447','#b33040','#d25c4d'])

                                    
                                    //////////////// YEAR SELECTOR ////////////////////////
                                    const yearSelector = d3.select('select');

                                    yearSelector.selectAll('option')
                                                .data(years)
                                                .enter()
                                                .append('option')
                                                .text(d => d)
                                    
                                    yearSelector.on("change", function(){
                                         d3.select('div.barChart').selectAll("*").remove();
                                         barChart(this.value)
                                    });

                                    ////////////// BAR CHART FUNCTION //////////////////////

                                    const barChart = function(year){
                                                                    //filter data for the year selected
                                                                    var filteredData = data.filter(d => d.year == year)
                                                          

                                                                    //get the max y value for the yScale
                                                                    const maxY = d3.max(filteredData.map(d => d.seven + d.six + d.five));

                                                                    //sums
                                                                    const sums = filteredData.map(d => d.seven + d.six + d.five);
                                                                    

                                                                    //update yScale domain
                                                                    yScale.domain([0, maxY + 100])

                                                                    //stack the data
                                                                    const dataStack = d3.stack().keys(cols)(filteredData).map(d => (d.forEach(v => v.key = d.key), d));
                                                             
                                                                    // svg element bounded to div
                                                                    var svg = d3.select("div.barChart")
                                                                                .append("svg")
                                                                                .attr("width", width + margin.left + margin.right)
                                                                                .attr("height", height + margin.top + margin.bottom)
                                                                                .append("g")
                                                                                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
                                                                    
                                                                    ///////////////////////// AXES /////////////////////////////////
                                                                    const xAxis = svg.append('g')
                                                                                    .call(d3.axisBottom(xScale))
                                                                                    .attr('transform', `translate(${0} , ${(height)})`);
                                                                    xAxis.selectAll('text').style('font-weight', 'bold')

                                                                    const yAxis = svg.append('g')
                                                                                    .call(d3.axisLeft(yScale))
                                                                                    .attr('transform', `translate(${margin.left}, ${0})`);
                                                                    yAxis.selectAll('text').style('font-weight', 'bold')
                                                                    //////////////////////// LEGEND ////////////////////////////////
                                                                    const severity = ['7.0+','6_6.9','5_5.9'];
                                                                    
                                                                    const legend = svg.append('g')
                                                                                    .attr('class', 'legend')
                                                                                    .attr('height', 100)
                                                                                    .attr('width', 100)
                                                                                    .attr('transform', `translate(${(width-padding)} , ${(padding/2)})`)

                                                                    legend.selectAll('circle')
                                                                        .data(cols)
                                                                        .enter()
                                                                        .append('circle')
                                                                        .attr('fill', d => colorScale(d))
                                                                        .attr('stroke', 'black')
                                                                        .attr('stroke-width', 1)
                                                                        .attr('cx', 0)
                                                                        .attr('cy', function(d,i){return i * 15})
                                                                        .attr('r', 5)

                                                                    legend.selectAll('text.legend')
                                                                        .data(severity)
                                                                        .enter()
                                                                        .append('text')
                                                                        .style('font-size', '10px')
                                                                        .style('font-weight', 'bolder')
                                                                        .attr('x', 8)
                                                                        .attr('y', (d,i) => {return i*15 + 3})
                                                                        .text(d => d);

                                                                    /////////////////////// BARS ////////////////////////////////////


                                                                    const chart = svg.append("g")
                                                                       chart.selectAll("g")
                                                                       .data(dataStack)
                                                                       .enter()
                                                                       .append("g")
                                                                       .attr("fill", d => colorScale(d.key))
                                                                       .selectAll("rect")
                                                                       .data(d => d)
                                                                       .enter()
                                                                       .append("rect")
                                                                       .attr("x", (d) => xScale(d.data.state)+10)
                                                                       .attr("y", d => yScale(d[1]))
                                                                       .attr("height", d => yScale(d[0]) - yScale(d[1]))
                                                                       .attr("width", xScale.bandwidth() - 10)

                                                                    //////////////////// LABELS //////////////////////////////////////////
                                                                    const valueLabels = svg.selectAll('text.label')

                                                                    valueLabels.data(sums)
                                                                              .enter()
                                                                              .append('text')
                                                                              .attr('x', function(d,i){return xScale(states[i])+45;})
                                                                              .attr('y', function(d){return yScale(+d)- 5;})
                                                                              .text(d => d)

                                                                    /////////////////// TITLE //////////////////////////////////////
                                                                    svg.append("text")
                                                                       .attr("text-anchor", "middle")
                                                                       .attr("transform", "translate("+ (width/2) +","+padding/3+")")
                                                                       .attr("font-size", "20px")
                                                                       .attr("font-weight", "bolder")
                                                                       .text("Visualizing Earthquake Counts by State");

                                                                    svg.append("text")
                                                                       .attr("text-anchor", "right")
                                                                       .attr("transform", "translate("+ (width-(padding * 5)) +","+(height + 50)+")")
                                                                       .attr("font-size", "15px")
                                                                       .attr("stroke", "black")
                                                                       .text("ksims35");

                                                                    svg.append("text")
                                                                       .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
                                                                       .attr("transform", "translate("+ (width/2) +","+(height+35) + ")")  // centre below axis
                                                                       .attr("font-size", "15px")
                                                                       .text("State");

                                                                    svg.append("text")
                                                                       .attr("text-anchor", "middle")
                                                                       .attr("transform", "translate(" + (0) + "," + (height/2)+ ")rotate(-90)")
                                                                       .attr("font-size", "15px")
                                                                       .text("Number of Earthquakes")
                                                                    
                                                            
                                                                    

                                        
                                    };

                                    ////////////////////// INITIALIZE BAR CHART ON PAGE LOAD /////////////////
                                    barChart(years[0])


            }).catch( (error) => {
                console.error(error)
            });