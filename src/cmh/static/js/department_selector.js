var department_selector = function (url) {
    $('.selector.all').change (
        function (event) {
            var checked_status = this.checked;
            $('.selector').each (
                function () {
                    this.checked = checked_status;
                }
            );
        });
    $('.selector').change (
        function (event) {
            if (this.checked == false) {
                $('.selector.all').removeAttr ("checked");
            }
            var selected_dept_ids = $('.selector:checked').map (
                function () {
                    return $(this).val ();
                }
            ).get ().join (',');
            MapHandler.update_with_stats (url, selected_dept_ids);
        });
};