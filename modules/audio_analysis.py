import librosa
import librosa.display
import numpy as np
from math import ceil


class AudioFile:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.tempo = None
        self.duration = None
        self.chords = None
        self.measures = None

    def detect_tempo(self):
        """
        Определяет темп (BPM) аудиофайла.

        :return: Темп в BPM
        """
        try:
            # Загрузка аудиофайла
            y, sr = librosa.load(self.audio_file)

            # Определение темпа
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

            # Если tempo — массив, извлечь первое значение
            if isinstance(tempo, (list, tuple, np.ndarray)):
                tempo = tempo.item()  # Извлекаем скалярное значение

            self.tempo = tempo
            return tempo
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return None

    def detect_duration(self):
        """
        Определяет длительность аудиофайла в секундах.

        :return: Длительность в секундах
        """
        try:
            # Загрузка аудиофайла
            y, sr = librosa.load(self.audio_file)

            # Вычисление длительности
            self.duration = librosa.get_duration(y=y, sr=sr)
            return self.duration
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return None

    def format_duration(self):
        """
        Представляет длительность в формате 'минуты:секунды'.

        :return: Строка в формате 'MM:SS'
        """
        if self.duration is None:
            raise ValueError("Длительность не определена.")

        # Преобразуем длительность в минуты и секунды
        minutes, seconds = divmod(int(self.duration), 60)
        return f"{minutes:02}:{seconds:02}"

    def calculate_measures(self):
        """
        Вычисляет количество тактов, основываясь на длительности трека и темпе.

        :return: Количество тактов
        """
        try:
            if self.tempo is None or self.duration is None:
                raise ValueError("Темп и/или длительность не определены.")

            # Длительность одного такта в секундах (для стандартного метра 4/4)
            duration_of_one_measure = 60 / self.tempo * 4  # Метро 4/4, т.е. 4 доли в такте

            # Рассчитываем количество тактов
            self.measures = ceil(self.duration / duration_of_one_measure)
            return self.measures
        except Exception as e:
            print(f"Ошибка при вычислении количества тактов: {e}")
            return None
