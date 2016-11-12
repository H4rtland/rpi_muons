var timer = setInterval(countTimer, 1000);
var detector_running_seconds = 0;
function countTimer() {
    var hour = Math.floor(detector_running_seconds /3600);
    var minute = Math.floor((detector_running_seconds - hour*3600)/60);
    var seconds = detector_running_seconds - (hour*3600 + minute*60);
    document.getElementById("run_timer").innerHTML = "Run time: " + hour + "h " + minute + "m " + seconds + "s";
    detector_running_seconds++;
}