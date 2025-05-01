import { uploadFileFromSource } from "./fileUploader.js";

// Проверка: только MP3-файл
function isMp3File(file) {
    return file && (
        file.type === "audio/mpeg" ||
        file.name.toLowerCase().endsWith(".mp3")
    );
}

function uploadFile(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file) {
        if (!isMp3File(file)) {
            alert("Пожалуйста, выберите файл в формате MP3.");
            fileInput.value = ''; // Сброс поля, чтобы можно было снова выбрать тот же файл
            return;
        }

        try {
            console.log("Загружается файл через кнопку:", file.name);
            uploadFileFromSource(file);
        } catch (err) {
            console.error("Ошибка при обработке файла:", err);
            alert("Произошла ошибка при загрузке файла. Пожалуйста, попробуйте снова.");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const chooseFileButton = document.getElementById("chooseFileButton");

    if (chooseFileButton) {
        chooseFileButton.addEventListener("click", () => {
            fileInput.click(); // Открывает диалог выбора файла
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", uploadFile);
    }
});
