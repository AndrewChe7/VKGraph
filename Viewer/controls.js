$("#size").on("click", function () {
	$("svg").attr("width", $("#width").val());
	$("svg").attr("height", $("#height").val());
});

$("#load").on("click", function () {
	loadJSON($("#file").val().replace(/C:\\fakepath\\/i, ''));
});
