from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query):
        params = {
            "text": search_query,
            'area': 'Russia',
        }
        headers = {
            'User_Agent': 'Your User Agent',
            'Authorization': f"Bearer {self.api_key}"
        }
        response = requests.get(self.base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            vacancies = data.get('items', [])
            return vacancies
        else:
            print('Ошибка при получение вакансии')
            return []


class SuperJobAPI(JobAPI):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.superjob.ru/2.0/vacancies"

    def get_vacancies(self, search_query):
        headers = {
            "User-Agent": "Your User Agent",
            "X-Api-App-Id": self.api_key,
        }
        params = {
            "town": "Москва",
            "keyword": search_query,
        }

        response = requests.get(self.base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("objects", [])
            return vacancies
        else:
            print("Ошибка при получении вакансий.")
            return []
