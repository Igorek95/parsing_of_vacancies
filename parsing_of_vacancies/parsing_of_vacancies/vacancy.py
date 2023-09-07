import json


class Vacancy:
    __data = []

    def __init__(self, name_job, salary_from, salary_to, currency, link, address, responsibilities):
        self.name_job = name_job
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.link = link
        self.address = address
        self.responsibilities = responsibilities
        self.__avr_salary = self.calc_salary(self.salary_from,  self.salary_to)
        Vacancy.__data.append(self)

    @staticmethod
    def calc_salary(salary_min: int, salary_max: int) -> int:
        if salary_min == 0 or salary_min is None:
            return salary_max
        elif salary_max == 0 or salary_max is None:
            return salary_min
        else:
            avr_salary = (salary_min + salary_max) // 2
            return avr_salary

    @property
    def avr_salary(self):
        return self.__avr_salary

    @property
    def data(self):
        return Vacancy.__data

    @data.setter
    def data(self, value):
        Vacancy.__data = value


    def __repr__(self):
            return f"""1.{self.name_job}\n 2.{self.salary_from}\n 3.{self.salary_to}\n 4.{self.currency}\n 5.{self.address}
    6.{self.responsibilities}
    """

    def __eq__(self, other):
        return self.salary_from == other.salary

    def __lt__(self, other):
        if self.salary_from < other.salary:
            self.data.remove(self)
            return True

    @classmethod
    def clean_data(cls):
        cls.__data.clear()
