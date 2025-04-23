// fileUploader.js
function uploadFileFromSource(file) {
    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("spinner").style.display = "block";

    fetch("/", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("spinner").style.display = "none";

        const messageDiv = document.getElementById("responseMessage");
        const responseText = document.getElementById("responseText");

        responseText.innerHTML = data.message;
        messageDiv.style.display = "block";

        if (data.download_url) {
            const link = document.createElement("a");
            link.href = data.download_url;
            link.innerText = "Скачать Guitar Pro файл";
            link.style.display = "block";
            responseText.appendChild(document.createElement("br"));
            responseText.appendChild(link);
        }
    })
    .catch(error => {
        document.getElementById("spinner").style.display = "none";
        console.error("Ошибка при загрузке файла:", error);
    });
}

export { uploadFileFromSource };
