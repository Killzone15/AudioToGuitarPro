from flask import Blueprint, render_template, request, send_from_directory, jsonify
import os
from app.core.main import process_audio_file
from app.core.file_utils import FileUtils

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    message = None
    download_url = None

    if request.method == 'POST':
        file = request.files.get('file')
        print(f"\n  Выбран файл {file} \n")

        if file:
            filename = file.filename
            audio_folder = os.path.join('app', 'audio')
            file_utils = FileUtils(audio_path=os.path.join(audio_folder, filename), directory=audio_folder)

            file_utils.ensure_directory_exists()

            file_path = os.path.join(audio_folder, filename)
            file.save(file_path)

            try:
                # Обработка файла
                process_audio_file(file_path)

                # Используем метод get_transliterated_filename()
                file_utils_output = FileUtils(audio_path=file_path, directory='output')
                file_name = file_utils_output.get_transliterated_filename() + '.gp5'
                download_url = f"/download/{file_name}"

                message = f"Файл {filename} успешно загружен и обработан!"

                file_utils.remove_audio_file_after_analysis(filename, audio_folder)

            except Exception as e:
                message = f"Ошибка при обработке файла: {e}"
                print(f"Ошибка: {e}")

        # Если это AJAX-запрос
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'message': message,
                'download_url': download_url
            })

    return render_template('index.html', message=message, download_url=download_url)


@main.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    print(f"Зашли в маршрут для скачивания файла: {filename}")

    output_dir = os.path.join(os.getcwd(), 'output')
    output_file_path = os.path.join(output_dir, filename)

    file_utils = FileUtils(directory=output_dir)

    # Удаляем старые файлы
    file_utils.remove_old_files(max_age=300)

    # Проверяем существование файла
    if file_utils.check_file_exists(output_file_path):
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

