class MeasureCalculator:
    def __init__(self, tempo, duration, beats_per_measure=4):
        """
        Инициализация класса для расчёта количества тактов.

        :param tempo: Темп в BPM
        :param duration: Длительность трека в секундах
        :param beats_per_measure: Количество долей в такте (по умолчанию 4)
        """
        self.tempo = tempo
        self.duration = duration
        self.beats_per_measure = beats_per_measure

    def calculate_measures(self):
        """
        Рассчитывает количество тактов на основе темпа, длительности и размера такта.

        :return: Количество тактов
        """
        if self.duration == 0:
            return 1  # Если длительность 0, возвращаем 1 такт

        seconds_per_beat = 60 / self.tempo
        measure_duration = seconds_per_beat * self.beats_per_measure
        measures = self.duration / measure_duration

        # Если есть остаток, добавляем 1 такт
        if measures % 1 > 0:
            return int(measures) + 1
        return int(measures)

