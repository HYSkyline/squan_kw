function infoFetch() {
    $.get("/info", function(data) {
        $("#tempInfo").text(data);
    });
};

$("#btnStart").click(function() {
    var file_f_part = document.getElementById("fpath_f").value.split("\\");
    var file_f = file_f_part[file_f_part.length - 1];
    var file_u = document.getElementById("fpath_u").value;
    var fpath = '';
    if (file_f != '') {fpath=file_f} else {fpath=file_u}

    var projName = document.getElementById("fname").value;

    var work_mode = 'local';
    if (document.getElementById('online').checked) {work_mode='online'};

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/process',
        contentType: 'application/json',
        data: JSON.stringify({
            file_address: fpath,
            proj_name: projName,
            model: work_mode
        }),
        function(result) {
            $("#tempPanel").text(result);
        }
    });

    var interval = self.setInterval("infoFetch()", 1000);
})
