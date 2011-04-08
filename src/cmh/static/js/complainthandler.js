function populate_sub_select (parent_sel_id, child_sel_id, child_empty_text, url) {
    var retfn = function () {
        var parent_sel_val = $(parent_sel_id).val ();
        $.post (url,
                { code : parent_sel_val},
                function (data, status, jqXHR) {
                    $(child_sel_id).children ()
                        .remove ()
                        .end ()
                        .append ("<option value='----'>-- " + child_empty_text + " --</option>");
                    json = $.parseJSON (data);
                    $.each (json, function (key, val) {
                                $(child_sel_id).children ().end ().append ("<option value='"
                                                                           + val.fields.code
                                                                           + "'>"
                                                                           + val.fields.name
                                                                           + "</option>");
                            });
                });
    };
    return retfn;
}
