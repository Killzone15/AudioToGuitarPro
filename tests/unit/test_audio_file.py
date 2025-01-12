import unittest
import os
import logging
from pydub.generators import Square
from modules.audio_analysis import AudioFile

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class TestAudioFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_audio_file = 'audio/test_audio.mp3'
        pulse = Square(440).to_audio_segment(duration=200).set_frame_rate(44100) * 5
        os.makedirs(os.path.dirname(cls.test_audio_file), exist_ok=True)
        with open(cls.test_audio_file, 'wb') as f:
            pulse.export(f, format="mp3")
        logger.info(f"Тестовый аудиофайл создан: {cls.test_audio_file}")

    def test_detect_tempo(self):
        audio = AudioFile(self.test_audio_file)
        tempo = audio.detect_tempo()
        logger.info(f"Темп: {tempo} BPM")
        self.assertIsNotNone(tempo, "Темп должен быть определён.")
        self.assertGreater(tempo, 0, "Темп должен быть положительным числом.")

    def test_detect_duration(self):
        audio = AudioFile(self.test_audio_file)
        duration = audio.detect_duration()
        logger.info(f"Длительность: {duration} секунд")
        self.assertIsNotNone(duration, "Длительность должна быть определена.")
        self.assertGreater(duration, 0, "Длительность должна быть положительным числом.")

    def test_calculate_measures(self):
        audio = AudioFile(self.test_audio_file)
        audio.detect_tempo()  # Получаем темп
        audio.detect_duration()  # Получаем длительность
        measures = audio.calculate_measures()
        logger.info(f"Количество тактов: {measures} тактов")

        self.assertIsNotNone(measures, "Количество тактов должно быть вычислено.")
        self.assertGreater(measures, 0, "Количество тактов должно быть положительным числом.")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_audio_file):
            os.remove(cls.test_audio_file)
        logger.info(f"Тестовый аудиофайл удалён: {cls.test_audio_file}")


if __name__ == '__main__':
    unittest.main()
