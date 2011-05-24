var select_handler = function (url, parent_select, child_select) {
    var dept_id = $(parent_select + " option:selected").val ();
    $.getJSON (url,
               {department : dept_id},
               function (data, status, xhr) {
                   $(child_select).empty ();
                   var options = "";
                   $.each (data, function (key, value) {
                               options += "<option value=\"" + value [0] + "\">" 
                                   + value [1]
                                   + "</option>";
                           });
                   $(child_select).html (options);
               });
};
