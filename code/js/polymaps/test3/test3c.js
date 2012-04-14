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

//map.add(po.geoJson()
//    .url(crimespotting("http://oakland.crimespotting.org"
//        + "/crime-data"
//        + "?count=1000"
//        + "&format=json"
//        + "&bbox={B}"
//        + "&dstart=2010-04-01"
//        + "&dend=2010-05-01"))
//    .on("load", load)
//    .clip(false)
//    .zoom(14));



map.add(po.compass()
    .pan("none"));

map.add(po.geoJson()
	.features(locs)
	.on("load", load));

function load(e) {
    
    var tile = e.tile, g = tile.element;
    while (g.lastChild) g.removeChild(g.lastChild);

    for (var i = 0; i < e.features.length; i++) {
	var pt = e.features[i].data.geometry.coordinates
	console.log(pt)
	point = g.appendChild(po.svg("circle"));
	point.setAttribute("cx", pt.x)
	point.setAttribute("cy", pt.y)
	point.setAttribute("r", 6)
	//var t = setTimeout("wait", 3000);
    }
}


