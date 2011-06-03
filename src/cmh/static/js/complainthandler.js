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
                                       var form = el.find ("." + action + " form");
                                       form.submit ();
                                   });
};

var plots = {};

var show_hot_complaints = function (chart_id, url, departments, period_start, period_end) {
    $.getJSON (url, 
               {
                   departments : departments,
                   stdate : period_start,
                   endate : period_end
               },
               function (data, status, xhr) {
                   if (chart_id in plots) {
                       $('#' + chart_id).empty ();
                   }
                   var series = data.datapoints [0];
                   var min_date = series [0][0];
                   var max_date = series [series.length - 1][0];
                   plots [chart_id] = $.jqplot(chart_id, data.datapoints,
                                               {
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