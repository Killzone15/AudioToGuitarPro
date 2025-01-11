import guitarpro
from guitarpro.models import Song, Track


class GuitarProFileCreator:
    def __init__(self, tempo):
        self.tempo = tempo
        self.song = Song()
        self.song.tempo = tempo
        self.track = Track(self.song)  # Track создается здесь

    def create_file(self, file_path):
        """
        Создает файл Guitar Pro с заданным темпом.
        """
        try:
            print("Атрибуты дорожки перед сохранением:", vars(self.track))  # Выводим атрибуты
            guitarpro.write(self.song, file_path)
            print(f"Файл Guitar Pro успешно создан: {file_path}")
        except Exception as e:
            print(f"Ошибка при создании файла Guitar Pro: {e}")

    @staticmethod
    def add_measures(track: Track, measure_count: int):
        for _ in range(measure_count):
            track.newMeasure()

