import librosa
import librosa.display
import numpy as np
from math import ceil
import os
import logging

class AudioFile:
    def __init__(self, audio_file: str):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Файл {audio_file} не найден.")
        self.audio_file = audio_file
        self.tempo: float = None
        self.duration: float = None
        self.chords = None
        self.measures: int = None

    def detect_tempo(self) -> float:
        try:
            y, sr = librosa.load(self.audio_file)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            self.tempo = float(tempo)
            return self.tempo
        except Exception as e:
            logging.error(f"Ошибка при определении темпа: {e}")
            raise

    def detect_duration(self) -> float:
        try:
            y, sr = librosa.load(self.audio_file)
            self.duration = librosa.get_duration(y=y, sr=sr)
            return self.duration
        except Exception as e:
            logging.error(f"Ошибка при определении длительности: {e}")
            raise

    def format_duration(self) -> str:
        if self.duration is None:
            raise ValueError("Длительность не определена.")
        minutes, seconds = divmod(int(self.duration), 60)
        return f"{minutes:02}:{seconds:02}"

    def calculate_measures(self, beats_per_measure: int = 4) -> int:
        if self.tempo is None or self.duration is None:
            raise ValueError("Темп и/или длительность не определены.")
        try:
            duration_of_one_measure = 60 / self.tempo * beats_per_measure
            self.measures = ceil(self.duration / duration_of_one_measure)
            return self.measures
        except Exception as e:
            logging.error(f"Ошибка при вычислении количества тактов: {e}")
            raise
