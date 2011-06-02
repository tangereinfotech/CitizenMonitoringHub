/*
 * encoding: utf-8
 * Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var MapHandler = {
    map : null,
    map_canvas : null,
    center_lat : null,
    center_long : null,
    VILLG_ZOOM : 11,
    GRAMP_ZOOM : 10,
    BLOCK_ZOOM : 9,
    DISTT_ZOOM : 8,
    STATE_ZOOM : 7,
    circleOverlays : [],
    nameOverlays : [],
    countOverlays : [],
    init : function (map_canvas, center_lat, center_long, callback) {
        this.map_canvas = map_canvas;
        this.center_lat = center_lat;
        this.center_long = center_long;

        var myOptions  = {
            mapTypeId : google.maps.MapTypeId.ROADMAP,
            zoom : MapHandler.VILLG_ZOOM,
            center : new google.maps.LatLng (center_lat, center_long)
        };

        this.map = new google.maps.Map (document.getElementById (map_canvas), myOptions);

        google.maps.event.addListener (this.map, 'zoom_changed', 
                                       function () {
                                           var zoomLevel = MapHandler.map.getZoom ();
                                           switch (zoomLevel) {
                                           case VILLG_ZOOM: 
                                               MapHandler.showVillageData ();
                                               break;
                                           case GRAMP_ZOOM: 
                                               MapHandler.showGrampData ();
                                               break;
                                           case BLOCK_ZOOM: 
                                               MapHandler.showBlockData ();
                                               break;
                                           case DISTT_ZOOM: 
                                               MapHandler.showDisttData ();
                                               break;
                                           case STATE_ZOOM: 
                                               MapHandler.showStateData ();
                                               break;
                                           default: 
                                               if (zoomLevel < STATE_ZOOM) {
                                                   MapHandler.updateStateData ();
                                               } else {
                                                   MapHandler.updateVillageData ();
                                               }
                                           }
                                       });

        callback ();
    },
    isEmpty : function (object) {
        for (var attr in object) { return false; }
        return true;
    },
    showVillageData : function () {
        
    },
    updateVillageData : function () {

    },
    showGrampData : function () {
        
    },
    showBlockData : function () {
        
    },
    showDisttData : function () {
        
    },
    showStateData : function () {
        
    },
    updateStateData : function () {
        
    },
    update_with_stats : function (url, departments, zoom_level) {
        for (var i = 0; i < MapHandler.circleOverlays.length; i++ ) {
            MapHandler.circleOverlays [i].setMap (null);
            MapHandler.circleOverlays [i] = null;
        }
        MapHandler.circleOverlays = [];
        for (i = 0; i < MapHandler.nameOverlays.length; i++ ) {
            MapHandler.nameOverlays [i].setMap (null);
            MapHandler.nameOverlays [i] = null;
        }
        MapHandler.nameOverlays = [];
        for (i = 0; i < MapHandler.countOverlays.length; i++ ) {
            MapHandler.countOverlays [i].setMap (null);
            MapHandler.countOverlays [i] = null;
        }
        MapHandler.countOverlays = [];

        $.post (url,
               {'departments' : departments},
                function (data, status, jqXHR) {
                    data = $.parseJSON (data);

                    if (MapHandler.isEmpty (data) == false) {
                        var bounds = new google.maps.LatLngBounds ();

                        $.each (data, 
                                function (index, value) {
                                    var place_latlong = new google.maps.LatLng (value.latitude, value.longitude);
                                    
                                    bounds.extend (place_latlong);
                                    
                                    var numdigits = ("" + value.count + "").length;
                                    var radius = numdigits * 1400;
                                    var font_size = "" + (numdigits * 100 * 1.2) + "%";
                                    var count_offset = -numdigits * 12 * 0.9;
                                    var name_offset = numdigits * 12 * 0.5;

                                    var circle = new google.maps.Circle ({ map : MapHandler.map,
                                                                           center : place_latlong,
                                                                           radius: radius,
                                                                           strokeColor : "#f6d8ca",
                                                                           strokeWeight : 10,
                                                                           strokeOpacity: 0.60,
                                                                           fillColor : "#e5926a",
                                                                           fillOpacity : 0.50});
                                    
                                    var nlabel = new Label ({map : MapHandler.map}, name_offset);
                                    nlabel.set ('position', place_latlong);
                                    nlabel.set ('text', value.name);

                                    var clabel = new CountLabel ({map : MapHandler.map}, font_size, count_offset);
                                    clabel.set ('position', place_latlong);
                                    clabel.set ('text', "" + value.count);

                                    MapHandler.circleOverlays.push (circle);
                                    MapHandler.nameOverlays.push (nlabel);
                                    MapHandler.countOverlays.push (clabel);
                                });
                        
                        MapHandler.map.fitBounds (bounds);
                        MapHandler.map.setCenter (bounds.getCenter ());
                        MapHandler.map.setZoom (zoom_level);
                    }
                });
    }
};


