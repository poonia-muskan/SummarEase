const API_URL = "http://127.0.0.1:8000";

function getFile() {
    return document.getElementById("fileInput").files[0];
}

function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
    document.getElementById("outputText").classList.add("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
    document.getElementById("outputText").classList.remove("hidden");
}

function showOutputBox() {
    document.querySelector(".output").classList.add("show");
}

async function summarize() {
    const file = getFile();
    if (!file) {
        alert("Please upload a file first!");
        return;
    }

    showLoader();
    document.getElementById("downloadBtn").classList.add("hidden");

    const wordLimit = document.getElementById("wordLimit").value.trim();
    const lang = document.getElementById("languageSelect").value.trim();

    let formData = new FormData();
    formData.append("file", file);

    let url = `${API_URL}/summarize`;
    const params = new URLSearchParams();

    if (wordLimit !== "" && !isNaN(wordLimit)) params.append("words", wordLimit);
    if (lang !== "" && lang !== "Auto") params.append("target_lang", lang);

    if ([...params].length > 0) url += "?" + params.toString();

    try {
        const response = await fetch(url, { method: "POST", body: formData });
        const data = await response.json();

        hideLoader();

        document.getElementById("outputText").textContent = data.summary;
        document.getElementById("engineText").textContent = `(${data.engine})`;
        document.getElementById("downloadBtn").classList.remove("hidden");

        showOutputBox();

    } catch (error) {
        hideLoader();
        alert("Error summarizing file.");
    }
}

async function getKeywords() {
    const file = getFile();
    if (!file) {
        alert("Please upload a file first!");
        return;
    }

    showLoader();
    document.getElementById("downloadBtn").classList.add("hidden");

    let formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/keywords`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        hideLoader();

        document.getElementById("outputText").textContent = data.keywords.join(", ");
        document.getElementById("engineText").textContent = "(Keywords)";
        
        showOutputBox();

    } catch (error) {
        hideLoader();
        alert("Error extracting keywords.");
    }
}

function downloadSummary() {
    const text = document.getElementById("outputText").textContent;
    if (!text) {
        alert("No summary to download.");
        return;
    }

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "summary.txt";
    link.click();
}

if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light");
}

function toggleTheme() {
    document.body.classList.toggle("light");
    localStorage.setItem(
        "theme",
        document.body.classList.contains("light") ? "light" : "dark"
    );
}
