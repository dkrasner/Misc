var po = org.polymaps;


// Compute noniles.
var quantile = pv.Scale.quantile()
    .quantiles(9)
    .domain(pv.values(pop))
    .range(0,8);

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 27, lon: -30})
    .zoom(3)
    .zoomRange([2, 16])
    .add(po.interact());


map.add(po.image()
    .url("http://s3.amazonaws.com/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg"));


map.add(po.compass()
    .pan("none"));

map.add(po.geoJson()
    .url("world.json")
    .tile(false)
    .zoom(3)
    .on("load", world_load));



map.add(po.geoJson()
      .url('states.json')
      .on("load", state_load))


map.add(po.geoJson()
	.url("timegeo.json")
	.on("load", point_load));





map.container().setAttribute("class", "Blues");


//////LOAD WORLD BORDERS

function world_load(e) {
 // console.log(e.features)

  for (var i = 0; i < e.features.length; i++) {
    var feature = e.features[i],  d = feature.data.properties.q;
    console.log(quantile(d))
    feature.element
        .setAttribute("class", "q" + quantile(d) + "-" + 9)
    feature.element.appendChild(po.svg("title").appendChild(
          document.createTextNode(feature.data.properties.name + ': ' + d))
          .parentNode);
     // .add("svg:title")
       // .text(n + (isNaN(v) ? "" : ":  " + percent(v)));
  }
}



/////LOAD STATE BORDERS

function state_load(e) {

 var state_counts = {};
 
  for (var i = 0; i < e.features.length; i++) {
    var feature = e.features[i], d = feature.data.properties.q;
    console.log(quantile(d))
    if (d == undefined) {
      feature.element.setAttribute("display", "none");
    } else {
      feature.element.setAttribute("class", "q" + quantile(d)  + "-" + 9);
    // console.log(quantile(d))
      feature.element.appendChild(po.svg("title").appendChild(
          document.createTextNode(feature.data.properties.name + ': ' + d))
          .parentNode);
    }
  }
}





function point_load(e) {
   
    var points = [];
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);
    var L = e.features[0].data.geometry.geometries.length	
    //console.log(e.features[0].data.geometry.geometries.length)
    for (var i = 0; i < e.features[0].data.geometry.geometries.length; i++) {		
		var pt = e.features[0].data.geometry.geometries
		var url = pt[i].url
		x = parseInt(pt[i].coordinates.x);
		y = parseInt(pt[i].coordinates.y);
		point = e.tile.element.appendChild(po.svg("circle"));
		points.push({x:x,y:y, point:point, url:url});
		//plot(i,e)
	
    }

	//setTimeout("alert('Fuck Javascript!!!')", 10000);
	var t
	//var i = 0
	//console.log(i)
	function pl(i, t){
		//var i = 0
	//	console.log(i)	
		t = setInterval(function(){	
			//console.log(i)		
			plot(points[i].x,points[i].y, points[i].point, points[i].url);
			if (i == e.features[0].data.geometry.geometries.length-1) {
			clearInterval(t)
			}
		}, t)
	
	}
	for (k=1; k < L; k++ ){
		//console.log(pt[k].ts)
		pl(k, pt[k].ts*10)
	}
}


function plot(x,y, point, url) {

		point.setAttribute("cx", x)
		point.setAttribute("cy", y)
		point.setAttribute("r", 4) /// use this for no animation
                point.setAttribute("fill", "purple")
                point.appendChild(po.svg("title").appendChild(
        document.createTextNode(url))
         .parentNode);
		}



