import guitarpro
from guitarpro.models import Song, Track


class GuitarProFileCreator:
    def __init__(self, tempo):
        self.tempo = tempo
        self.song = Song()
        self.song.tempo = tempo
        self.track = Track(self.song)

    def create_file(self, file_path):
        """
        Создает файл Guitar Pro с заданным темпом.

        :param file_path: Путь для сохранения файла .gp5
        """
        try:
            # Сохранение файла Guitar Pro
            guitarpro.write(self.song, file_path)
            print(f"Файл Guitar Pro успешно создан: {file_path}")
        except Exception as e:
            print(f"Ошибка при создании файла Guitar Pro: {e}")


