var a = "";
$("tr.cells-middle > td:nth-of-type(2) > a:last-child").each(function(){ a += /\/\d+/.exec($(this).attr("href"));})