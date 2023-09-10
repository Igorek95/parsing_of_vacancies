import json


class Vacancy:
    """
    Класс для представления вакансии.

    Attributes:
        name_job (str): Название вакансии.
        salary_from (int): Минимальная зарплата.
        salary_to (int): Максимальная зарплата.
        currency (str): Валюта зарплаты.
        link (str): Ссылка на вакансию.
        address (str): Место работы.
        responsibilities (str): Описание обязанностей.
        __avr_salary (int): Средняя зарплата (вычисляется автоматически).
    """

    __data = []

    def __init__(self, name_job, salary_from, salary_to, currency, link, address, responsibilities):
        """
        Инициализирует объект вакансии.

        Args:
            name_job (str): Название вакансии.
            salary_from (int): Минимальная зарплата.
            salary_to (int): Максимальная зарплата.
            currency (str): Валюта зарплаты.
            link (str): Ссылка на вакансию.
            address (str): Место работы.
            responsibilities (str): Описание обязанностей.
        """
        self.name_job = name_job
        self.salary_from = salary_from if salary_from else 0
        self.salary_to = salary_to if salary_to else 0
        self.currency = currency if currency else ""
        self.link = link
        self.address = address
        self.responsibilities = responsibilities
        self.__avr_salary = self.calc_salary(self.salary_from, self.salary_to)
        Vacancy.__data.append(self)

    @staticmethod
    def calc_salary(salary_min: int, salary_max: int) -> int:
        """
        Вычисляет среднюю зарплату на основе минимальной и максимальной зарплаты.

        Args:
            salary_min (int): Минимальная зарплата.
            salary_max (int): Максимальная зарплата.

        Returns:
            int: Средняя зарплата.
        """
        if salary_min == 0 or salary_min is None:
            return salary_max
        elif salary_max == 0 or salary_max is None:
            return salary_min
        else:
            avr_salary = (salary_min + salary_max) // 2
            return avr_salary

    @property
    def avr_salary(self):
        """
        Свойство, возвращающее среднюю зарплату.

        Returns:
            int: Средняя зарплата.
        """
        return self.__avr_salary

    @property
    def data(self):
        """
        Свойство, возвращающее список всех объектов вакансий.

        Returns:
            list: Список объектов вакансий.
        """
        return Vacancy.__data

    @data.setter
    def data(self, value):
        """
        Свойство для установки списка объектов вакансий.

        Args:
            value (list): Новый список объектов вакансий.
        """
        Vacancy.__data = value

    def __repr__(self):
        return f"""1.{self.name_job}\n 2.{self.salary_from}\n 3.{self.salary_to}\n 4.{self.currency}\n 5.{self.address}
6.{self.responsibilities}
"""



    @classmethod
    def clean_data(cls):
        """
        Метод для очистки списка объектов вакансий.
        """
        cls.__data.clear()
