import librosa
import librosa.display


def detect_chords(audio_file):
    """
    Определяет аккорды из аудиофайла.

    :param audio_file: Путь к аудиофайлу
    :return: Список аккордов
    """
    try:
        y, sr = librosa.load(audio_file)
        # Примерный способ определения аккордов (используйте более точные методы в реальности)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        # Здесь можно добавить более сложный алгоритм для определения аккордов
        chords = chroma.argmax(axis=0)  # Просто пример
        return chords
    except Exception as e:
        print(f"Ошибка при определении аккордов: {e}")
        return []
