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

    # Сохраняем файл
    output_file_path = 'output/chords_track.gp5'
    gp_creator.create_file(output_file_path)
    print(f"Файл сохранён: {output_file_path}")


if __name__ == "__main__":
    main()
