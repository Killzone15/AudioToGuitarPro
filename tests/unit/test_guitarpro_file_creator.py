import unittest
import os
import shutil
from modules.guitarpro_file_creator import GuitarProFileCreator  # Убедитесь, что путь правильный


class TestGuitarProFileCreator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Выполняется один раз перед всеми тестами.
        Создаем директорию для файлов, если её нет.
        """
        cls.output_dir = "output"
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

    def setUp(self):
        """
        Выполняется перед каждым тестом. Здесь мы создаем экземпляр для тестирования.
        """
        self.tempo = 120  # Примерный темп
        self.creator = GuitarProFileCreator(self.tempo)

    def test_initial_song(self):
        """
        Проверяем, что песня создается с правильным темпом.
        """
        self.assertEqual(self.creator.song.tempo, self.tempo, "Темп не соответствует заданному.")

    def test_set_track_name(self):
        """
        Проверяем, что имя дорожки корректно устанавливается.
        """
        track_name = "Chords"
        self.creator.set_track_name(track_name)
        self.assertEqual(self.creator.track.name, track_name, "Имя дорожки не установлено правильно.")

    def test_add_measures(self):
        """
        Проверяем, что добавление тактов работает корректно.
        """
        measure_count = 5  # Количество тактов
        self.creator.add_measures(measure_count)

        # Ожидаем, что в дорожке будет ровно measure_count тактов
        self.assertEqual(len(self.creator.track.measures), measure_count,
                         f"Должно быть {measure_count} тактов, но найдено {len(self.creator.track.measures)}.")

    def test_create_file(self):
        """
        Проверяем, что файл создается корректно.
        """
        output_path = os.path.join(self.output_dir, "test_track.gp5")

        # Удаляем файл, если он существует
        if os.path.exists(output_path):
            os.remove(output_path)

        # Создаем файл
        self.creator.create_file(output_path)

        # Проверяем, что файл действительно создался
        self.assertTrue(os.path.exists(output_path), f"Файл не был создан по пути {output_path}.")

        # Удаляем файл после теста
        if os.path.exists(output_path):
            os.remove(output_path)

    @classmethod
    def tearDownClass(cls):
        """
        Удаляет созданные директории и файлы после всех тестов.
        """
        if os.path.exists(cls.output_dir):
            try:
                # Попробуем удалить папку, если она пуста
                os.rmdir(cls.output_dir)
                print(f"Папка {cls.output_dir} успешно удалена.")
            except OSError:
                # Если папка не пуста, используем shutil.rmtree для рекурсивного удаления
                shutil.rmtree(cls.output_dir)
                print(f"Папка {cls.output_dir} удалена с содержимым.")


if __name__ == '__main__':
    unittest.main()
