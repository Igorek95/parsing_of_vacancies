from abc import ABC, abstractmethod
class JobAPI(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, search_query):
        pass

