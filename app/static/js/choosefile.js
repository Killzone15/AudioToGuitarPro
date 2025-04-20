function uploadFile(event) {
    var formData = new FormData();
    var file = event.target.files[0];
    formData.append("file", file);

    // Используем jQuery для отправки данных через AJAX
    $.ajax({
        url: '/',  // URL для загрузки файла (на сервере Flask)
        type: 'POST',
        data: formData,
        contentType: false,  // важно: не устанавливать content-type
        processData: false,  // важно: не обрабатывать данные
        success: function(response) {
            // Показываем сообщение с результатом
            $('#responseMessage').show();
            $('#responseText').text(response);
        },
        error: function() {
            alert("Произошла ошибка при загрузке файла.");
        }
    });
}
