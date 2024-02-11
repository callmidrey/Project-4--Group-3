/// static/js/result.js

document.addEventListener("DOMContentLoaded", function () {
    // Fetch and display results when the DOM is fully loaded
    fetchResults();
});

function fetchResults() {
    fetch('/getResults')
        .then(response => response.json())
        .then(data => {
            // Process and display the fetched results
            displayResults(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function displayResults(data) {
    const resultContainer = document.getElementById("resultContainer");

    if (resultContainer) {
        // Clear existing content in the result container
        resultContainer.innerHTML = "";

        // Create a new list element to display results
        const resultList = document.createElement("ul");

        // Iterate over the data and create list items for each result
        for (const key in data) {
            const listItem = document.createElement("li");
            listItem.textContent = `${key}: ${data[key]}`;
            resultList.appendChild(listItem);
        }

        // Append the list to the result container
        resultContainer.appendChild(resultList);
    }
}
