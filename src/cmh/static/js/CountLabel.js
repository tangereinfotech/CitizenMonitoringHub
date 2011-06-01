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

/* 
 * Adapted from 
 * http://blog.mridey.com/2009/09/label-overlay-example-for-google-maps.html
 */

// Define the overlay, derived from google.maps.OverlayView
function CountLabel(opt_options, font_size, top_offset) {
    // Initialization
    this.setValues(opt_options);

    // CountLabel specific
    var span = this.span_ = document.createElement('span');
    span.style.cssText = 'white-space: nowrap; color: #6a2d0b; font-size:' + font_size;

    var div = document.createElement('div');
    div.appendChild(span);
    div.style.cssText = 'padding: 2px; position: relative; top: ' + top_offset + 'px; left: -50%; text-align: center; ';

    var divTop = this.div_ = document.createElement ('div');
    divTop.appendChild (div);
    divTop.style.cssText = "display:none;position:absolute;";
};

CountLabel.prototype = new google.maps.OverlayView;

// Implement onAdd
CountLabel.prototype.onAdd = function() {
    var pane = this.getPanes().overlayLayer;
    pane.appendChild(this.div_);

    // Ensures the label is redrawn if the text or position is changed.
    var me = this;
    this.listeners_ = [
        google.maps.event.addListener(this, 'position_changed',
                                      function() { me.draw(); }),
        google.maps.event.addListener(this, 'text_changed',
                                      function() { me.draw(); })
    ];
};

// Implement onRemove
CountLabel.prototype.onRemove = function() {
    this.div_.parentNode.removeChild(this.div_);

    // CountLabel is removed from the map, stop updating its position/text.
    for (var i = 0, I = this.listeners_.length; i < I; ++i) {
        google.maps.event.removeListener(this.listeners_[i]);
    }
};

// Implement draw
CountLabel.prototype.draw = function() {
    var projection = this.getProjection();
    var position = projection.fromLatLngToDivPixel(this.get('position'));

    var div = this.div_;
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';
    div.style.display = 'block';

    this.span_.innerHTML = this.get('text').toString();
};

