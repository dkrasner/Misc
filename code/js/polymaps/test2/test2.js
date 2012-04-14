var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 40.775, lon: -73.98})
    .zoomRange([11,13])
    .zoom(12)
    .add(po.interact());

map.add(po.image()
	.url(po.url("http://{S}tile.cloudmade.com"
		    + "/3110d8462f7446cfb0900015a5cb3daf" // http://cloudmade.com/register
		    + "/44094/256/{Z}/{X}/{Y}.png")
	     .hosts(["a.", "b.", "c.", ""])));

map.add(po.compass()
      .pan("none"))

map.add(po.geoJson()
	.features(locs)
	.on("load", load));

// this function is not necessary as is, but could be used in the future to do more computations

function load(e) {
    
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);

    for (var i = 0; i < e.features.length; i++) {
	var pt = e.features[i].data.geometry.coordinates
	point = g.appendChild(po.svg("circle"));
	point.setAttribute("cx", pt.x)
	point.setAttribute("cy", pt.y)
	point.setAttribute("r", 6)
	//var t = setTimeout("wait", 3000);
    }
}