console.time("graph")
//generate some random colors function
function get_rand_color()
{
    var color = Math.floor(Math.random() * Math.pow(256, 3)).toString(16);
    while(color.length < 6) {
        color = "0" + color;
    }
    return "#" + color;
}


//chord matrix
var chord_mat = [];
var list_sizes = []

// read in data

var keys = []

d3.csv("chord_mat.txt", function(data) {
  var listnames = {},
      array = [],
      n = 0;


  //get the column names
  for(var key in data[0]){
    keys.push(key)  	
  } 

	
  //populate the matrix
  n = data.length -10 
  for (var i = 0; i < n; i++) {
    chord_mat[i] = [];
    for (var j = 0; j < n; j++) {
 	if(i==j){
	  chord_mat[i][j] = 0
	  list_sizes[i] = eval(data[i][keys[j]])
	} else {
	  chord_mat[i][j] = eval(data[i][keys[j]]);
	}
    }
  }
  
  




// From http://mkweb.bcgsc.ca/circos/guide/tables/
  var chord = d3.layout.chord()
    .padding(.05)
    .sortSubgroups(d3.descending)
    .matrix(chord_mat);

//console.log(chord_mat)

  var colors = []
  for (i = 0; i < n; i++){
    colors.push(get_rand_color())
  }



  var w = 600,
      h = 600,
      r0 = Math.min(w, h) * .41,
      r1 = r0 * 1.1;

  var fill = d3.scale.ordinal()
      .domain(d3.range(23))
      .range(colors);

  var svg = d3.select("#chart")
    .append("svg")
      .attr("width", w)
      .attr("height", h)
    .append("g")
      .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

/// hack for click fade change
  var mode = 0
  function fade_mode(){
    if(mode%2 == 0){
      mode+=1 
     // return fade(.1);
    } 
    if(mode%2 == 1){
      //return fade(1);
    }
    return mode	;
  }
  
  console.log(fade_mode())
  console.log(fade_mode())

  svg.append("g")
    .selectAll("path")
      .data(chord.groups)
    .enter().append("path")
      .style("fill", function(d) { return fill(d.index);  })
      .style("stroke", function(d) { return fill(d.index); })
      .attr("d", d3.svg.arc().innerRadius(r0).outerRadius(r1))
      .on("click", fade(.1))
      .on("mouseover", fade(1))
      //.on("click.off", fade_mode())
      .append("svg:title").text(function(d) { return keys[d.index] + " #users: " + list_sizes[d.index]});
    
  var ticks = svg.append("g")
    .selectAll("g")
     .data(chord.groups)
      .enter().append("g")
      .selectAll("g")
      .data(groupTicks)
    .enter().append("g")
      .attr("transform", function(d) {
	return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
  	    + "translate(" + r1 + ",0)";
      });

//ticks.append("line")
//    .attr("x1", 1)
//    .attr("y1", 0)
//    .attr("x2", 5)
//    .attr("y2", 0)
//    .style("stroke", "#000");


//ticks.append("text")
//    .attr("x", 8)
//    .attr("dy", ".35em")
//    .attr("text-anchor", function(d) {
//      return d.angle > Math.PI ? "end" : null;
//    })
//    .attr("transform", function(d) {
//      return d.angle > Math.PI ? "rotate(180)translate(-16)" : null;
//    })
//    .text(function(d) { return d.label; });

svg.append("g")
    .attr("class", "chord")
  .selectAll("path")
    .data(chord.chords)
  .enter().append("path")
    .style("fill", function(d) { return fill(d.target.index); })
    .attr("d", d3.svg.chord().radius(r0))
    .style("opacity", 1)
   // .on("mouseover", fade(.2))
   // .on("mouseout", fade(1))
    .append("svg:title").text(function(d) {return chord_mat[d.target.index][d.source.index]});

/** Returns an array of tick angles and labels, given a group. */
function groupTicks(d) {
  var k = (d.endAngle - d.startAngle) / d.value;
  return d3.range(0, d.value, 1000).map(function(v, i) {
    return {
      angle: v * k + d.startAngle,
      label: i % 5 ? null : v / 1000 + "k"
    };
  });
}

/** Returns an event handler for fading a given chord group. */
function fade(opacity) {
  return function(g, i) {
    svg.selectAll("g.chord path")
        .filter(function(d) {
          return d.source.index != i && d.target.index != i;
        })
      .transition()
        .style("opacity", opacity);
  };
}

console.log("Time: " + console.timeEnd("graph"));
});



