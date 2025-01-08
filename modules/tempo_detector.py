import os
import librosa
import numpy as np


class TempoDetector:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.tempo = None

    def detect_tempo(self):
        """
        Определяет темп (BPM) аудиофайла.

        :param audio_file: Путь к аудиофайлу
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
