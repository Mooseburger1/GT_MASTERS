

// get the data
links =  [
  {
    "source": "Milwaukee Bucks",
    "target": "Cleveland Cavaliers",
    "value": 0
  },
  {
    "source": "Milwaukee Bucks",
    "target": "Sacramento Kings",
    "value": 0
  },
  {
    "source": "Detroit Pistons",
    "target": "Philadelphia 76ers",
    "value": 1
  },
  {
    "source": "Cleveland Cavaliers",
    "target": "Los Angeles Lakers",
    "value": 1
  },
  {
    "source": "Dallas Mavericks",
    "target": "Houston Rockets",
    "value": 1
  },
  {
    "source": "Miami Heat",
    "target": "San Antonio Spurs",
    "value": 1
  },
  {
    "source": "Miami Heat",
    "target": "Los Angeles Lakers",
    "value": 1
  },
  {
    "source": "Brooklyn Nets",
    "target": "Los Angeles Lakers",
    "value": 1
  },
  {
    "source": "Brooklyn Nets",
    "target": "Houston Rockets",
    "value": 1
  },
  {
    "source": "Sacramento Kings",
    "target": "Los Angeles Lakers",
    "value": 1
  },
  {
    "source": "Houston Rockets",
    "target": "Golden State Warriors",
    "value": 0
  },
  {
    "source": "Los Angeles Lakers",
    "target": "Los Angeles Clippers",
    "value": 1
  },
  {
    "source": "Sacramento Kings",
    "target": "Philadelphia 76ers",
    "value": 1
  },
  {
    "source": "San Antonio Spurs",
    "target": "Miami Heat",
    "value": 0
  },
  {
    "source": "Portand Trail Blazers",
    "target": "Miami Heat",
    "value": 0
  },
  {
    "source": "Chicago Bulls",
    "target": "Boston Celtics",
    "value": 0
  },
  {
    "source": "New York Knicks",
    "target": "Golden State Warriors",
    "value": 0
  },
  {
    "source": "Denver Nuggets",
    "target": "Golden State Warriors",
    "value": 0
  },
  {
    "source": "Portand Trail Blazers",
    "target": "Golden State Warriors",
    "value": 0
  },
  {
    "source": "New York Knicks",
    "target": "Denver Nuggets",
    "value": 1
  },
  {
    "source": "San Antonio Spurs",
    "target": "Denver Nuggets",
    "value": 0
  },
  {
    "source": "Houston Rockets",
    "target": "Denver Nuggets",
    "value": 1
  },
  {
    "source": "Portand Trail Blazers",
    "target": "San Antonio Spurs",
    "value": 1
  },
  {
    "source": "Houston Rockets",
    "target": "Brooklyn Nets",
    "value": 0
  },
  {
    "source": "Milwaukee Bucks",
    "target": "Boston Celtics",
    "value": 0
  },
  {
    "source": "Golden State Warriors",
    "target": "Milwaukee Bucks",
    "value": 1
  },
  {
    "source": "Golden State Warriors",
    "target": "Atlanta Hawks",
    "value": 1
  },
  {
    "source": "Orlando Magic",
    "target": "Memphis Grizzlies",
    "value": 0
  },
  {
    "source": "Washington Wizards",
    "target": "New York Knicks",
    "value": 1
  },
  {
    "source": "Boston Celtics",
    "target": "Orlando Magic",
    "value": 1
  },
  {
    "source": "Oklahoma City Thunder",
    "target": "Sacramento Kings",
    "value": 0
  },
  {
    "source": "Boston Celtics",
    "target": "Charlotte Hornets",
    "value": 1
  },
  {
    "source": "Boston Celtics",
    "target": "Philadelphia 76ers",
    "value": 1
  },
  {
    "source": "Brooklyn Nets",
    "target": "Miami Heat",
    "value": 1
  },
  {
    "source": "Indiana Pacers",
    "target": "Chicago Bulls",
    "value": 1
  },
  {
    "source": "New York Knicks",
    "target": "Boston Celtics",
    "value": 0
  },
  {
    "source": "Los Angeles Lakers",
    "target": "Phoenix Suns",
    "value": 0
  },
  {
    "source": "Golden State Warriors",
    "target": "Dallas Mavericks",
    "value": 1
  },
  {
    "source": "New Orleans Pelicans",
    "target": "Indiana Pacers",
    "value": 0
  },
  {
    "source": "Milwaukee Bucks",
    "target": "Brooklyn Nets",
    "value": 0
  },
  {
    "source": "Washington Wizards",
    "target": "Portand Trail Blazers",
    "value": 1
  },
  {
    "source": "Utah Jazz",
    "target": "Golden State Warriors",
    "value": 1
  },
  {
    "source": "Boston Celtics",
    "target": "Utah Jazz",
    "value": 1
  },
  {
    "source": "Golden State Warriors",
    "target": "Charlotte Hornets",
    "value": 1
  },
  {
    "source": "Boston Celtics",
    "target": "Atlanta Hawks",
    "value": 1
  },
  {
    "source": "Philadelphia 76ers",
    "target": "Boston Celtics",
    "value": 0
  }
];

