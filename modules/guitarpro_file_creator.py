import guitarpro
from guitarpro.models import Song, Track, Measure, MeasureHeader
from unidecode import unidecode
import re


class GuitarProFileCreator:
    def __init__(self, tempo, title="MySong", artist="Unknown", album="Unknown", words="", copyright="", tab="Unknown",
                 instructions=""):
        """
        Инициализация класса для создания файла Guitar Pro.
        :param tempo: Темп для песни.
        :param title: Название песни.
        :param artist: Исполнитель песни.
        :param album: Альбом.
        :param words: Текст песни.
        :param copyright: Копирайт.
        :param tab: Автор табулатуры.
        :param instructions: Инструкции.
        """
        self.song = Song()
        self.song.tempo = tempo
        self.song.title = self.clean_string(title)
        self.song.artist = self.clean_string(artist)
        self.song.album = self.clean_string(album)
        self.song.words = self.clean_string(words)
        self.song.copyright = self.clean_string(copyright)
        self.song.tab = self.clean_string(tab)
        self.song.instructions = self.clean_string(instructions)

        # Удаляем стандартную дорожку (если она есть)
        if self.song.tracks:
            self.song.tracks.clear()

        # Создаём основной трек
        self.track = Track(self.song)
        self.song.tracks.append(self.track)

    def clean_string(self, input_string: str) -> str:
        """
        Очистка строки от символов, которые не могут быть закодированы в используемой кодировке.
        :param input_string: Строка для очистки.
        :return: Очищенная строка.
        """
        input_string = input_string or "Unknown"  # Если строка пуста, ставим значение "Unknown"
        input_string = self.remove_invalid_characters(input_string)  # Удаление невалидных символов
        input_string = unidecode(input_string)  # Транслитерация символов
        return input_string

    def remove_invalid_characters(self, input_string: str) -> str:
        """
        Удаляет символы, не поддерживаемые ASCII (или те, что не входят в допустимый набор).
        :param input_string: Строка для очистки.
        :return: Очищенная строка.
        """
        # Удаляет все символы, кроме латинских букв, цифр и пробелов
        return re.sub(r'[^a-zA-Z0-9 ]+', '', input_string)

    def set_track_name(self, name):
        """
        Устанавливает имя дорожки.
        :param name: Имя дорожки.
        """
        self.track.name = name

    def create_file(self, file_path):
        """
        Создаёт файл Guitar Pro с заданным треком.
        """
        try:
            guitarpro.write(self.song, file_path)
            print(f"Файл Guitar Pro успешно создан: {file_path}")
        except Exception as e:
            print(f"Ошибка при создании файла Guitar Pro: {e}")

    def add_measures(self, measure_count: int):
        """
        Добавляет заданное количество тактов в дорожку.
        :param measure_count: Количество добавляемых тактов.
        """
        for _ in range(measure_count - 1):  # так как GuitarPro содержит первый такт по умолчанию, отнимем один такт.
            measure = Measure(self.track, MeasureHeader())  # Создаем новый такт
            self.track.measures.append(measure)  # Добавляем такт в дорожку

    def add_instrument(self, instrument):
        """
        Добавляет инструмент в дорожку.
        :param instrument: Инструмент для добавления в дорожку.
        """
        self.track.instrument = instrument
        print(f"Инструмент для дорожки установлен: {instrument}")

