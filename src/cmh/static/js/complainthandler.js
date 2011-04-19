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

function populate_sub_select (parent_sel_id, child_sel_id, child_empty_text, url) {
    var retfn = function () {
        var parent_sel_val = $(parent_sel_id).val ();
        $.post (url,
                { select : parent_sel_val},
                function (data, status, jqXHR) {
                    $(child_sel_id).children ()
                        .remove ()
                        .end ()
                        .append ("<option value='----'>-- " + child_empty_text + " --</option>");
                    var json = $.parseJSON (data);
                    $.each (json, function (key, val) {
                                $(child_sel_id).children ().end ().append ("<option value='"
                                                                           + val.optval
                                                                           + "'>"
                                                                           + val.name
                                                                           + "</option>");
                            });
                });
    };
    return retfn;
}


function populate_default_complaint_description (select_elem_id, child_elem_id, url) {
    var retfn = function () {
        var select_elem_val = $(select_elem_id).val ();
        $.post (url,
                { select : select_elem_val },
                function (data, status, jqXHR) {
                    var json = $.parseJSON (data);
                    $(child_elem_id).val (json.description);
                });
    };

    return retfn;
}
