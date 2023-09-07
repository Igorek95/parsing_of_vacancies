import json

from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy
from abc import ABC, abstractmethod


class Saver(ABC):
    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONSaver(Saver):
    vacancies = []

    def __init__(self, filename):
        self.filename = filename

    def save_to_file(self):
        vacancies_data = [vacancy.__dict__ for vacancy in Vacancy._Vacancy__data]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            JSONSaver.vacancies = json.load(file)

    @staticmethod
    def merge_json_files(first_file_path, second_file_path, output_file_path):
        with open(first_file_path, 'r', encoding="utf-8") as file1:
            data1 = json.load(file1)

        with open(second_file_path, 'r', encoding="utf-8") as file2:
            data2 = json.load(file2)

        result = data1 + data2

        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=4)

    def delete_vacancy(self):
        self.vacancies.clear()
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)
