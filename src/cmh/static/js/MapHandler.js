
var MapHandler = {
    init : function (map_canvas) {
        var places = {'Sehore' : {lat  : 23.20119, lng : 77.081795},
                      'Pachama' : {lat  : 23.215791, lng : 77.125053}};
        var latlng = new google.maps.LatLng(23.20119, 77.081795);
        var myOptions = {
            zoom: 13,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.HYBRID
        };
        var map = new google.maps.Map(document.getElementById(map_canvas), myOptions);
        
        for (var place in places) {
            var place_latlong = new google.maps.LatLng (places [place].lat, places [place].lng);
            var circleOpts = {
                strokeColor: "#FF0000",
                strokeOpacity: 0.7,
                strokeWeight: 2,
                fillColor: "#FF0000",
                fillOpacity: 0.35,
                map: map,
                center: place_latlong,
                radius: 400
            };
            var placeCircle = new google.maps.Circle (circleOpts);
            google.maps.event.addListener (placeCircle, 'click', this.placeAlert (place));
        }
    },
    placeAlert : function (place) {
        return ((function x (){
                     alert (place);
                 }));
    }

}
