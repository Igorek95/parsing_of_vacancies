import pprint

import requests
from parsing_of_vacancies.parsing_of_vacancies.vacancy import Vacancy
from parsing_of_vacancies.parsing_of_vacancies.job_api import JobAPI
from parsing_of_vacancies.parsing_of_vacancies.json_saver import JSONSaver


class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query=''):
        params = {
            "area": 1,
            'per_page': 30,
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
        for vacancy in vacancies:
            name_job = vacancy.get('name')
            if vacancy.get('salary'):
                salary_from = vacancy['salary'].get('from', "Не указана")
                salary_to = vacancy['salary'].get('to', "Не указана")
                currency = vacancy['salary'].get('currency', "")
            link = vacancy.get('alternate_url', 'Не указана')
            address = vacancy['area'].get('name')
            responsibilities = vacancy['snippet'].get('requirement')
            Vacancy(name_job, salary_from, salary_to, currency, link, address, responsibilities)


# hh = HeadHunterAPI()
# appa = hh.get_vacancies('python')
# json_saver = JSONSaver('Axaxa')
# json_saver.save_to_file()
# pprint.pprint(json_saver.get_vacancies_by_salary(110000))
# json_saver.delete_vacancy()
# pprint.pprint(hh.get_vacancies('python'))