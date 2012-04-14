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
    
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);
    console.log(e.features[0].data.geometry.geometries.length)
    for (var i = 0; i < e.features[0].data.geometry.geometries.length-1; i++) {
	var pt = e.features[0].data.geometry.geometries
	console.log(i);
	point = g.appendChild(po.svg("circle"));
	point.setAttribute("cx", pt[i].coordinates.x)
	point.setAttribute("cy", pt[i].coordinates.y)
	point.setAttribute("r", 6)
	point.setAttribute("fill", "green")
	//var t = setTimeout("wait()", 1000);
    }
}


