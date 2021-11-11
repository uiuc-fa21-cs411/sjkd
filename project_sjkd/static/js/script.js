var getData
var getMod

$( document ).ready(function() {
    plotly_canvas_result_table = document.getElementById('canvas-result-table')

    getData = function (query_string) {
        $.post( "/query", {
            query_string: query_string
        }, function(result, status){
            result_data = result['data']

            var data = [{
                type: 'table',
                header: {
                  values: result_data['labels'],
                  align: "center",
                  line: {width: 1, color: 'black'},
                  fill: {color: "grey"},
                  font: {family: "Arial", size: 12, color: "white"}
                },
                cells: {
                  values: result_data['values'],
                  align: "center",
                  line: {color: "black", width: 1},
                  font: {family: "Arial", size: 11, color: ["black"]}
                }
            }]

            Plotly.newPlot(plotly_canvas_result_table, data)

            var bar_data = [
                {
                    type: 'bar',
                    x: result_data['values'][0],
                    y: result_data['values'][1]
                }
            ]

        }, 'json')
    }

    $("#queryButton").click(function() {
        getData($("#sql-text-area").val())
    })
    $("#selectButton").click(function() {
        getData("select * from " + $("#table-selection").val())
    })
    $("#createButton").click(function() {
        let input = $('#song_name').val() + "," +
                    $('#artist_name').val() + "," +
                    $('#city_id').val() + "," +
                    $('#spotify_song_id').val() + "," +
                    $('#duration_s').val();
        $.post( "/create", {
            input: input
        }, function(result, status){
        })
    })
    $("#deleteButton").click(function() {
        let input = $('#song_id').val();
        $.post( "/delete", {
            input: input
        }, function(result, status){
        })
    })
    $("#updateButton").click(function() {
        let input = $('#song_id').val() + "," +
                    $('#song_name').val() + "," +
                    $('#artist_name').val() + "," +
                    $('#city_id').val() + "," +
                    $('#spotify_song_id').val() + "," +
                    $('#duration_s').val();
        $.post( "/update", {
            input: input
        }, function(result, status){
        })
    })
})