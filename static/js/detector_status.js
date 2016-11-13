var timer = setInterval(countTimer, 1000);
var detector_running_seconds = 0;
var run_scripts = false;
function countTimer() {
    if (!run_scripts) {
        return;
    }
    var hour = Math.floor(detector_running_seconds /3600);
    var minute = Math.floor((detector_running_seconds - hour*3600)/60);
    var seconds = detector_running_seconds - (hour*3600 + minute*60);
    document.getElementById("run_timer").innerHTML = "Run time: " + hour + "h " + minute + "m " + seconds + "s";
    detector_running_seconds++;
}

$("#current_muons").ready(function() {
    updateMuons();
    function updateMuons() {
        if (!run_scripts) {
            return;
        }
        setTimeout(updateMuons, 10000);
        $.getJSON($SCRIPT_ROOT + '/current_muons', function(data) {
            if (data.reload) {
                window.location.href = 'detector';
            } else {
                $("#current_muons").text("Current muons: " + data.result);
            }
        });
    }
});

/*$(document).ready(function() {
    $(".alert").fadeTo(5000, 500).slideUp(500, function(){
        $(this).remove();
    });
});*/