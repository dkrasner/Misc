d3.csv("us-income-inequality.csv", function(data1) { 
     

    /* Read CSV file: first row =>  year,top1,top5  */
    var maxval = 0,
        sampsize = 0;
    var label_array = new Array(),
        val_array1 = new Array();

    sampsize = data1.length;
    

    for (var i=0; i < sampsize; i++) {
       label_array[i] = parseInt(data1[i].year);
       val_array1[i] = { x: label_array[i], y: parseFloat(data1[i].p99), z: parseFloat(data1[i].p95) };
       maxval = Math.max(maxval, parseFloat(data1[i].p99), parseFloat(data1[i].p95) );
     }
 
     maxval = (1 + Math.floor(maxval / 10)) * 10;   
     console.log(maxval)

   var  w = 815,
        h = 500,
        p = 30,
        x = d3.scale.linear().domain([ label_array[0], label_array[sampsize-1] ]).range([0, w]),
        y = d3.scale.linear().domain([0, maxval]).range([h, 0]);

   var vis = d3.select("#paired-line-chart")
       .data([val_array1])
     .append("svg:svg")
       .attr("width", w + p * 2)
       .attr("height", h + p * 2)
     .append("svg:g")
       .attr("transform", "translate(" + p + "," + p + ")");


   var rules = vis.selectAll("g.rule")
      .data(x.ticks(15))
     .enter().append("svg:g")
       .attr("class", "rule");

   // Draw grid lines
   rules.append("svg:line")
    .attr("x1", x)
    .attr("x2", x)
    .attr("y1", 0)
    .attr("y2", h - 1);

   rules.append("svg:line")
    .attr("class", function(d) { return d ? null : "axis"; })
    .data(y.ticks(10))
    .attr("y1", y)
    .attr("y2", y)
    .attr("x1", 0)
    .attr("x2", w - 10);

   // Place axis tick labels
   rules.append("svg:text")
    .attr("x", x)
    .attr("y", h + 15)
    .attr("dy", ".71em")
    .attr("text-anchor", "middle")
    .text(x.tickFormat(10))
    .text(String);

   rules.append("svg:text")
    .data(y.ticks(12))
    .attr("y", y)
    .attr("x", -10)
    .attr("dy", ".35em")
    .attr("text-anchor", "end")
    .text(y.tickFormat(5));


   // Series I
   vis.append("svg:path")
       .attr("class", "line")
       .attr("fill", "none")
       .attr("stroke", "maroon")
       .attr("stroke-width", 2)
       .attr("d", d3.svg.line()
         .x(function(d) { return x(d.x); })
         .y(function(d) { return y(d.y); }));

   vis.selectAll("circle.line")
       .data(val_array1)
     .enter().append("svg:circle")
       .attr("class", "line")
       .attr("fill", "maroon" )
       .attr("cx", function(d) { return x(d.x); })
       .attr("cy", function(d) { return y(d.y); })
       .attr("r", 1);

   // Series II
   vis.append("svg:path")
       .attr("class", "line")
       .attr("fill", "none")
       .attr("stroke", "darkblue")
       .attr("stroke-width", 2)
       .attr("d", d3.svg.line()
         .x(function(d) { return x(d.x); })
         .y(function(d) { return y(d.z); }));

   vis.select("circle.line")
       .data(val_array1)
     .enter().append("svg:circle")
       .attr("class", "line")
       .attr("fill", "darkblue" )
       .attr("cx", function(d) { return x(d.x); })
       .attr("cy", function(d) { return y(d.z); })
       .attr("r", 1);

   // -----------------------------
   // Add Title then Legend
   // -----------------------------
   vis.append("svg:text")
       .attr("x", w/4)
       .attr("y", 20)
       .text("% share of income (excluding capital gains): U.S. 1920-2008");

   vis.append("svg:rect")
       .attr("x", w/2 - 20)
       .attr("y", 50)
       .attr("stroke", "darkblue")
       .attr("height", 2)
       .attr("width", 40);

   vis.append("svg:text")
       .attr("x", 30 + w/2)
       .attr("y", 55)
       .text("Top 5% households");

   vis.append("svg:rect")
       .attr("x", w/2 - 20)
       .attr("y", 80)
       .attr("stroke", "maroon")
       .attr("height", 2)
       .attr("width", 40);

   vis.append("svg:text")
       .attr("x", 30 + w/2)
       .attr("y", 85)
       .text("Top 1% households");


}); 

