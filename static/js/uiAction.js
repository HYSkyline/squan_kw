$(document).ready(function () {
    $(".row-step:first").attr({style: 'background-color: aliceblue;'});
    $("#btnStart").removeAttr("disabled");
    $("#downloadBtn").attr("disabled","disabled");
});

// 文件输入处理
$("#fpath_f").click(function () {
    $("hr").attr({style: 'display:none'});
    $("#fpath_u").text("none");
    $("#fpath_u").attr({style: 'display:none'});
    $("#filepathURLLabel").attr({style: 'display:none'});
    $('small:first').text("若不小心选错，重新刷新网页就好");

    $(".row-step").eq(0).attr({style: 'background-color: white;'});
    $(".row-step").eq(1).attr({style: 'background-color: aliceblue;'});
});
$("#fpath_u").change(function () {
    $("hr").attr({style: 'display:none'});
    $("#fpath_f").attr({style: 'display:none'});
    $(".addbr").remove();
    $("#filepathFILELabel").attr({style: 'display:none'});
    $("#filepathURLLabel").text("统计资料网址已填入");
    $('small:first').text("若不小心选错，重新刷新网页就好");

    $(".row-step").eq(0).attr({style: 'background-color: white;'});
    $(".row-step").eq(1).attr({style: 'background-color: aliceblue;'});
});

// 项目名称填写
$("#fname").change(function () {
    $(".row-step").eq(1).attr({style: 'background-color: white;'});
    $(".row-step").eq(2).attr({style: 'background-color: aliceblue;'});
    $("#modeText").attr({style: 'background-color: aliceblue;'});
});

// 工作模式选择
$("#modeForm").click(function(e) {
    if ($('input[name="modeSelect"]:checked').val() == '联网模式') {
        $("#modeText").val("联网模式");
    } else {
        $("#modeText").val("本地模式");
    }
    $(".row-step").eq(2).attr({style: 'background-color: white;'});
    $(".row-step").eq(3).attr({style: 'background-color: aliceblue;'});
    $("#modeText").attr({style: 'background-color: white;'});
});

$("#btnStart").click(function() {
    $(".row-step").eq(3).attr({style: 'background-color: white;'});
    $("#processBar").attr({style: 'background-color: #F2F2F2;'});
});
