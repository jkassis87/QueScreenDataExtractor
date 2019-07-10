<!doctype html>
<html lang="en">
<head>
<title>Team Statistics</title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
</head>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>



var url = "data.php?brand=CR&date=2019-05-19%"

/*$.ajax({
            type: "GET", //rest Type
            dataType: 'json', //mispelled
            url: "data.php?brand=CR&date=2019-05-19%",
            contentType: "application/json; charset=utf-8",
            success: function (msg) {
                console.log(msg);                
            }
 });
*/

$.getJSON(url, function (json) {

    for (var i = 0; i < json.length; i++) {

        //console.log(json[i].Stat);
        //console.log(json[i].Tstamp);
        var tcount = json[i].Stat;
        var ttime = json[i].Tstamp;
        console.log("count " + tcount);
        console.log("time " + ttime);
    }
});

</script>

</head>

<body>

<button id="getStats">Get Stats</button>
<div id="cand"></div>


</body>
</html>
