var timer = setInterval(countTimer, 1000);
var detector_running_seconds = 0;
function countTimer() {
    var elementExists = !!document.getElementById("run_timer");
    if (elementExists == false) {
        return;
    }
    var hour = Math.floor(detector_running_seconds /3600);
    var minute = Math.floor((detector_running_seconds - hour*3600)/60);
    var seconds = detector_running_seconds - (hour*3600 + minute*60);
    document.getElementById("run_timer").innerHTML = "Run time: " + hour + "h " + minute + "m " + seconds + "s";
    detector_running_seconds++;
}

$(document).ready(function() {
    updateMuons();
    function updateMuons() {
        setTimeout(updateMuons, 10000);
        $.getJSON($SCRIPT_ROOT + '/current_muons', function(data) {$("#current_muons").text("Current muons: " + data.result)});
    }
});
