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
    data : null,
    url : null,
    departments : null,
    center_lat : null,
    center_long : null,
    VILLG_ZOOM : 12,
    GRAMP_ZOOM : 11,
    BLOCK_ZOOM : 10,
    DISTT_ZOOM : 9,
    STATE_ZOOM : 8,
    circleOverlays : [],
    nameOverlays : [],
    countOverlays : [],
    data_level : null,
    stdate : null,
    endate : null,
    bounds : null,
    isEmpty : function (object) {
        for (var attr in object) { return false; }
        return true;
    },
    init : function (map_canvas, center_lat, center_long, donecallback) {
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
                                           case MapHandler.VILLG_ZOOM:
                                               MapHandler.showVillageData ();
                                               break;
                                           case MapHandler.GRAMP_ZOOM:
                                               MapHandler.showGrampData ();
                                               break;
                                           case MapHandler.BLOCK_ZOOM:
                                               MapHandler.showBlockData ();
                                               break;
                                           case MapHandler.DISTT_ZOOM:
                                               MapHandler.showDisttData ();
                                               break;
                                           case MapHandler.STATE_ZOOM:
                                               MapHandler.showStateData ();
                                               break;
                                           default:
                                               if (zoomLevel < MapHandler.STATE_ZOOM) {
                                                   MapHandler.updateStateData ();
                                               } else {
                                                   MapHandler.updateVillageData ();
                                               }
                                           }
                                       });

        google.maps.event.addListener (this.map, 'center_changed',
                                       function () {
                                           MapHandler.renderWithinBounds ();
                                       });

	google.maps.event.addListenerOnce (this.map, "bounds_changed", 
					   function () {
					       donecallback ();
					   });
    },
    showVillageData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.VILLG_ZOOM,
                                      'villg',
                                      MapHandler.stdate,
                                      MapHandler.endate
                                     );
    },
    updateVillageData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.VILLG_ZOOM,
                                      'villg',
                                      MapHandler.stdate,
                                      MapHandler.endate
                                     );
    },
    showGrampData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.GRAMP_ZOOM,
                                      'gramp',
                                      MapHandler.stdate,
                                      MapHandler.endate);
    },
    showBlockData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.BLOCK_ZOOM,
                                      'block',
                                      MapHandler.stdate,
                                      MapHandler.endate);
    },
    showDisttData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.DISTT_ZOOM,
                                      'distt',
                                      MapHandler.stdate,
                                      MapHandler.endate);
    },
    showStateData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.STATE_ZOOM,
                                      'state',
                                      MapHandler.stdate,
                                      MapHandler.endate);
    },
    updateStateData : function () {
        MapHandler.update_with_stats (this.url,
                                      this.departments,
                                      MapHandler.STATE_ZOOM,
                                      'state',
                                      MapHandler.stdate,
                                      MapHandler.endate);
    },
    getCurrentDataLevel : function () {
        return this.data_level;
    },
    renderWithinBounds : function () {
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

        var data = MapHandler.data;

        if (!(MapHandler.isEmpty (data))) {
            MapHandler.bounds = new google.maps.LatLngBounds ();
            var mapBounds = MapHandler.map.getBounds ();

            $.each (data,
                    function (index, value) {
                        var place_latlong = new google.maps.LatLng (value.latitude, value.longitude);
                        if (mapBounds.contains (place_latlong)) {
                            MapHandler.bounds.extend (place_latlong);

                            var numdigits = ("" + value.count + "").length;
                            var villzoom = MapHandler.VILLG_ZOOM;
                            var currzoom = MapHandler.map.getZoom ();
                            var zoomval = villzoom - currzoom;
                            var radius = (numdigits * 400 * Math.pow(2,zoomval));
                            var font_size = "90%";
                            var count_offset = -12 * 0.9;
                            var name_offset = 12 * 0.5;

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
                        }
                    });
        }
    },
    update_with_stats : function (url, departments, zoom_level, data_level, st_date, en_date) {
        this.url = url;
        this.departments = departments;
        this.data_level = data_level;
        this.stdate = st_date;
        this.endate = en_date;

        $.post (url,
               {
                   'departments' : departments,
                   'datalevel'   : data_level,
                   'stdate' : st_date,
                   'endate' : en_date
               },
                function (data, status, jqXHR) {
                    data = $.parseJSON (data);
                    MapHandler.data = data;
                    MapHandler.renderWithinBounds ();
                });
    }
};


