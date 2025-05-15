var modeForm = document.getElementById("modeForm");
var onlineBtn = document.getElementById("online");
var modeInput = document.getElementById("modeText");

modeForm.addEventListener('click', function(e) {
    if (onlineBtn.checked) {
        document.getElementById("modeText").value="联网模式";
    } else {
        document.getElementById("modeText").value="本地模式";
    }
});