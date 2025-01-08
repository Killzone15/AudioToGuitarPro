from modules.tempo_detector import TempoDetector
from modules.guitarpro_file_creator import GuitarProFileCreator


class Main:
    def __init__(self, audio_file, output_file):
        self.audio_file = audio_file
        self.output_file = output_file

    def run(self):
        # Определяем темп
        tempo_detector = TempoDetector(self.audio_file)
        tempo = tempo_detector.detect_tempo()

        if tempo is not None:
            # Создаем файл Guitar Pro с этим темпом
            gp_creator = GuitarProFileCreator(tempo)
            gp_creator.create_file(self.output_file)
        else:
            print("Не удалось определить темп. Файл Guitar Pro не был создан.")


if __name__ == "__main__":
    # Замените пути на ваши
    audio_file = 'audio/Frostpunk Theme.mp3'  # Путь к вашему аудиофайлу
    output_file = 'output/new.gp5'  # Путь для сохранения файла Guitar Pro

    main_program = Main(audio_file, output_file)
    main_program.run()
