import { uploadFileFromSource } from "./fileUploader.js";  // Импортируем функцию

document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");

    // Проверка: только .mp3
    function isMp3File(file) {
        return file && (
            file.type === "audio/mpeg" ||
            file.name.toLowerCase().endsWith(".mp3")
        );
    }

    function handleFile(file) {
        if (!isMp3File(file)) {
            alert("Этот формат не поддерживается. Разрешены только MP3-файлы.");
            return;
        }
        console.log("Файл прошёл проверку:", file);
        uploadFileFromSource(file);
    }

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        const files = e.dataTransfer.files;
        const items = e.dataTransfer.items;

        if (files.length > 0) {
            const file = files[0];
            handleFile(file);
        } else if (items.length > 0) {
            alert("⚠️ Файл не распознан. Попробуйте перетащить его из файлового менеджера.");
        }
    });

    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });
});
