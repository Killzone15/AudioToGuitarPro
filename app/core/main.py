from app.core.audio_analysis import AudioFile
from app.core.guitarpro_file_creator import GuitarProFileCreator
from app.core.file_utils import FileUtils



'''Main function'''
def process_audio_file(audio_path):

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

    # Устанавливаем имя дорожки
    gp_creator.set_track_name(track_name)

    # Добавляем нужное количество тактов
    gp_creator.add_measures(measures)

    file_utils = FileUtils(audio_path=audio_path, directory='output/')
    output_file_path = file_utils.prepare_output_path()
    print("Путь к файлу:" + output_file_path)


    try:
        # Сохраняем файл
        gp_creator.create_file(output_file_path)
        print(f"Файл сохранён: {output_file_path}")
        return output_file_path
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return None
