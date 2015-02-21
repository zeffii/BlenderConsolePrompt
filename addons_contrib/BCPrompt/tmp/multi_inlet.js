/* SHARED FUNCTIONS*/

function getArray(obj) {
  var data = [];
  for(var prop in obj) {
    if(obj.hasOwnProperty(prop)){
      data.push(obj[prop]);
    }
  }
  return data
}

function translate(a, b) { 
  return "translate(" + [a, b] + ")" 
}

// Collect Totals
// Possibly totals should be calculated a different way than
// the current code does.
// * namely : a = get first start, 
// *          b = get last start + last duration
// *          c = delta(b, a)
// on small graphs, the time spent in between function calls to 
// each graph is almost as large as the graph takes to process.

var totals = 0;
for (var graph_idx in tributary.terrible.graphs){
  var u_graph = tributary.terrible.graphs[graph_idx];
  for (var item_idx in u_graph.items){
      totals += (u_graph.items[item_idx].duration * 1000);
  }
}


d3.select("body").style("background-color", d3.rgb(240,240,240));

var margin = {top: 16, right: 6, bottom: 30, left: 103},
    width = 900 - margin.left - margin.right,
    height = 116 - margin.top - margin.bottom;

var scalar = width/totals;
var barheight = 15;
var tx = 103;  // internal x position.


/* UNIQUE FUNCTIONS PER SVG */

function draw_graph(u_graph){

    var graphname = u_graph.name.replace(/\./g, '_')
    console.log(graphname);
    var disp = d3.select('#display')
    var svg = disp.append('svg').attr({'id': graphname});

    var data = getArray(u_graph.items);
    var num_bars = data.length + 2;

    var bars = (num_bars * barheight);
    var svg_height = bars + 77 + margin.top + margin.bottom;
    svg.attr({height: svg_height, width: 964})
      .style({border: "1px solid #d6d6d6"});

    var num_keys = data.length;

    var group2 = svg.append("g")
      .attr({transform: function(d){ return translate(tx, -32) } })

    var group3 = svg.append("g")
      .attr({transform: function(d){ return translate(tx, -11) } })

    var group1 = svg.append("g")
      .attr({transform: function(d){ return translate(tx, 77) } })

    var name_group = svg.append("g")
      .attr({transform: function(d){ return translate(tx- 10, 77) } })

    var x = d3.scale.linear()
      .domain([0, totals])
      .range([0, width]);

    var x2 = d3.scale.linear()
      .domain([0, totals])
      .range([0, width]);


    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

    var xAxis2 = d3.svg.axis()
      .scale(x2)
      .tickSize(bars+20)

    group2.append("g")
      .attr("class", "x axis")
      .attr("transform", translate(0, height))
      .call(xAxis)
      .append("text")
      .attr("y", -20)
      .attr("x", width/2 )
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Time (ms)");

    // margin.top + (num_keys*barheight)
    group3.append("g")
      .attr("class", "x axis")
      .attr("transform", translate(0, height))
      .call(xAxis2)
      .attr("id", "chunk")

    //
    var interims = u_graph.items[0].start;
    
    var rect_groups = group1.selectAll("g").data(data);
    var rect = rect_groups.enter()
      .append("g")
      .attr({
        transform: function(d,i){
           var x = (d.start-interims) * scalar * 1000;
           var y = barheight*i;
           return translate(x, y) 
           } 
        })
    
    rect.append("rect")
      .attr({
        height: barheight, 
        width: function(d){ return d.duration * scalar * 1000 } })
      .style({fill: "#9ef"})

    // rect faux drop shadow
    rect.append('path')
      .attr({d: function(d,i){
        var xlen = (d.duration * scalar * 1000);
        var ybass = -barheight;
        return "M" + [0, 0, 0, -ybass, xlen, -ybass] }})
      .style({stroke: "#000000", fill: 'none', 'stroke-width': 0.2})

    rect.append("text")
      .text(function(d,i){ 
        var rounded = d3.round(d.duration * 1000, 4)
        return rounded })
      .attr({transform: translate(4,11) })
      .style({fill: "#434"})

    var node_names = name_group.selectAll("g").data(data);
    var node = node_names.enter().append("g")
      .attr({transform: function(d,i){
        var y = barheight*i;
        return translate(0, y+11); } })

    node.append("text")
    .text(function(d,i){return d.name })
    .attr({'text-anchor': 'end'})

}


for (var graph_idx in tributary.terrible.graphs){
  var u_graph = tributary.terrible.graphs[graph_idx];
  draw_graph(u_graph);
}



/* EOF  */

