from flask import Blueprint, render_template, request, send_from_directory, jsonify
import os
import shutil
from app.core.main import process_audio_file  # Импортируем основную функцию обработки

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    message = None
    download_url = None

    if request.method == 'POST':
        file = request.files.get('file')

        if file:
            filename = file.filename
            audio_folder = os.path.join('app', 'audio')

            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)

            file_path = os.path.join(audio_folder, filename)
            file.save(file_path)

            try:
                process_audio_file(file_path)

                output_dir = 'output/'
                file_name = filename.rsplit('.', 1)[0] + '.gp5'
                download_url = f"/download/{file_name}"

                message = f"Файл {filename} успешно загружен и обработан!"
            except Exception as e:
                message = f"Ошибка при обработке файла: {e}"

            os.remove(file_path)

            if not os.listdir(audio_folder):
                shutil.rmtree(audio_folder)

        # Если запрос AJAX (fetch), возвращаем JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'message': message,
                'download_url': download_url
            })

    return render_template('index.html', message=message, download_url=download_url)

@main.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    print(f"Зашли в маршрут для скачивания файла: {filename}")  # Принт на проверку

    # Получаем абсолютный путь
    output_dir = os.path.join(os.getcwd(), 'output')  # Абсолютный путь к папке output

    # Формируем путь к файлу на основе переданного имени
    output_file_path = os.path.join(output_dir, filename)

    # Проверяем существование файла
    if os.path.exists(output_file_path):
        print(f"Файл для отправки: {output_file_path}")
        print(f"Существует ли файл: {os.path.exists(output_file_path)}")

        try:
            return send_from_directory(
                directory=output_dir,
                path=filename,
                as_attachment=True,
                mimetype='application/octet-stream',
                download_name=filename
            )
        except Exception as e:
            print(f"Ошибка при отправке файла: {e}")
            return "Ошибка при отправке файла", 500
    else:
        print(f"Файл не найден: {output_file_path}")
        return "Файл не найден", 404
