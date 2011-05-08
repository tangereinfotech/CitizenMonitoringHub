var MapHandler = {
    map : null,
    init : function (map_canvas, center_lat, center_long, zoom_level, callback) {
        var latlng = new google.maps.LatLng(center_lat, center_long);
        var myOptions = {
            zoom: zoom_level,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.HYBRID
        };
        this.map = new google.maps.Map(document.getElementById(map_canvas), myOptions);
        callback ();
    },
    placeAlert : function (place) {
        return (function x (){
                     alert (place);
                 });
    },
    update_with_stats : function (url, category) {
        category || (category = 'all');
        $.getJSON (url + category + "/",
                   null,
                   function (data) {
                       var bounds = new google.maps.LatLngBounds ();
                       $.each (data, function (index, value) {
                                   var place_latlong = new google.maps.LatLng (value.latitude,
                                                                               value.longitude);
                                   bounds.extend (place_latlong);
                                   
                                   var circleOpts = {
                                       strokeColor: "#FF0000",
                                       strokeOpacity: 0.7,
                                       strokeWeight: 2,
                                       fillColor: "#FF0000",
                                       fillOpacity: 0.35,
                                       map: MapHandler.map,
                                       center: place_latlong,
                                       radius: value.count * 200
                                   };
                                   var placeCircle = new google.maps.Circle (circleOpts);
                               });
                       MapHandler.map.setCenter (bounds.getCenter ());
                       MapHandler.map.fitBounds (bounds);
                       // google.maps.event.addListener (placeCircle, 
                       //                                'click',
                       //                                MapHandler.placeAlert (place));
                   });
    }
};


