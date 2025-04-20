import os
from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем файл из формы
        file = request.files['file']

        if file:
            # Получаем имя файла
            filename = file.filename

            # Путь для сохранения файла (в папку audio)
            audio_folder = os.path.join('app', 'audio')

            # Создаем папку, если она не существует
            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)

            # Сохраняем файл
            file.save(os.path.join(audio_folder, filename))
            return f"Файл {filename} успешно загружен!"

    return render_template('index.html')
