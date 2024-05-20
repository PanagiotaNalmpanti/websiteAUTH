const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const searchBtn = document.getElementById("searchBtn");
    searchBtn.onclick = searchButtonOnClick;
    const saveBtn = document.getElementById("saveBtn");
    saveBtn.onclick = saveButtonOnClick;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const getName = document.getElementById("search-input");
    const request = new XMLHttpRequest();
    request.open("GET", `${api}/search?name=${getName.value}`);

    request.onreadystatechange = () => {
        if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {

            const requestText = JSON.parse(request.responseText);
            const tableBody = document.getElementById("result-table");

            // Clear previous results
            while (tableBody.rows.length > 1) {
                tableBody.deleteRow(1);
            }

            requestText.forEach((item) => {
                const row = document.createElement("tr");

                const cell_id = document.createElement("td");
                cell_id.innerText = item["_id"];
                row.appendChild(cell_id);

                const name = document.createElement("td");
                name.innerText = item["name"];
                row.appendChild(name);

                const production_year = document.createElement("td");
                production_year.innerText = item["production_year"];
                row.appendChild(production_year);

                const price = document.createElement("td");
                price.innerText = item["price"];
                row.appendChild(price);

                const color = document.createElement("td");
                color.innerText = item["color"];
                row.appendChild(color);

                const size = document.createElement("td");
                size.innerText = item["size"];
                row.appendChild(size);

                tableBody.appendChild(row);
            });
        }
    }
            request.send();

            // END CODE HERE

}

saveButtonOnClick = () => {
    // BEGIN CODE HERE
    const getName1= document.getElementById("name-input");
    const getName2 = document.getElementById("prod-input");
    const getName3 = document.getElementById("price-input");
    const getName4 = document.getElementById("color-input");
    const getName5 = document.getElementById("size-input");

    const product_data = {
        name: getName1.value,
        production_year: getName2.value,
        price: getName3.value,
        color: getName4.value,
        size: getName5.value
    };

    const request = new XMLHttpRequest();
    request.open("POST", `${api}/add-product`);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    
    request.onreadystatechange = () => {
         if (request.readyState === XMLHttpRequest.DONE && (request.status === 200 || request.status === 201)) {
             alert("OK");
             document.getElementById("productForm").reset();
         }
    }
    request.send(JSON.stringify(product_data));
    // END CODE HERE
}