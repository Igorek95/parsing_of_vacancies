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
        Vacancy.__data.append(self)

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
