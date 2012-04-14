var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .center({lat: 36, lon: -90})
    .zoom(4.5)
    .zoomRange([2, 16])
    .add(po.interact());

map.add(po.image()
    .url(po.url("http://{S}tile.cloudmade.com"
    + "/8c6e1a7ebbf441d28ad88878842b1202" // http://cloudmade.com/register
    + "/44094/256/{Z}/{X}/{Y}.png")
    .hosts(["a.", "b.", "c.", ""])));



map.add(po.compass()
    .pan("none"));


map.add(po.geoJson()
      .url('states.json')
      .on("load", state_load))

map.add(po.geoJson()
	.url("timegeo.json")
	.on("load", load));





map.container().setAttribute("class", "Blues");






/////LOAD STATE BORDERS

function state_load(e) {
  //console.log(states)
  for (var i = 0; i < e.features.length; i++) {
    var feature = e.features[i], d = feature.data.properties.q;
    console.log(d)
    if (d == undefined) {
      feature.element.setAttribute("display", "none");
    } else {
      feature.element.setAttribute("class", "q" + d  + "-" + 9);
    // console.log(quantile(d))
      feature.element.appendChild(po.svg("title").appendChild(
          document.createTextNode(feature.data.properties.name))
          .parentNode);
    }
  }
}








function load(e) {
  var cluster = e.tile.cluster || (e.tile.cluster = kmeans()
      .iterations(20)
      .size(300));
  console.log(e.features[0].data.geometry.geometries.length)
  for (var i = 0; i < e.features[0].data.geometry.geometries.length; i++) {
    cluster.add(e.features[0].data.geometry.geometries[i].coordinates);
   // console.log(e.features[0].data.geometry.geometries[i].coordinates)
  }

  var tile = e.tile, g = tile.element;
  while (g.lastChild) g.removeChild(g.lastChild);

  var means = cluster.means();
  console.log(means.length)
  means.sort(function(a, b) { return b.size - a.size; });
  for (var i = 0; i < means.length; i++) {
    //console.log(means.length)
    var mean = means[i], point = g.appendChild(po.svg("circle"));
    //console.log(mean.y)	
    point.setAttribute("cx", mean.x);
    point.setAttribute("cy", mean.y);
    point.setAttribute("r", 100*Math.pow(2, tile.zoom - 11) * Math.sqrt(mean.size));
  }
}
