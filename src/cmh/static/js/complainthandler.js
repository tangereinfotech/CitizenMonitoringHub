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

function getTableRow (table_elem_id, offset_y) {
    var height = 0;
    var rownum = 0;
    $.each ($(table_elem_id + " tr").get (), function (index) {
                height += $(this).height ();
                if (height > offset_y) {
                    rownum = index;
                    return false;
                }
            });
    return rownum;
};

var showContextMenu = function (elem_id, menu_id, url) {
  $(elem_id).contextMenu ({'menu' : menu_id},
                      function (action, el, pos) {
                          alert (getTableRow (elem_id, pos.y));
                      });
};
