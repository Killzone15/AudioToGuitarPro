document.addEventListener("DOMContentLoaded", function () {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");

  // Глобальное предотвращение открытия файла в браузере
  document.addEventListener("dragover", function (e) {
    e.preventDefault();
  }, false);

  document.addEventListener("drop", function (e) {
    e.preventDefault();
  }, false);

  dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropZone.classList.remove("dragover");

    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      // вручную запускаем функцию обработки
      uploadFile({ target: fileInput });
    }
  });
});
