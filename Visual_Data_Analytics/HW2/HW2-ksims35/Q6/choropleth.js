var margin = {top: 20, right: 20, bottom:50, left:0},
             width = 1000 - margin.left - margin.right,
             height = 500 - margin.top - margin.bottom;

var padding = 50;

  var sliderTime = d3
    .sliderBottom()
    .min(2010)
    .max(2015)
    .step(1)
    .width(500)
    .tickFormat(d3.format('d'))
    .default(2010)
    .ticks(6)
    .on('onchange',val =>{
      
    
        d3.select('div.map').selectAll('*').remove();
        Promise.all(promises).then(function(d){ ready(d, val)});

    });

  var gTime = d3
    .select('div#slider-time')
    .append('svg')
    .attr('width', 800)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

  gTime.call(sliderTime);



var parseTime = d3.timeParse("%Y")




var map = d3.map();

const projection = d3.geoAlbersUsa()
                     .translate([width/2, height/2])
                     .scale(1000);

var path = d3.geoPath().projection(projection);

var x = d3.scaleLog()
          .domain([])
          .range([]);

var color = d3.scaleThreshold()
              .range(d3.schemeBlues[9])


var promises = [
d3.json('states-10m.json'),
d3.csv( "state-earthquakes.csv")
        ];

Promise.all(promises).then(function(d){ ready(d, 2010)})


function ready(us, year){
    var svg = d3.select("div.map")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    ////////////// DOMAIN FOR COLOR SCALER /////////////////
    function makeArr(startValue, stopValue, cardinality) {
        var arr = [];
        var step = (stopValue - startValue) / (cardinality - 1);
        for (var i = 0; i < cardinality; i++) {
          arr.push(startValue + (step * i));
        }
        return arr;
      }

    const maxVal = d3.max(us[1].map(d => +d[year]));
    var minVal = d3.min(us[1].map(d => +d[year]));
    
    if(minVal <= 0){minVal = 1}

    const logMin = Math.log(minVal);
    const logMax = Math.log(maxVal)
    
    

    nineGradationsLog = makeArr(0, logMax, 9)
    nineGradations = nineGradationsLog.map(d => Math.exp(d)).map(d => parseInt(d));
    nineGradations[0] = 0;
    color.domain(nineGradationsLog);



    ////////////// DRAW THE MAP ////////////////////////////
    const map = svg.append('g');

    map.selectAll('path')
       .data(topojson.feature(us[0], us[0].objects.states).features)
       .enter()
       .append('path')
       .style('stroke', 'black')
       .attr('fill', function(d){return  color(getStateValue(d.properties.name, us[1]))})
       .attr('d', path)
       .on('mouseover', d => tip.show(getStateInfo(d.properties.name, us[1])))
       .on('mouseout', d => tip.hide(d))
       

    ///////////////////// MAP STATE VALUE FROM OBJECTS TO ACTUAL DATA //////////////////////////   
    function getStateValue(state, data){
                                        var stateRow = data.filter(d => d.States == state);
                                        
                                        if (stateRow.length == 0){
                                            return 0
                                        }else if (stateRow[0][year] == 0){
                                                return 0
                                        }else{
                                            
                                            return Math.log(stateRow[0][year])
                                        }
                                    }

    function getStateInfo(state, data){
                                       var stateRow = data.filter(d => d.States == state);
                                       const numEarthquakes = stateRow[0][year]
                                       const region = stateRow[0].Region

                                       return {'state':state, 'year':year, 'region':region, 'count':numEarthquakes}
    }

    ///////////////////// LEGEND //////////////////////////////////////////
    const legend = svg.append('g')
                      .attr('class', 'legend')
                      .attr('transform', `translate(${(width-(1.5 *padding))}, ${padding})`);

    
    legend.selectAll('rect')
          .data(nineGradationsLog)
          .enter()
          .append('rect')
          .attr('x', 0)
          .attr('y', (d, i) => i * 40)
          .attr('height', 30)
          .attr('width', 30)
          .style('stroke', 'black')
          .attr('fill', d => color(d))
          

    legend.selectAll('text')
          .data(nineGradations)
          .enter()
          .append('text')
          .attr('x', 40)
          .attr('y', (d,i) => i * 40 + 25)
          .style('font-weight', 'bold')
          .text(d => d)

    svg.append("text")
          .attr("text-anchor", "right")
          .attr("transform", "translate("+ (width-(padding * 5)) +","+(height + 50)+")")
          .attr("font-size", "15px")
          .attr("stroke", "black")
          .text("ksims35");

    /////////////////////////// TOOL TIP //////////////////////////////////////////
    var tip = d3.tip()
                .attr('class', 'd3-tip')
                .style('background', 'black')
                .style('color', 'white')
                .style('line-height', 1)
                .style('font-weight', 'bold')
                .style('padding', '12px')
                .style('border-radius', '2px')
                .offset([-10, 0])
                .html(function(d){return "<strong>State:</strong> <span style='color:red'>" + d.state + "</span>" + 
                                         "</br><strong>Region:</strong> <span style='color:red'>" + d.region + "</span>" +
                                         "</br><strong>Year:</strong> <span style='color:red'>" + d.year + "</span>" +
                                         "</br><strong>Earthquakes:</strong> <span style='color:red'>" + d.count + "</span>" ;})
    svg.call(tip);
}




