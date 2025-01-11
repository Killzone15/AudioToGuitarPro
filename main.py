from modules.audio_analysis import AudioFile


def main():
    # Путь к аудиофайлу
    audio_path = 'audio/Frostpunk Theme.mp3'

    # Создание объекта AudioFile
    audio = AudioFile(audio_path)

    # Получение темпа
    tempo = audio.detect_tempo()
    print(f"Темп: {tempo} BPM")

    # Получение длительности
    duration = audio.detect_duration()
    print(f"Длительность: {duration} секунд")


if __name__ == "__main__":
    main()
