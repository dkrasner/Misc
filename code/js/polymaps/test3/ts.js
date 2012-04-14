var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 36, lon: -90})
    .zoom(4.5)
    .zoomRange([2, 10])
    .add(po.interact());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/8c6e1a7ebbf441d28ad88878842b1202" // http://cloudmade.com/register
    + "/44094/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));



map.add(po.compass()
    .pan("none"));

map.add(po.geoJson()
	.url("timegeo.json")
	.on("load", load));



function load(e) {
    var points = [];
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);
    var L = e.features[0].data.geometry.geometries.length	
    console.log(e.features[0].data.geometry.geometries.length)
    for (var i = 0; i < e.features[0].data.geometry.geometries.length; i++) {
  		var pt = e.features[0].data.geometry.geometries
		//console.log(pt[i].ts)
		x = parseInt(pt[i].coordinates.x);
		y = parseInt(pt[i].coordinates.y);
		point = e.tile.element.appendChild(po.svg("circle"));
		points.push({x:x,y:y, point:point});
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
			plot(points[i].x,points[i].y, points[i].point);
			if (i == e.features[0].data.geometry.geometries.length-1) {
			clearInterval(t)
			}
		}, t)
	
	}
	for (k=0; k < L; k++ ){
		//console.log(pt[k].ts)
		pl(k, pt[k].ts*10)
	}
}


function plot(x,y, point) {
		//var pt = p.features[0].data.geometry.geometries
		//console.log(pt[i]);

		//point = p.tile.element.appendChild(po.svg("circle"));
		point.setAttribute("cx", x)
		point.setAttribute("cy", y)
		point.setAttribute("r", 6)
		//setTimeout("plot()", 500)

	}

//setTimeout("alert('fuck!')", 2000);
