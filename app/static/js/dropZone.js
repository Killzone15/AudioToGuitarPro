import { uploadFileFromSource } from "./fileUploader.js";  // Импортируем функцию

document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");

    // Dragover — когда мышка с файлом над зоной
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();  // Нужно для разрешения drop
        dropZone.classList.add("dragover");
        console.log("Dragover event triggered on dropZone");
    });

    // Dragleave — когда мышка уходит из зоны
    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
        console.log("Dragleave event triggered on dropZone");
    });

    // Drop — когда файл сброшен
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        console.log("Drop event triggered on dropZone");

        const files = e.dataTransfer.files;
        const items = e.dataTransfer.items;

        console.log("DataTransfer object:", e.dataTransfer);
        console.log("Files detected:", files);

        if (files.length > 0) {
            console.log("Files dropped:", files);
            uploadFileFromSource(files[0]);  // Загружаем файл
        } else if (items.length > 0) {
            console.warn("Файл не был получен, возможно, источник перетаскивания не поддерживается.");
            alert("⚠️ Файл не распознан. Попробуйте перетащить его из основного окна файлового менеджера.");
        } else {
            console.log("No files detected in dropZone");
        }
    });

    // Обработка выбора файла через input
    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            console.log("File selected via input:", file);
            uploadFileFromSource(file);
        }
    });
});
