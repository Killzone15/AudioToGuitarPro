import os
from unidecode import unidecode
from src.audiotoguitarpro.audio_analysis import AudioFile
from src.audiotoguitarpro.guitarpro_file_creator import GuitarProFileCreator


def get_transliterated_filename(audio_path):
    """Возвращает имя файла без расширения, транслитерируя кириллицу в латиницу."""
    base_name = os.path.splitext(os.path.basename(audio_path))[0]  # Получаем имя файла без расширения
    return unidecode(base_name)  # Транслитерация


def main():
    # Путь к аудиофайлу
    audio_path = 'audio/Frostpunk Theme.mp3'

    # Создание объекта AudioFile
    audio = AudioFile(audio_path)

    # Получение темпа
    tempo = audio.detect_tempo()
    print(f"Темп: {tempo} BPM")

    # Определение длительности
    audio.detect_duration()
    formatted_duration = audio.format_duration()
    print(f"Длительность: {formatted_duration}")

    # Получение количества тактов
    measures = audio.calculate_measures()
    print(f"Количество тактов: {measures}")

    # Получение метаданных
    metadata = audio.get_metadata()
    print(f"Метаданные: {metadata}")

    # Создание файла Guitar Pro с метаданными
    track_name = "Chords"
    gp_creator = GuitarProFileCreator(
        tempo=tempo,
        title=metadata.get("title"),
        artist=metadata.get("artist"),
        album=metadata.get("album")
    )

    gp_creator.set_track_name(track_name)  # Устанавливаем имя дорожки

    # Добавляем нужное количество тактов
    gp_creator.add_measures(measures)

    # Формируем корректное имя файла
    output_dir = 'output/'
    file_name = get_transliterated_filename(audio_path) + '.gp5'
    output_file_path = os.path.join(output_dir, file_name)

    # Проверка существования директории
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Сохраняем файл
        gp_creator.create_file(output_file_path)
        print(f"Файл сохранён: {output_file_path}")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


if __name__ == "__main__":
    main()
