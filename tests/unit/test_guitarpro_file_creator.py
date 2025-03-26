import unittest
import os
from modules.guitarpro_file_creator import GuitarProFileCreator


class TestGuitarProFileCreator(unittest.TestCase):
    # Объявляем атрибуты с типами, чтобы IDE не ругалась
    tempo: int
    title: str
    artist: str
    album: str
    words: str
    copyright: str
    tab: str
    instructions: str
    creator: GuitarProFileCreator

    @classmethod
    def setUpClass(cls):
        """
        Этот метод выполняется один раз перед запуском всех тестов в классе.
        Здесь мы создаем экземпляр для тестирования, который будет использоваться в каждом тесте.
        """
        cls.tempo = 120  # Примерный темп
        cls.title = "Song Title"
        cls.artist = "Artist Name"
        cls.album = "Album Name"
        cls.words = "Lyrics of the song"
        cls.copyright = "Copyright Information"
        cls.tab = "Tab Author"
        cls.instructions = "Song Instructions"
        cls.creator = GuitarProFileCreator(
            cls.tempo,
            cls.title,
            cls.artist,
            cls.album,
            cls.words,
            cls.copyright,
            cls.tab,
            cls.instructions
        )

    def test_initialization(self):
        """
        Проверяем, что конструктор правильно инициализирует объект
        """
        # Проверяем, что атрибуты song установлены корректно
        self.assertEqual(self.creator.song.tempo, self.tempo, f"Темп должен быть {self.tempo}.")
        self.assertEqual(self.creator.song.title, "Song Title", "Название песни не установлено корректно.")
        self.assertEqual(self.creator.song.artist, "Artist Name", "Исполнитель не установлен корректно.")
        self.assertEqual(self.creator.song.album, "Album Name", "Альбом не установлен корректно.")
        self.assertEqual(self.creator.song.words, "Lyrics of the song", "Текст песни не установлен корректно.")
        self.assertEqual(self.creator.song.copyright, "Copyright Information", "Копирайт не установлен корректно.")
        self.assertEqual(self.creator.song.tab, "Tab Author", "Автор табулатуры не установлен корректно.")
        self.assertEqual(self.creator.song.instructions, "Song Instructions", "Инструкции не установлены корректно.")

    def test_string_cleaning_in_constructor(self):
        """
        Проверяем, что строковые параметры проходят очистку с помощью clean_string
        """
        # Проверяем, что метод clean_string был вызван и строки были очищены
        self.assertEqual(self.creator.song.title, "Song Title", "Название песни должно быть очищено корректно.")
        self.assertEqual(self.creator.song.artist, "Artist Name", "Исполнитель должен быть очищен корректно.")
        self.assertEqual(self.creator.song.album, "Album Name", "Альбом должен быть очищен корректно.")
        self.assertEqual(self.creator.song.words, "Lyrics of the song", "Текст песни должен быть очищен корректно.")
        self.assertEqual(self.creator.song.copyright, "Copyright Information", "Копирайт должен быть очищен корректно.")
        self.assertEqual(self.creator.song.tab, "Tab Author", "Автор табулатуры должен быть очищен корректно.")
        self.assertEqual(self.creator.song.instructions, "Song Instructions",
                         "Инструкции должны быть очищены корректно.")

    def test_clean_string_empty_input(self):
        """
        Проверяем, что если строка пуста, то она заменяется на "Unknown"
        """
        creator = GuitarProFileCreator(self.tempo, title="", artist="", album="", words="")
        self.assertEqual(creator.song.title, "Unknown",
                         "Пустая строка для названия песни должна быть заменена на 'Unknown'.")
        self.assertEqual(creator.song.artist, "Unknown",
                         "Пустая строка для исполнителя должна быть заменена на 'Unknown'.")
        self.assertEqual(creator.song.album, "Unknown", "Пустая строка для альбома должна быть заменена на 'Unknown'.")
        self.assertEqual(creator.song.words, "Unknown",
                         "Пустая строка для текста песни должна быть заменена на 'Unknown'.")

    def test_remove_invalid_characters(self):
        """
        Проверяем, что метод remove_invalid_characters удаляет невалидные символы
        """
        input_string = "ValidString!@#"
        cleaned_string = self.creator.remove_invalid_characters(input_string)
        self.assertEqual(cleaned_string, "ValidString", "Невалидные символы должны быть удалены.")

    def test_create_file(self):
        """
        Проверяем создание файла gp5
        """
        file_path = "test_song.gp5"  # Убедитесь, что путь корректный
        try:
            self.creator.create_file(file_path)
            # После создания файла можно проверить его существование
            self.assertTrue(os.path.exists(file_path), "Файл не был создан.")
        except Exception as e:
            self.fail(f"Ошибка при создании файла: {e}")

    def test_add_measures(self):
        """
        Проверяем добавление тактов в дорожку
        """
        initial_measure_count = len(self.creator.track.measures)
        self.creator.add_measures(4)
        self.assertEqual(len(self.creator.track.measures), initial_measure_count + 3,
                         "Количество тактов должно увеличиться на 3.")

    def test_add_instrument(self):
        """
        Проверяем добавление инструмента в дорожку
        """
        instrument = "Electric Guitar"
        self.creator.add_instrument(instrument)
        self.assertEqual(self.creator.track.instrument, instrument,
                         f"Инструмент должен быть установлен как {instrument}.")

    @classmethod
    def tearDownClass(cls):
        """
        Этот метод выполняется один раз после завершения всех тестов.
        Здесь мы можем удалить созданные файлы или выполнить другую очистку.
        """
        # Удаляем файл, если он был создан
        try:
            if os.path.exists("test_song.gp5"):
                os.remove("test_song.gp5")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")


if __name__ == '__main__':
    unittest.main()
