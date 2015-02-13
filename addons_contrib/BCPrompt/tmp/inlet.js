var data = [];
var rawdata = [];
var localfile = 'sverchok_times.json'

// https://github.com/mrdoob/three.js/wiki/How-to-run-things-locally

// d3.json(localfile, function(data) {
//     console.log(data.items);
//     rawdata = data.items;
//     draw_content(rawdata)
// });

function getArray(obj) {
  for(var prop in obj) {
    if(obj.hasOwnProperty(prop)){
      data.push(obj[prop]);
    }
  }
}

function translate(a, b) { 
  return "translate(" + [a, b] + ")" 
}

function draw_content(rawdata){

  var display = d3.select('#display')
  display.append('svg')


  d3.select("body").style("background-color", d3.rgb(240,240,240))

  var svg = d3.select("svg")
    .attr({height: 494, width: 964})
    .style({border: "1px solid #d6d6d6"});

  var barheight = 15;
  var tx = 130;

  //
  var group2 = svg.append("g")
    .attr({transform: function(d){ return translate(tx, -32) } })

  var group3 = svg.append("g")
    .attr({transform: function(d){ return translate(tx, -11) } })

  var group1 = svg.append("g")
    .attr({transform: function(d){ return translate(tx, 77) } })

  var name_group = svg.append("g")
    .attr({transform: function(d){ return translate(tx- 10, 77) } })

  // or some other counting scheme
  getArray(rawdata);

  var num_keys = data.length;
  var totals = 0;
  for (var i=0; i<num_keys; i+=1){
    totals += (data[i].duration * 1000);
  }

  // 
  var margin = {top: 16, right: 6, bottom: 30, left: 103},
     width = 900 - margin.left - margin.right,
     height = 119 - margin.top - margin.bottom;

  var scalar = width/totals;

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
    .tickSize(350)

  group2.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + [0, height] + ")")
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
    .attr("transform", "translate(" + [0, height] + ")")
    .call(xAxis2)
    .attr("id", "chunk")

  //
  var interims = data[0].start
  var rect_groups = group1.selectAll("g").data(data);
  var rect = rect_groups.enter()
    .append("g")
    .attr({transform: function(d,i){
      var x = (d.start - interims) * scalar * 1000;
      var y = barheight*i;
      return "translate(" + [x, y] + ")"; } })

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
  .text(function(d,i){
     return d.name 
  })
  .attr({'text-anchor': 'end'})


}


$(document).ready(function(e) {
     rawdata = jsonObject.items;
     draw_content(rawdata);
});









/* EOF  */
