import pprint
import requests
from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy
from parsing_of_vacancies.parsing_of_vacancies.job_api import JobAPI
from parsing_of_vacancies.parsing_of_vacancies.json_saver import JSONSaver


class HeadHunterAPI(JobAPI):
    """
    Класс для взаимодействия с API HeadHunter и получения информации о вакансиях.

    Attributes:
        base_url (str): Базовый URL для запросов к API HeadHunter.
    """

    def __init__(self):
        """
        Инициализирует объект HeadHunterAPI и устанавливает базовый URL API HeadHunter.

        """
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query=''):
        """
        Получает список вакансий с использованием API HeadHunter.

        Args:
            search_query (str, optional): Поисковый запрос для фильтрации вакансий. По умолчанию пустая строка.

        """
        params = {
            "area": 1,
            'per_page': 40,
            'host': 'hh.ru'
        }
        if search_query:
            params['text'] = search_query
        response = requests.get(self.base_url, params)
        if response.status_code == 200:
            data = response.json()
            response.close()
            vacancies = data.get("items", [])
            self.data_vacancies(vacancies)
        else:
            print("Ошибка получения данных")
            return []

    @staticmethod
    def data_vacancies(vacancies):
        """
        Обрабатывает данные о вакансиях и создает объекты класса Vacancy.

        Args:
            vacancies (list): Список данных о вакансиях, полученных из API HeadHunter.
        """
        for vacancy in vacancies:
            name_job = vacancy.get('name')
            if vacancy.get('salary'):
                salary_from = vacancy['salary'].get('from')
                salary_to = vacancy['salary'].get('to')
                currency = vacancy['salary'].get('currency')
            else:
                salary_from = 0
                salary_to = 0
                currency = ""
            link = vacancy.get('alternate_url', 'Не указана')
            address = vacancy['area'].get('name')
            responsibilities = vacancy['snippet'].get('requirement')
            Vacancy(name_job, salary_from, salary_to, currency, link, address, responsibilities)
