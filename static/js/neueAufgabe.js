const toggleKnopf = document.getElementById("toggleKnopf");
const meinDiv = document.getElementById("meinDiv");

toggleKnopf.addEventListener("click", () => {
    if (meinDiv.style.display === "none") {
        meinDiv.style.display = "block"; //
    } else {
        meinDiv.style.display = "none";  
    }
});
