    // datepicker element
    $(document).ready(function(){
        $( "#datepickerA, #datepickerB" ).datepicker({
                dateFormat: "yy-mm-dd", 
            });
        
        // action to update graphe when date is clicked
        $(document).on("click", "#butta", function(event, ui){
            // create template for data to graph
            window.trace1 = {
            x: [],
            y: [],
            mode: 'lines'
            };
            window.trace2 = {
            x: [],
            y: [],
            mode: 'lines'
            };
            // elements for get request
            var brand1 = $('#brandSelect1 :selected').text()
            console.log(brand1)
            var brand2 = $('#brandSelect2 :selected').text()
            console.log(brand2)
            
            var tdateA = $("#datepickerA").datepicker("getDate")
            var tdate1 = $.datepicker.formatDate("yy-mm-dd", tdateA)
            var tdateB = $("#datepickerB").datepicker("getDate")
            var tdate2 = $.datepicker.formatDate("yy-mm-dd", tdateB)

            var urlA = 'data/date/' + tdate1 + '/brand/';
            var urlB = 'data/date/' + tdate2 + '/brand/';

            // get request to grab data from db
            function first() {
                var deferred = $.Deferred();
                $.ajax({
                    dataType: 'json',
                    url: urlA,
                    // push data into var window.trace1 
                    success: function (data) {
                        for (var i = 0; i < data.length; i++) {
                            window.trace1.x.push(data[i].Tstamp);  
                            window.trace1.y.push(parseInt(data[i].Stat));
                            }
                    }
                });
                return deferred.promise();
            };
            function second() {
                $.ajax({
                    dataType: 'json',
                    url: urlB,
                    // push data into var window.trace1 
                    success: function (data) {
                        for (var i = 0; i < data.length; i++) {
                            window.trace2.x.push(data[i].Tstamp);  
                            window.trace2.y.push(parseInt(data[i].Stat));
                            }
        
                        // assign var to the graph div
                        var graph = document.getElementById('graph');
                        
                        Plotly.newPlot(graph, [window.trace1, window.trace2] );
                    }
                });
            };
            
            first().then(second());
        });
    });
