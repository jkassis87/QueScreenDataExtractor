/*
Intended view: DateRange.blade.php
The purpose of this script is to:
1 - Get dates from the 2 datepicker elements
2 - Send those dates to db via a get reqest to retrieve data for between and inclding the selected dates
3 - Display that data via the Plotly js plugin ()
*/

$(document).ready(function(){

    // creates 2x jqueryui datepicker objects
    $( "#dpFROM, #dpTO" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        dateFormat: "yy-mm-dd"
    });

    // when the html5 button is clicked, data is retrieved and graph is generated
    $( "#submitButton" ).click(function () {

        // array for Plotly data trace
        window.tracerange = {
                x: [],
                y: [],
                mode: 'lines'
                };

        // vars for start and end dates form the datepickers in a "YYYY-MM-DD" string
        var sdate = $("#dpFROM").datepicker().val();
        var edate = $("#dpTO").datepicker().val();
        
        // var for the brand as a string
        var brand = $('#brandSelect :selected').text();

        // var for the get request
        var geturl = 'rangedata/sdate/' + sdate + '/edate/' + edate + '/brand/' + brand;
        
        // logging for debugging only
        console.log(sdate);
        console.log(edate);
        console.log(brand);
        console.log(geturl);

        // get data from sql as json
        $.ajax({
            dataType: 'json',
            url: geturl,

            // add data to variable
            success: function(data) {
                for (var i = 0; i < data.length; i++) {
                    window.tracerange.y.push(parseInt(data[i].Stat));
                    window.tracerange.x.push(data[i].Tstamp);  
                }

                var graph = document.getElementById('graph');

                // invoke plotly to plot the graph
                Plotly.newPlot(graph, [window.tracerange]);
                
            }
        })

    });
    
});
