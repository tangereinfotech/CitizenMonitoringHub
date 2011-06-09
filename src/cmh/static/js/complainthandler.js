var field_autocomplete = function (field_tag, db_id_tag, detail_id_tag, url) {
    var cache = {}, lastXhr;

    $(field_tag).autocomplete ({minLength : 0,
                                source : function (request, response) {
                                    var term = request.term;
                                    if (term in cache) {
                                        response (cache [term]);
                                        return;
                                    } else {
                                        lastXhr = $.getJSON (url, 
                                                             request, 
                                                             function (data, status, xhr) {
                                                                 cache [term] = data;
                                                                 if (xhr === lastXhr) {
                                                                     response (data);
                                                                 }
                                                             });
                                    }
                                },
                                focus : function (event, ui) {
                                    $(field_tag).val (ui.item.display);
                                    return false;
                                },
                                select: function (event, ui) {
                                    $(field_tag).val (ui.item.display);
                                    $(db_id_tag).val (ui.item.id);
                                    $(detail_id_tag).html (ui.item.detail);
                                    return false;
                                }
                               })
        .data ("autocomplete")._renderItem = function (ul, item) {
            return $( "<li></li>")
                .data ("item.autocomplete", item)
                .append ("<a>" + item.display + "<br/>" + item.detail + "</a>")
                .appendTo (ul);
        };
};

var showContextMenu = function (row_class, menu_id) {
  $("tr" + row_class).contextMenu ({'menu' : menu_id},
                                   function (action, el, pos) {
                                       complaintno = $(el).find ("td.complaintno").text ();
                                       var f = document.createElement ("form");
                                       f.action = "/complaint/" + action + "/" + complaintno + "/";
                                       f.method = "get";
                                       f.submit ();
                                       // var form = el.find (".complaintno" + action + " form");
                                       // form.submit ();
                                   });
};

var plots = {};

var show_hot_complaints = function (chart_id, url, departments, period_start, period_end) {
    var colors = ["#663333", "#FFFF33", "#0066CC", "#669900", "#CC0099", "#666666", "#660000", "#00FFFF", 
                  "#9966FF", "#006600", "#FFE87C", "#FF3300", "#003366", "#CC9900", "#FFCCFF", "#CCFF33", 
                  "#660066", "#FFCC00", "#003300", "#00BFFF", "#8D38C9", "#F778A1", "#FDD017", "#666633", 
                  "#FF9933", "#660033", "#FFFF00", "#999999", "#0099FF", "#CCFF00", "#663300", "#CCCCFF", 
                  "#FF0000", "#C9BE62", "#2F4F4F", "#000000", "#FFF0F5", "#D3D3D3", "#191970", "#EEE8AA", 
                  "#8B6508", "#FFDEAD", "#CDB7B5", "#CD1076", "#E066FF", "#F88158", "#87F717", "#333300",
                  "#3399FF", "#C3FDB8"];

    $.getJSON (url, 
               {
                   departments : departments,
                   stdate : period_start,
                   endate : period_end
               },
               function (data, status, xhr) {
                   $.each (data.departments, function (index, value) {
                               $(".dept-selector.deptid-" + value [0]).css("background-color", colors [index]);
                           });
                   if (chart_id in plots) {
                       $('#' + chart_id).empty ();
                   }
                   var series = data.datapoints [0];
                   var min_date = series [0][0];
                   var max_date = series [series.length - 1][0];
                   plots [chart_id] = $.jqplot(chart_id, data.datapoints,
                                               {
                                                   seriesColors : colors,
                                                   axes : {
                                                       xaxis : {
                                                           renderer:$.jqplot.DateAxisRenderer,
                                                           tickOptions: {formatString: '%b %#d'},
                                                           min : min_date,
                                                           max : max_date
                                                       },
                                                       yaxis : {
                                                           min: 0,
                                                           tickOptions: {formatString: '%d'}
                                                       }
                                                   },
                                                   seriesDefaults : {
                                                       showMarker : true,
                                                       pointLabels: { 
                                                           show:false, 
                                                           ypadding: 3,
                                                           edgeTolerance: 4
                                                       } 
                                                   }
                                               });
               });
};