var nodes = {};

// compute the distinct nodes from the links.
links.forEach(function(link) {
    link.source = nodes[link.source] ||
        (nodes[link.source] = {name: link.source});
    link.target = nodes[link.target] ||
        (nodes[link.target] = {name: link.target});
});

var width = 1200,
    height = 700;

var force = d3.forceSimulation()
    .nodes(d3.values(nodes))
    .force("link", d3.forceLink(links).distance(100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force("x", d3.forceX())
    .force("y", d3.forceY())
    .force("charge", d3.forceManyBody().strength(-250))
    .alphaTarget(1)
    .on("tick", tick);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

// add the links and the arrows
var path = svg.append("g")
    .selectAll("path")
    .data(links)
    .enter()
    .append("path")
    .attr("class", function(d){                                            //Change the class of each path depending on data value
        if (d.value == 0){
            return "edge_zero";                                           //If value is 0 change class to edge_zero and update formatting via CSS
        }
        else{
            return "edge_one";                                            //If value is 1 change class to edge_one and update formatting via CSS
        }
    });
    //.attr("class", function(d) { return "link " + d.type; });

//function for pinning nodes
function pinned(d){

    if (d.fixed == false || d.fixed == null){
        d.fixed = true;

        d3.select(this).selectAll("text").attr("class", "pinned");
    }
    else{
        d3.select(this).selectAll("text").attr("class", "labels");
        d.fixed = false;
        dragended(d);

       
        
       

        
      
};
};
//Scaler for node radius
var radiusScaler = d3.scaleLinear().domain([0,20]).range([10,100]);                                      //Scaler for node radius size
var color = ["#f7fbff","#e3eef9","#cfe1f2","#b5d4e9","#93c3df","#6daed5","#4b97c9","#2f7ebc","#1864aa","#0a4a90","#08306b"]     //ColorBrewer Scale
// define the nodes
var node = svg.selectAll(".node")
    .data(force.nodes())
    .enter().append("g")
    .attr("class", "node")
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
    .on("dblclick", pinned);
    

// add the nodes
node.append("circle")
    .attr("r", function(d){
        d.weight = links.filter(function(l){
            return l.source.index == d.index || l.target.index == d.index;
        }).length;

        
        return radiusScaler(d.weight);
    })
    .attr("fill", function(d){
        d.weight = links.filter(function(l){
            return l.source.index == d.index || l.target.index == d.index;
        }).length;

        
        return color[d.weight];

    });

// Add node labels
var labels = node.append("text")                        //Append "text" elements
                 .text(function(d) {                    //nodes have a __data__ attribute which contains name, x, and y
                     return d.name;                     //return d.name for name attr
                 })
                 .attr('x', 6)
                 .attr('y', 12)
                 .attr("class", "labels");




// add the curvy lines
function tick() {
    path.attr("d", function(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" +
            d.source.x + "," +
            d.source.y + "A" +
            dr + "," + dr + " 0 0,1 " +
            d.target.x + "," +
            d.target.y;
    });

    node
        .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")"; })
};

function dragstarted(d) {
    if (!d3.event.active) force.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
};

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
};

function dragended(d) {
    if (!d3.event.active) force.alphaTarget(0);
    if (d.fixed == true) {
        d.fx = d.x;
        d.fy = d.y;
    }
    else {
        d.fx = null;
        d.fy = null;
    }
};



//My credentials
svg.append("text")
   .attr("x", 900)
   .attr("y", 20)
   .style("font-size", "16px")
   .text("ksims35")
