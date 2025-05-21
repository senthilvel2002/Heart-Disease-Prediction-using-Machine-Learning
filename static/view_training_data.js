document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById("trainingDataTable");

    table.addEventListener("mouseover", function (e) {
        if (e.target.tagName === "TD") {
            e.target.style.backgroundColor = "#bbdefb";
        }
    });

    table.addEventListener("mouseout", function (e) {
        if (e.target.tagName === "TD") {
            e.target.style.backgroundColor = "";
        }
    });
});
