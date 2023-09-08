from abc import ABC, abstractmethod


class JobAPI(ABC):
    """
    Абстрактный класс для взаимодействия с API по получению информации о вакансиях.

    """

    @abstractmethod
    def get_vacancies(self, search_query):
        """
        Абстрактный метод для получения списка вакансий.

        """
        pass
