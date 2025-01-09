import unittest
from modules.measure_calculator import MeasureCalculator


class TestMeasureCalculator(unittest.TestCase):
    def test_calculate_measures_default(self):
        """
        Тестирует расчёт количества тактов с размером такта 4/4.
        """
        tempo = 120  # Темп в BPM
        duration = 60  # Длительность трека в секундах
        calculator = MeasureCalculator(tempo, duration)

        measures = calculator.calculate_measures()
        self.assertEqual(measures, 30, "Количество тактов для 4/4 размера должно быть 30.")

    def test_calculate_measures_custom(self):
        """
        Тестирует расчёт количества тактов с изменённым размером такта.
        """
        tempo = 100  # Темп в BPM
        duration = 90  # Длительность трека в секундах
        beats_per_measure = 3  # Размер такта 3/4
        calculator = MeasureCalculator(tempo, duration, beats_per_measure)

        measures = calculator.calculate_measures()
        expected_measures = int(duration / (60 / tempo * beats_per_measure)) + 1
        self.assertEqual(measures, expected_measures, "Количество тактов для 3/4 размера должно совпадать с расчётом.")

    def test_zero_duration(self):
        """
        Тестирует поведение при длительности трека равной 0.
        """
        tempo = 120
        duration = 0
        calculator = MeasureCalculator(tempo, duration)

        measures = calculator.calculate_measures()
        self.assertEqual(measures, 1, "При длительности 0 должен возвращаться 1 такт.")

    def test_low_tempo(self):
        """
        Тестирует поведение при низком темпе.
        """
        tempo = 20  # Темп в BPM
        duration = 120  # Длительность трека в секундах
        calculator = MeasureCalculator(tempo, duration)

        measures = calculator.calculate_measures()
        self.assertGreater(measures, 0, "При низком темпе количество тактов должно быть положительным.")


if __name__ == "__main__":
    unittest.main()
