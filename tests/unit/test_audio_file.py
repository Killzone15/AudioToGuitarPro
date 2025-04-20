import shutil
import unittest
import os
import logging
from pydub.generators import Square
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from app.core.audio_analysis import AudioFile

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class TestAudioFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_audio_file = 'audio/test_audio.mp3'
        pulse = Square(440).to_audio_segment(duration=200).set_frame_rate(44100) * 5
        os.makedirs(os.path.dirname(cls.test_audio_file), exist_ok=True)

        # Сохраняем аудиофайл
        with open(cls.test_audio_file, 'wb') as f:
            pulse.export(f, format="mp3")
        logger.info(f"Тестовый аудиофайл создан: {cls.test_audio_file}")

        # Добавляем метаданные
        audio_file = MP3(cls.test_audio_file, ID3=ID3)
        audio_file.tags = ID3()  # Инициализируем ID3 теги, если они еще не установлены

        # Добавление тега названия (TIT2)
        audio_file.tags.add(TIT2(encoding=3, text="Test Track"))

        # Добавление тега исполнителя (TPE1)
        audio_file.tags.add(TPE1(encoding=3, text="Test Artist"))

        # Добавление тега альбома (TALB)
        audio_file.tags.add(TALB(encoding=3, text="Test Album"))

        # Сохраняем изменения в файле
        audio_file.save()
        logger.info("Метаданные добавлены в тестовый аудиофайл.")

    def test_detect_tempo(self):
        """
        Проверяем определение темпа
        """
        audio = AudioFile(self.test_audio_file)
        tempo = audio.detect_tempo()
        logger.info(f"Темп: {tempo} BPM")
        self.assertIsNotNone(tempo, "Темп должен быть определён.")
        self.assertGreater(tempo, 0, "Темп должен быть положительным числом.")

    def test_detect_duration(self):
        """
        Проверяем определение длительности трека
        """
        audio = AudioFile(self.test_audio_file)
        duration = audio.detect_duration()
        logger.info(f"Длительность: {duration} секунд")
        self.assertIsNotNone(duration, "Длительность должна быть определена.")
        self.assertGreater(duration, 0, "Длительность должна быть положительным числом.")

    def test_calculate_measures(self):
        """
        Проверяем вычисления кол-ва тактов
        """
        audio = AudioFile(self.test_audio_file)
        tempo = audio.detect_tempo()  # Получаем темп
        duration = audio.detect_duration()  # Получаем длительность
        measures = audio.calculate_measures()
        logger.info(f"Темп: {tempo}, Длительность: {duration}, Количество тактов: {measures}")

        self.assertIsNotNone(measures, "Количество тактов должно быть вычислено.")
        self.assertGreater(measures, 0, "Количество тактов должно быть положительным числом.")

    def test_get_metadata(self):
        """
        Проверяем мета-данные из аудио
        """
        audio = AudioFile(self.test_audio_file)
        metadata = audio.get_metadata()
        logger.info(f"Метаданные: {metadata}")

        self.assertIn("filename", metadata, "Имя файла должно быть в метаданных.")
        self.assertIn("title", metadata, "Название трека должно быть в метаданных.")
        self.assertIn("artist", metadata, "Исполнитель должен быть в метаданных.")
        self.assertIn("album", metadata, "Альбом должен быть в метаданных.")
        self.assertEqual(metadata["title"], "Test Track", "Название трека должно быть 'Test Track'.")
        self.assertEqual(metadata["artist"], "Test Artist", "Исполнитель должен быть 'Test Artist'.")
        self.assertEqual(metadata["album"], "Test Album", "Альбом должен быть 'Test Album'.")

    @classmethod
    def tearDownClass(cls):
        # Удаление файла
        if os.path.exists(cls.test_audio_file):
            os.remove(cls.test_audio_file)
            logger.info(f"Тестовый аудиофайл удалён: {cls.test_audio_file}")

        # Удаление папки, если она пустая
        audio_dir = os.path.dirname(cls.test_audio_file)
        if os.path.exists(audio_dir):
            try:
                # Попробуем удалить папку, если она пуста
                os.rmdir(audio_dir)
                logger.info(f"Папка {audio_dir} успешно удалена.")
            except OSError:
                # Если папка не пуста, используем shutil.rmtree для рекурсивного удаления
                shutil.rmtree(audio_dir)
                logger.info(f"Папка {audio_dir} удалена с содержимым.")


if __name__ == '__main__':
    unittest.main()
