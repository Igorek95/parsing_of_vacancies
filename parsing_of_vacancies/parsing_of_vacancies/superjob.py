import requests
from parsing_of_vacancies.parsing_of_vacancies.api_superjob import api_key
from parsing_of_vacancies.parsing_of_vacancies.job_api import JobAPI
from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy


class SuperJobAPI(JobAPI):
    superjob_api_key = api_key

    def __init__(self):
        self.base_url = "https://api.superjob.ru/2.0/vacancies"

    def get_vacancies(self, search_query):
        headers = {
            "User-Agent": "Your User Agent",
            "X-Api-App-Id": self.superjob_api_key,
        }
        params = {
            "town": "Москва",
            "keyword": search_query,
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
        for vacancy in vacancies:
            name_job = vacancy.get('profession')
            salary_from = vacancy.get('payment_from', 'Не указана')
            salary_to = vacancy.get('payment_to', "Не указана")
            currency = vacancy.get('currency', 'Не указана')
            link = vacancy.get('link', 'Не указана')
            address = vacancy['town'].get('title')
            responsibilities = vacancy.get('candidat')
            Vacancy(name_job, salary_from, salary_to, currency, link, address, responsibilities)

#
# sj = SuperJobAPI()
# user_input = input("Введите ваше запрос: ")
# vacancies = sj.get_vacancies(user_input)
# print(Vacancy.data)