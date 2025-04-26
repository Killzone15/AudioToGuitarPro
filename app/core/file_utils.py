# app/core/file_utils.py
import os
import time
import shutil
from unidecode import unidecode

def get_transliterated_filename(audio_path):
    """Возвращает имя файла без расширения, транслитерируя кириллицу в латиницу."""
    base_name = os.path.splitext(os.path.basename(audio_path))[0]  # Получаем имя файла без расширения
    return unidecode(base_name)  # Транслитерация

def remove_old_files(directory, max_age=600):
    """Удаляет файлы старше max_age секунд (по умолчанию 10 минут)."""
    current_time = time.time()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)  # Время последней модификации
            if file_age > max_age:
                try:
                    os.remove(file_path)
                    print(f"Файл {filename} удалён, так как он старше {max_age} секунд.")
                except Exception as e:
                    print(f"Ошибка при удалении файла {filename}: {e}")


def remove_audio_file_after_analysis(file_path, filename, audio_folder):
    """ Удаляет аудио файл пользователя с сервера после его аудио-анализа """
    os.remove(file_path)
    print(f"Файл {filename} успешно удалён")

    # Если папка пуста, удаляем её
    if not os.listdir(audio_folder):
        shutil.rmtree(audio_folder)
