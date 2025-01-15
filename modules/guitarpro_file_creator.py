import guitarpro
from guitarpro.models import Song, Track


class GuitarProFileCreator:
    def __init__(self, tempo):
        self.tempo = tempo
        self.song = Song()
        self.song.tempo = tempo

        # Удаляем стандартную дорожку (если она есть)
        if self.song.tracks:
            self.song.tracks.clear()

        # Создаём трек и добавляем его в песню
        self.track = Track(self.song)
        self.song.tracks.append(self.track)

    def set_track_name(self, name):
        """
        Устанавливает имя дорожки.

        :param name: Имя дорожки
        """
        self.track.name = name

    def create_file(self, file_path):
        """
        Создаёт файл Guitar Pro с заданным треком.
        """
        try:
            guitarpro.write(self.song, file_path)
            print(f"Файл Guitar Pro успешно создан: {file_path}")
        except Exception as e:
            print(f"Ошибка при создании файла Guitar Pro: {e}")

    @staticmethod
    def add_measures(track: Track, measure_count: int):
        """
        Добавляет заданное количество тактов в дорожку.

        :param track: Дорожка, куда добавляются такты.
        :param measure_count: Количество добавляемых тактов.
        """
        for _ in range(measure_count):
            track.newMeasure()
