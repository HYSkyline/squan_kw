var interval = self.setInterval("infoFetch()", 1000);

function infoFetch() {
    $.get("/info", function(data) {
        $("#tempInfo").text(data);
    });
};
