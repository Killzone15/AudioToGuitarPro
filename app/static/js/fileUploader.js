let isFileBeingUploaded = false; // Флаг для предотвращения повторной загрузки

function uploadFileFromSource(file) {
    if (isFileBeingUploaded) {
        console.log("Файл уже загружается, повторная попытка запрещена.");
        return; // Если файл уже загружается, ничего не делаем
    }

    isFileBeingUploaded = true;  // Устанавливаем флаг загрузки

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
        isFileBeingUploaded = false;  // Снимаем флаг после завершения загрузки

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
        isFileBeingUploaded = false;  // Снимаем флаг в случае ошибки
        document.getElementById("spinner").style.display = "none";
        console.error("Ошибка при загрузке файла:", error);
    });
}

export { uploadFileFromSource };
