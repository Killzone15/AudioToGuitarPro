import librosa
import librosa.display
import numpy as np


class AudioFile:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.tempo = None
        self.duration = None
        self.chords = None

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
