import os
import logging
import librosa
import numpy as np
from math import ceil
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.easyid3 import EasyID3


class AudioFile:
    def __init__(self, audio_file: str):
        """Инициализация класса AudioFile."""
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Файл {audio_file} не найден.")

        self.audio_file = audio_file
        self.tempo: float = None
        self.duration: float = None
        self.chords = None
        self.measures: int = None

    def detect_tempo(self) -> float:
        """Определяет темп аудиофайла."""
        try:
            y, sr = librosa.load(self.audio_file)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            self.tempo = float(tempo.item()) if isinstance(tempo, np.ndarray) else float(tempo)
            return self.tempo
        except Exception as e:
            logging.error(f"Ошибка при определении темпа: {e}")
            raise

    def detect_duration(self) -> float:
        """Определяет длительность аудиофайла."""
        try:
            y, sr = librosa.load(self.audio_file)
            self.duration = librosa.get_duration(y=y, sr=sr)
            return self.duration
        except Exception as e:
            logging.error(f"Ошибка при определении длительности: {e}")
            raise

    def format_duration(self) -> str:
        """Форматирует длительность в MM:SS."""
        if self.duration is None:
            raise ValueError("Длительность не определена.")
        minutes, seconds = divmod(int(self.duration), 60)
        return f"{minutes:02}:{seconds:02}"

    def calculate_measures(self, beats_per_measure: int = 4) -> int:
        """Вычисляет количество тактов в аудиофайле."""
        if self.tempo is None or self.duration is None:
            raise ValueError("Темп и/или длительность не определены.")
        try:
            duration_of_one_measure = 60 / self.tempo * beats_per_measure
            self.measures = ceil(self.duration / duration_of_one_measure)
            return self.measures
        except Exception as e:
            logging.error(f"Ошибка при вычислении количества тактов: {e}")
            raise

    def get_metadata(self):
        """Получает имя файла и метаданные (исполнитель, альбом, название трека)."""
        filename = os.path.basename(self.audio_file)  # Имя файла без пути
        metadata = {"filename": filename, "title": filename, "artist": "Unknown", "album": "Unknown"}

        if self.audio_file.endswith(".mp3"):
            try:
                audio = MP3(self.audio_file, ID3=EasyID3)
                metadata["title"] = audio.get("title", [filename])[0]
                metadata["artist"] = audio.get("artist", ["Unknown"])[0]
                metadata["album"] = audio.get("album", ["Unknown"])[0]
            except Exception as e:
                logging.warning(f"Не удалось получить метаданные MP3: {e}")

        elif self.audio_file.endswith(".wav"):
            try:
                audio = WAVE(self.audio_file)  # Загружаем WAV-файл
                metadata["title"] = filename  # WAV не хранит теги, используем имя файла
                metadata["sample_rate"] = audio.info.sample_rate  # Частота дискретизации (например, 44100 Hz)
                metadata["channels"] = audio.info.channels  # Количество каналов (моно/стерео)
                metadata["bits_per_sample"] = audio.info.bits_per_sample  # Глубина (16-bit, 24-bit)
            except Exception as e:
                logging.warning(f"Не удалось получить информацию о WAV: {e}")

        return metadata
