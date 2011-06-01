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
    VILLG_ZOOM : 11,
    GRAMP_ZOOM : 10,
    BLOCK_ZOOM : 9,
    DISTT_ZOOM : 8,
    STATE_ZOOM : 7,
    overlays : [],
    init : function (map_canvas, center_lat, center_long, zoom_level, callback) {
        this.map_canvas = map_canvas;
        var latlng = new google.maps.LatLng (center_lat, center_long);
        
        var myOptions  = {
            zoom : zoom_level,
            center : latlng,
            mapTypeId : google.maps.MapTypeId.ROADMAP
        };

        this.map = new google.maps.Map (document.getElementById (map_canvas), myOptions);

        // google.maps.event.addListener (this.map, 'zoom_changed', 
        //                                function () {
        //                                    var zoomLevel = MapHandler.map.getZoom ();
        //                                    switch (zoomLevel) {
        //                                    case VILLG_ZOOM: 
        //                                        MapHandler.showVillageData ();
        //                                        break;
        //                                    case GRAMP_ZOOM: 
        //                                        MapHandler.showGrampData ();
        //                                        break;
        //                                    case BLOCK_ZOOM: 
        //                                        MapHandler.showBlockData ();
        //                                        break;
        //                                    case DISTT_ZOOM: 
        //                                        MapHandler.showDisttData ();
        //                                        break;
        //                                    case STATE_ZOOM: 
        //                                        MapHandler.showStateData ();
        //                                        break;
        //                                    default: 
        //                                        if (zoomLevel < STATE_ZOOM) {
        //                                            MapHandler.showStateData ();
        //                                        } else {
        //                                            MapHandler.showVillageData ();
        //                                        }
        //                                    }
        //                                });

        callback ();
    },
    showVillageData : function () {
        
    },
    showGrampData : function () {
        
    },
    showBlockData : function () {
        
    },
    showDisttData : function () {
        
    },
    showStateData : function () {
        
    },
    update_with_stats : function (url, departments) {
        $.post (url,
               {'departments' : departments},
                function (data, status, jqXHR) {
                    var overlays = MapHandler.overlays;
                    $.each (overlays, function (index, overlay) {
                                overlay.setMap (null);
                            });
                    data = $.parseJSON (data);

                    var map = MapHandler.map;
                    var bounds = new google.maps.LatLngBounds ();

                    $.each (data, 
                            function (index, value) {
                                var place_latlong = new google.maps.LatLng (value.latitude, value.longitude);
                                
                                bounds = bounds.extend (place_latlong);
                                
                                var radius = ("" + value.count + "").length;
                                var font_size = "" + (radius * 100 * 1.4) + "%";
                                var count_offset = -radius * 14 * 0.8;
                                var name_offset = radius * 14 * 0.5;

                                var circle = new CircleOverlay (map,
                                                                place_latlong,
                                                                radius,
                                                                "#f6d8ca",
                                                                16,
                                                                0.20,
                                                                "#e5926a",
                                                                0.40,
                                                                2000);
                                
                                var nlabel = new Label ({map : map}, name_offset);
                                nlabel.set ('position', place_latlong);
                                nlabel.set ('text', value.name);

                                var clabel = new CountLabel ({map : map}, font_size, count_offset);
                                clabel.set ('position', place_latlong);
                                clabel.set ('text', "" + value.count);

                                MapHandler.overlays.push (circle);
                                MapHandler.overlays.push (nlabel);
                                MapHandler.overlays.push (clabel);
                            });
                    map.setCenter (bounds.getCenter ());
                    map.setZoom (MapHandler.VILLG_ZOOM);
                });
    }
};


