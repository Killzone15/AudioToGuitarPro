import unittest
import os
from pydub.generators import Square
from modules.tempo_detector import TempoDetector


class TestTempoDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_audio_file = 'audio/test_audio.mp3'  # Путь к файлу
        # Генерируем аудио с ритмом
        pulse = Square(440).to_audio_segment(duration=200).set_frame_rate(44100) * 5
        os.makedirs(os.path.dirname(cls.test_audio_file), exist_ok=True)
        with open(cls.test_audio_file, 'wb') as f:
            pulse.export(f, format="mp3")
        print(f"Тестовый аудиофайл создан: {cls.test_audio_file}")

    def test_detect_tempo(self):
        detector = TempoDetector(self.test_audio_file)
        tempo = detector.detect_tempo()
        self.assertIsNotNone(tempo, "Темп должен быть определён.")
        self.assertGreater(tempo, 0, "Темп должен быть положительным числом.")
        print(f"Определённый темп: {tempo} BPM")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_audio_file):
            os.remove(cls.test_audio_file)
        print(f"Тестовый аудиофайл удалён: {cls.test_audio_file}")


if __name__ == '__main__':
    unittest.main()
