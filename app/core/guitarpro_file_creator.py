import guitarpro
from guitarpro.models import Song, Track, Measure, MeasureHeader
from unidecode import unidecode
import re
import os


def transliterate_text(text):
    """Переводит кириллический текст в латиницу."""
    return unidecode(text) if text else "Unknown"


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
        self.song.title = transliterate_text(title)
        self.song.artist = transliterate_text(artist)
        self.song.album = transliterate_text(album)
        self.song.words = transliterate_text(words)
        self.song.copyright = transliterate_text(copyright)
        self.song.tab = transliterate_text(tab)
        self.song.instructions = transliterate_text(instructions)

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
        input_string = unidecode(input_string)  # Транслитерация символов (кириллица -> латиница)
        return input_string

    def remove_invalid_characters(self, input_string: str) -> str:
        """
        Удаляет символы, не поддерживаемые ASCII (или те, что не входят в допустимый набор).
        :param input_string: Строка для очистки.
        :return: Очищенная строка.
        """
        return re.sub(r'[^a-zA-Z0-9 _-]+', '', input_string)  # Оставляем латиницу, цифры, пробелы, "-", "_"

    def set_track_name(self, name):
        """
        Устанавливает имя дорожки.
        :param name: Имя дорожки.
        """
        self.track.name = self.clean_string(name)  # Применяем очистку строки

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

    def generate_filename(self, audio_filename):
        """
        Генерирует имя файла Guitar Pro, очищая его от кириллицы и запрещённых символов.
        :param audio_filename: Имя оригинального аудиофайла.
        :return: Очищенное имя файла Guitar Pro.
        """
        base_name = os.path.splitext(os.path.basename(audio_filename))[0]  # Убираем путь и расширение
        cleaned_name = self.clean_string(base_name)  # Очищаем от кириллицы
        return f"{cleaned_name}.gp5"  # Возвращаем имя файла с расширением

    def add_instrument(self, instrument):
        """
        Добавляет инструмент в дорожку.
        :param instrument: Инструмент для добавления в дорожку.
        """
        self.track.instrument = instrument
        print(f"Инструмент для дорожки установлен: {instrument}")
