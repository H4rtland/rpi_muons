var result_id = 0;
var current_status = "";
var run_scripts = false;

$(document).ready(function() {
    check_reload();
    function check_reload() {
        if (!run_scripts) {
            return;
        }
        setTimeout(check_reload, 1000);
        $.getJSON($SCRIPT_ROOT + '/check_progress/' + result_id,
            {current_status: current_status},
            function(data) {
                if (data.reload) {
                    window.location.href = window.location.href;
                }
            }
        );
    }
});