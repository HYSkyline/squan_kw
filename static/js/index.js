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

function urlInputHidden() {
    document.getElementById("fpath_u").value = "none";
    document.getElementById("fpath_u").style.display = "none";
    document.getElementById("filepathURLLabel").style.display = "none";
}

function fileInputHidden() {
    // document.getElementById("fpath_f").value = "none";
    document.getElementById("fpath_f").style.display = "none";
    document.getElementById("fileUploadBtn").style.display = "none";
    document.getElementById("addbr").style.display = "none";
    document.getElementById("filepathFILELabel").style.display = "none";
    document.getElementById("filepathURLLabel").textContent = "统计资料网址已填入";
}