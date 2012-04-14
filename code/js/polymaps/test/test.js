var po = org.polymaps;

// Compute noniles.
var quantile = pv.Scale.quantile()
    .quantiles(9)
    .domain(pv.values(states))
    .range(0, 8);

// Date format.
var format = pv.Format.date("%B %e, %Y");

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 40, lon: -95})
    .zoomRange([3, 7])
    .zoom(4)
    .add(po.interact());

map.add(po.image()
	.url(po.url("http://{S}tile.cloudmade.com"
		    + "/8c6e1a7ebbf441d28ad88878842b1202" // http://cloudmade.com/register
		    + "/44094/256/{Z}/{X}/{Y}.png")
	     .hosts(["a.", "b.", "c.", ""])));

map.add(po.geoJson()
	.url("coordinates5.json")
	.on("load", load))

    map.add(po.compass()
	    .pan("none"));

map.container().setAttribute("class", "Blues");

function load(e) {
    for (var i = 0; i < e.features.length; i++) {
	var feature = e.features[i], d = states[feature.data.id.substring(6)];
	if (d == undefined) {
	    feature.element.setAttribute("display", "none");
	} else {
	    feature.element.setAttribute("class", "q" + quantile(d) + "-" + 9);
	    feature.element.appendChild(po.svg("title").appendChild(
								    document.createTextNode(feature.data.properties.name + ": "
											    + format(d).replace(/ [ ]+/, " ")))
					.parentNode);
	}
    }
}
