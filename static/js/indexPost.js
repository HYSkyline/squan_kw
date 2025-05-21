function infoFetch() {
    $.ajax({
        type: 'GET',
        url: '/info',
        contentType: 'application/json',
        success: function(data) {
            $("#tempInfo").empty();
            var infoList = data.split("\n");
            for (var i = infoList.length - 1; i >= 0; i--) {
                $("#tempInfo").prepend('<p class="info">' + infoList[i] + '</p>');
            }
        },
    });
};

function alertWithCallback(message, callback) {
    alert(message);
    if(typeof callback === 'function') {
        callback();
    }
}

$('#fpath_f').change(function (e) {
    var files = e.target.files;
    var formFile = new FormData();
    formFile.append("file", files[0]);
    $.ajax({
        type: 'POST',
        url: '/upload',
        contentType: false,
        data: formFile,
        dataType: 'json',
        cache: false,
        processData: false,
        success: function (result) {
            console.log(result);
        }
    })
});

$("#btnStart").click(function() {
    var file_f_part = document.getElementById("fpath_f").value.split("\\");
    var file_f = file_f_part[file_f_part.length - 1];
    var file_u = document.getElementById("fpath_u").value;
    var fpath = '';
    if (file_f != '') {fpath=file_f} else {fpath=file_u}

    var projName = document.getElementById("fname").value;

    var work_mode = 'local';
    if (document.getElementById('online').checked) {work_mode='online'};

    $("#btnStart").attr("disabled","disabled");
    $("small").eq(3).text("程序运行中……");
    $("#tempPanel").text("程序仍在持续运行，请稍等");
    var interval = self.setInterval("infoFetch()", 1000);
    $.ajax({
        type: 'POST',
        url: '/process',
        contentType: 'application/json',
        data: JSON.stringify({
            file_address: fpath,
            proj_name: projName,
            model: work_mode
        }),
        success: function(result) {
            $("#tempPanel").text(result);
            clearInterval(interval);
            $(".row-step").eq(3).attr({style: 'background-color: aliceblue;'});
            $("#downloadBtn").removeAttr("disabled");
            $("small").eq(3).text("点击结果下载按钮，保存数据提取结果");
            alert('数据抽取任务完成，请单击“结果下载”按钮以保存输出结果。')
        },
    });
});

$("#downloadBtn").click(function () {
    var projName = $("#fname").value;
    var a = $("downloadLink");
    a.href = "/download";
    a.download = projName + '-数据抽取结果.xls';
    a.click();
    $(".row-step").eq(3).attr({style: 'background-color: white;'});
    
    alertWithCallback('输出结果保存后，请刷新网页以开始下一项抽取任务', function() {
        location.reload();
    });
});



