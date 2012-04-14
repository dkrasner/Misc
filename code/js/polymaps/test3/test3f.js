var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 40, lon: -95})
    .zoom(4)
    .zoomRange([0, 16])
    .add(po.interact());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/8c6e1a7ebbf441d28ad88878842b1202" // http://cloudmade.com/register
    + "/44094/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));



map.add(po.compass()
    .pan("none"));

map.add(po.geoJson()
	.url("coordinates5.json")
	.on("load", load));



function load(e) {
    var points = [];
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);
    //console.log(e.features[0].data.geometry.geometries.length)
    for (var i = 0; i < e.features[0].data.geometry.geometries.length-1; i++) {
  		var pt = e.features[0].data.geometry.geometries
		x = parseInt(pt[i].coordinates.x);
		y = parseInt(pt[i].coordinates.y);
		point = e.tile.element.appendChild(po.svg("circle"));
		points.push({x:x,y:y, point:point});
		//plot(i,e)
	
    }
	var i = 0
	setInterval(function(){
		//for(var i=0; i< points.length; i++){
			
		plot(points[i].x,points[i].y, points[i].point);
		i++;		
		
	}, 500)

    
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
