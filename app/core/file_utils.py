# file_utils.py
import os
import time
import shutil
from unidecode import unidecode

class FileUtils:
    def __init__(self, audio_path=None, directory=None):
        self.audio_path = audio_path
        self.directory = directory

    def ensure_directory_exists(self):
        """Проверяет существование директории, если нет - создает её."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_transliterated_filename(self):
        """Возвращает имя файла без расширения, транслитерируя кириллицу в латиницу."""
        base_name = os.path.splitext(os.path.basename(self.audio_path))[0]  # Получаем имя файла без расширения
        return unidecode(base_name)  # Транслитерация

    def remove_old_files(self, max_age=600):
        """Удаляет файлы старше max_age секунд (по умолчанию 10 минут)."""
        current_time = time.time()

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)

            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)  # Время последней модификации
                if file_age > max_age:
                    try:
                        os.remove(file_path)
                        print(f"Файл {filename} удалён, так как он старше {max_age} секунд.")
                    except Exception as e:
                        print(f"Ошибка при удалении файла {filename}: {e}")

    def remove_audio_file_after_analysis(self, filename, audio_folder):
        """Удаляет аудиофайл пользователя с сервера после его аудио-анализа"""
        file_path = os.path.join(audio_folder, filename)
        os.remove(file_path)
        print(f"Файл {filename} успешно удалён")

        # Если папка пуста, удаляем её
        if not os.listdir(audio_folder):
            shutil.rmtree(audio_folder)

    def check_file_exists(self, file_path):
        """Проверяет существование файла."""
        return os.path.exists(file_path)

    def prepare_output_path(self, extension='.gp5'):
        """
        Проверяет наличие директории, формирует путь к выходному файлу
        с транслитерированным именем и нужным расширением.
        """
        self.ensure_directory_exists()

        file_name = self.get_transliterated_filename() + extension
        output_file_path = os.path.join(self.directory, file_name)

        return output_file_path
