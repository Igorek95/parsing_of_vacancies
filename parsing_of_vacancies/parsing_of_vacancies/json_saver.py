import json
from parsing_of_vacancies.parsing_of_vacancies.saver import Saver
from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy


class JSONSaver(Saver):
    """
    Класс для сохранения и загрузки данных о вакансиях в формате JSON.

    Attributes:
        vacancies (list): Список вакансий.
        filename (str): Имя JSON-файла, в который будут сохраняться данные.
    """

    vacancies = []

    def __init__(self, filename):
        """
        Инициализирует объект JSONSaver.

        Args:
            filename (str): Имя JSON-файла, в который будут сохраняться данные.
        """
        self.filename = filename

    def save_to_file(self):
        """
        Сохраняет данные о вакансиях в JSON-файл.

        Записывает данные из списка вакансий в указанный JSON-файл.

        """
        vacancies_data = [vacancy.__dict__ for vacancy in Vacancy._Vacancy__data]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        """
        Загружает данные о вакансиях из JSON-файла.

        Загружает данные из указанного JSON-файла и сохраняет их в переменной класса vacancies.

        """
        with open(self.filename, "r", encoding="utf-8") as file:
            JSONSaver.vacancies = json.load(file)

    @staticmethod
    def merge_json_files(first_file_path, second_file_path, output_file_path):
        """
        Объединяет два JSON-файла в один.

        Args:
            first_file_path (str): Путь к первому JSON-файлу.
            second_file_path (str): Путь ко второму JSON-файлу.
            output_file_path (str): Путь к выходному JSON-файлу.

        """
        with open(first_file_path, 'r', encoding="utf-8") as file1:
            data1 = json.load(file1)

        with open(second_file_path, 'r', encoding="utf-8") as file2:
            data2 = json.load(file2)

        result = data1[0:30] + data2[0:30]

        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=4)

    def delete_vacancy(self):
        """
        Удаляет все данные о вакансиях и очищает JSON-файл.

        Удаляет все данные о вакансиях из списка и очищает содержимое JSON-файла.

        """
        self.vacancies.clear()
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)
