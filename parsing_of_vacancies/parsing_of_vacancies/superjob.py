import requests
from parsing_of_vacancies.parsing_of_vacancies.api_superjob import api_key
from parsing_of_vacancies.parsing_of_vacancies.job_api import JobAPI
from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy


class SuperJobAPI(JobAPI):
    """
    Класс для взаимодействия с API SuperJob и получения информации о вакансиях.

    Attributes:
        superjob_api_key (str): Ключ API SuperJob.
        base_url (str): Базовый URL для запросов к API SuperJob.
    """

    superjob_api_key = api_key

    def __init__(self):
        """
        Инициализирует объект SuperJobAPI и устанавливает базовый URL API SuperJob.
        """
        self.base_url = "https://api.superjob.ru/2.0/vacancies"

    def get_vacancies(self, search_query):
        """
        Получает список вакансий с использованием API SuperJob.

        Args:
            search_query (str): Поисковый запрос для фильтрации вакансий.
        """
        headers = {
            "User-Agent": "Your User Agent",
            "X-Api-App-Id": self.superjob_api_key,
        }
        params = {
            "town": "Москва",
            "keyword": search_query,
            "count": 100
        }

        response = requests.get(self.base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            response.close()
            vacancies = data.get("objects", [])
            self.data_vacancies(vacancies)
        else:
            print("Произошла ошибка при получении вакансий.")
            return []

    @staticmethod
    def data_vacancies(vacancies):
        """
        Обрабатывает данные о вакансиях и создает объекты класса Vacancy.

        Args:
            vacancies (list): Список данных о вакансиях, полученных из API SuperJob.
        """
        for vacancy in vacancies:
            name_job = vacancy.get('profession')
            salary_from = vacancy.get('payment_from', 'Не указана')
            salary_to = vacancy.get('payment_to', "Не указана")
            currency = vacancy.get('currency', 'Не указана')
            link = vacancy.get('link', 'Не указана')
            address = vacancy['town'].get('title')
            responsibilities = vacancy.get('candidat')
            Vacancy(name_job, salary_from, salary_to, currency, link, address, responsibilities)
