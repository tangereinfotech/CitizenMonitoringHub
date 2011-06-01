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

/* Adapted from https://github.com/mattwilliamson/Google-Maps-Circle-Overlay */

// Constructor
var CircleOverlay = function(map, latLng, radius, 
                             strokeColor, strokeWidth, strokeOpacity,
                             fillColor, fillOpacity, 
                             numPoints) {
	this.map = map;
	this.setMap(map);
	this.latLng = latLng;
	this.radius = radius;
	this.strokeColor = strokeColor;
	this.strokeWidth = strokeWidth;
	this.strokeOpacity = strokeOpacity;
	this.fillColor = fillColor;
	this.fillOpacity = fillOpacity;

	// Set resolution of polygon
	if (typeof(numPoints) == 'undefined') {
		this.numPoints = 45;
	} else {
		this.numPoints = numPoints;
	}
}

// Inherit from GOverlay
CircleOverlay.prototype = new google.maps.OverlayView();

// Reset overlay
CircleOverlay.prototype.clear = function() {
	if(this.polygon != null && this.map != null) {
		this.polygon.setMap(null);
	}
}

// Calculate all the points of the circle and draw them
CircleOverlay.prototype.draw = function(force) {
	var d2r = Math.PI / 180;
	circleLatLngs = new Array();

	// Convert statute miles into degrees latitude
	var circleLat = this.radius * 0.014483;
	var circleLng = circleLat / Math.cos(this.latLng.lat() * d2r);

	// Create polygon points (extra point to close polygon)
	for (var i = 0; i < this.numPoints + 1; i++) { 
		// Convert degrees to radians
		var theta = Math.PI * (i / (this.numPoints / 2)); 
		var vertexLat = this.latLng.lat() + (circleLat * Math.sin(theta)); 
		var vertexLng = this.latLng.lng() + (circleLng * Math.cos(theta));
		var vertextLatLng = new google.maps.LatLng(vertexLat, vertexLng);
		circleLatLngs.push(vertextLatLng); 
	}

	this.clear();
	this.polygon = new google.maps.Polygon({
		paths: circleLatLngs, 
		strokeColor: this.strokeColor, 
		strokeWeight: this.strokeWidth, 
		strokeOpacity: this.strokeOpacity, 
		fillColor: this.fillColor, 
		fillOpacity: this.fillOpacity
	});
	this.polygon.setMap(this.map);
}

// Remove circle method
CircleOverlay.prototype.remove = function() {
	this.clear();
}

// Can use this method if the library at is included at http://appdelegateinc.com/blog/2010/05/16/point-in-polygon-checking/
CircleOverlay.prototype.containsLatLng = function(latLng) {
	if(this.polygon.containsLatLng) {
		return this.polygon.containsLatLng(latLng);
	}
}

// Set radius of circle
CircleOverlay.prototype.setRadius = function(radius) {
	this.radius = radius;
}

// Set center of circle
CircleOverlay.prototype.setLatLng = function(latLng) {
	this.latLng = latLng;
}