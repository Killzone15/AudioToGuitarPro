from modules.audio_analysis import AudioFile


def main():
    # Путь к аудиофайлу
    audio_path = 'audio/Frostpunk Theme.mp3'

    # Создание объекта AudioFile
    audio = AudioFile(audio_path)

    # Получение темпа
    tempo = audio.detect_tempo()
    print(f"Темп: {tempo} BPM")

    audio.detect_duration()
    # Получение длительности в формате 'минуты:секунды'
    formatted_duration = audio.format_duration()
    print(f"Длительность: {formatted_duration}")

    # Получение кол-ва тактов
    measures = audio.calculate_measures()
    print(f"Количество тактов: {measures}")


if __name__ == "__main__":
    main()
