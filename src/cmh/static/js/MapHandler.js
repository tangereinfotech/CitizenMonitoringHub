var MapHandler = {
    map : null,
    init : function (map_canvas, center_lat, center_long, zoom_level) {
        var latlng = new google.maps.LatLng(center_lat, center_long);
        var myOptions = {
            zoom: zoom_level,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.HYBRID
        };
        this.map = new google.maps.Map(document.getElementById(map_canvas), myOptions);
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
                       $.each (data, function (index, value) {
                                   var place_latlong = new google.maps.LatLng (value.latitude,
                                                                               value.longitude);
                                   
                                   var circleOpts = {
                                       strokeColor: "#FF0000",
                                       strokeOpacity: 0.7,
                                       strokeWeight: 2,
                                       fillColor: "#FF0000",
                                       fillOpacity: 0.35,
                                       map: MapHandler.map,
                                       center: place_latlong,
                                       radius: value.count * 25
                                   };
                                   var placeCircle = new google.maps.Circle (circleOpts);
                               });
                       // google.maps.event.addListener (placeCircle, 
                       //                                'click',
                       //                                MapHandler.placeAlert (place));
                   });
    }
};


