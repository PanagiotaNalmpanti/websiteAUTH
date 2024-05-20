const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const searchBtn = document.getElementById("searchBtn");
    searchBtn.onclick = searchButtonOnClick;
    const saveButton = document.getElementById("saveBtn");
    saveButton.onclick = productFormOnSubmit;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const getName = document.getElementById("search-input");
    const request = new XMLHttpRequest();
    request.open("GET", `${api}/search?name=${getName.value}`,true);

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
    };
    getName.value = "";
    request.send();
    // END CODE HERE
}

    productFormOnSubmit = (event) => {
        // BEGIN CODE HERE
        const getName = document.getElementById("name-input");
        const getProductionYear = document.getElementById("prod-input");
        const getPrice = document.getElementById("price-input");
        const getColor = document.getElementById("color-input");
        const getSize = document.getElementById("size-input");

        if (getName.value !== "" && getProductionYear.value !== "" && getPrice.value !== "" && getColor.value !== "" && getSize.value !== "") {
            const res = new XMLHttpRequest();
            res.open("POST", `${api}/add-product`);
            res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            res.onreadystatechange = () => {
                if (res.readyState == 4) {
                    if (res.status == 200) {
                        alert(res.responseText);
                        // clear fields after successful update or addition
                        getName.value = "";
                        getProductionYear.value = "";
                        getPrice.value = "";
                        getColor.value = "";
                        getSize.value = "";
                    }
                    else {
                        alert(res.responseText);
                    }
                }
            };

            res.send(JSON.stringify({
                "name": getName.value,
                "production_year": parseInt(getProductionYear.value),
                "price": parseInt(getPrice.value),
                "color": parseInt(getColor.value),
                "size": parseInt(getSize.value)
            }));
        }
        else {
            alert("Please fill in all fields");
        }

    // END CODE HERE
}