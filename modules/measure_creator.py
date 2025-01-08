from guitarpro.models import MeasureHeader, Measure, TimeSignature


def calculate_measures(tempo, duration, beats_per_measure=4):
    """
    Рассчитывает количество тактов на основе темпа и длительности трека.

    :param tempo: Темп в BPM
    :param duration: Длительность трека в секундах
    :param beats_per_measure: Количество долей в такте (по умолчанию 4/4)
    :return: Количество тактов
    """
    seconds_per_beat = 60 / tempo
    measure_duration = seconds_per_beat * beats_per_measure
    return int(duration / measure_duration) + 1  # Округляем вверх для точности


def add_measures_to_song(song, num_measures, beats_per_measure=4):
    """
    Добавляет заданное количество тактов в объект песни.

    :param song: Объект Guitar Pro песни
    :param num_measures: Количество тактов
    :param beats_per_measure: Количество долей в такте (по умолчанию 4/4)
    """
    for _ in range(num_measures):
        # Создаем заголовок такта
        header = MeasureHeader()
        header.timeSignature = TimeSignature(beats_per_measure, 4)
        song.addMeasureHeader(header)

        # Добавляем такт для каждой дорожки
        for track in song.tracks:
            measure = Measure(track=track, header=header)
            track.measures.append(measure)
