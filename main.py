import os
from modules.audio_analysis import AudioFile
from modules.guitarpro_file_creator import GuitarProFileCreator


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

    # Создание файла Guitar Pro
    track_name = "Chords"  # Здесь можно задать любое имя трека
    gp_creator = GuitarProFileCreator(tempo)
    gp_creator.set_track_name(track_name)  # Устанавливаем имя дорожки

    # Путь к директории и файлу для сохранения
    output_dir = 'output/'
    output_file_path = os.path.join(output_dir, 'chords_track.gp5')

    # Проверка существования директории, создание, если необходимо
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
