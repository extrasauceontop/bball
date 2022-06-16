function grab_and_filter() {
    // Read in the island data
    d3.json("/data_week_preds").then((data) => {
        //Format it into an array
        keys = Object.entries(data)

        var filtered_list = []
        keys.forEach((datum, index) => {
            console.log(datum)
            filtered_list.push(datum)

        })
    make_table(filtered_list)
    })
}

function make_table(filtered_list) {
    var restructured_list = []
    filtered_list.forEach((game, index) => {
        contest = game[1]
        delete contest["pred_value"]
        restructured_list.push(contest)
    })

    var myTable = document.getElementById("dataTable")
    myTable.innerHTML = ""

    restructured_list.forEach(function(tableRow) {
        // Create a row for each Object in tableData
        var row = tbody.append("tr");
    
        // Create a cell for each value in the Object
        Object.entries(tableRow).forEach(function([key, value]) {
            var cell = row.append('td');
            // Put value into the cell
            cell.text(value)
        });
    });
}

var tbody = d3.select("tbody")

grab_and_filter()
console.log("hi")