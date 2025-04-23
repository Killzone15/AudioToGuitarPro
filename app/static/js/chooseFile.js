import { uploadFileFromSource } from "./fileUploader.js";

function uploadFile(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    if (file) {
        uploadFileFromSource(file);
    }
}

// Назначаем обработчик на выбор файла через кнопку:
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const chooseFileButton = document.getElementById("chooseFileButton");

    // Если кнопка существует, назначаем событие:
    if (chooseFileButton) {
        chooseFileButton.addEventListener("click", () => {
            fileInput.click(); // Триггерим выбор файла
        });
    }

    // Назначаем обработчик для input (выбор файла):
    if (fileInput) {
        fileInput.addEventListener("change", uploadFile);
    }
});
