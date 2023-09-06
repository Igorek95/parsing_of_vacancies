import json
import os

from headhunter import HeadHunterAPI
from superjob import SuperJobAPI
from vacancy import Vacancy
from json_saver import JSONSaver

platforms = {1: 'HH.ru',
             2: 'SuperJob',
             3: "HH.ru + SuperJob",
             4: "Выход"
             }

choice_method = {1: 'Вывести в консоль',
                 2: "Отфильтровать по зарплате",
                 3: "Удалить данные",
                 4: "Вывести топ 10",
                 5: "Вернуться в главное меню"
                 }


def platform():
    while True:
        for k, v in platforms.items():
            print(f'{k} -> {v}')
        user_input = input("Выберите платформу: \n-> ")
        if user_input == '1':
            hh = HeadHunterAPI()
            user_vacancy = input("Введите название вакансии: \n-> ")
            hh.get_vacancies(user_vacancy)
            hh_save = JSONSaver('vacancy.json')
            hh_save.save_to_file()
            break
        elif user_input == '2':
            sj = SuperJobAPI()
            user_vacancy = input("Введите название вакансии: \n-> ")
            sj.get_vacancies(user_vacancy)
            sj_save = JSONSaver('vacancy.json')
            sj_save.save_to_file()
            break
        elif user_input == '3':
            hh = HeadHunterAPI()
            sj = SuperJobAPI()
            user_vacancy = input("Введите название вакансии: \n-> ")
            hh.get_vacancies(user_vacancy)
            hh_save = JSONSaver('vacancy.json')
            hh_save.save_to_file()
            sj.get_vacancies(user_vacancy)
            sj_save = JSONSaver('vacancy.json')
            sj_save.save_to_file()
            JSONSaver.merge_json_files('vacancy_hh.json', 'vacancy_sj.json', 'vacancy.json')
            os.remove('vacancy_sj.json')
            os.remove('vacancy_hh.json')
            break
        elif user_input == '4':
            exit()

        else:
            print('Вы ввели неверное число')


def console_output():
    file_path = 'vacancy.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for d in data:
            name_job = d.get('name_job')
            address = d.get('address')
            if d.get('salary_from'):
                salary_from = d.get('salary_from')
            else:
                salary_from = 0
            if d.get('salary_to'):
                salary_to = d.get('salary_to')
            else:
                salary_to = 0
            currency = d.get('currency')
            responsibilities = d.get('responsibilities')
            link = d.get('link')
            print(f'Название вакансии: {name_job}\n'
                  f'Место работы: {address}\n'
                  f'Зарплата: {salary_from} - {salary_to}.{currency}\n'
                  f'Ссылка: {link}\n'
                  f'Описание: {responsibilities}\n')
    except:
        raise FileNotFoundError('Нет такого файла')


def method():
    while True:
        for k, v in choice_method.items():
            print(f'{k} -> {v}')
        user_input = input()
        if user_input == '1':
            console_output()
        if user_input == '2':
            user_salary = int(input('Введите минимальную зарплату: \n-> '))
            while True:
                user_action = input('Что вы хотите сделать:\n1: Вывести в консоль.\n2: Сохранить\n3: Вернуться назад\n ->')
                if user_action == '1':
                    get_vacancies_by_salary(user_salary)
                elif user_action == '2':
                    save_vacancy_by_salary(user_salary)
                elif user_action == '3':
                    method()

        elif user_input == '5':
            platform()
            method()


def get_vacancies_by_salary(min_salary: int):
    json_load = JSONSaver('vacancy.json')
    json_load.load_from_file()
    filtered_vacancies = []
    for vacancy in JSONSaver.vacancies:
        if vacancy.get('salary_from'):
            if vacancy.get("salary_from") >= min_salary:
                filtered_vacancies.append(vacancy)
        elif vacancy.get('salary_to'):
            if vacancy.get("salary_to") >= min_salary:
                filtered_vacancies.append(vacancy)
        for d in filtered_vacancies:
            name_job = d.get('name_job')
            address = d.get('address')
            if d.get('salary_from'):
                salary_from = d.get('salary_from')
            else:
                salary_from = 0
            if d.get('salary_to'):
                salary_to = d.get('salary_to')
            else:
                salary_to = 0
            currency = d.get('currency')
            responsibilities = d.get('responsibilities')
            link = d.get('link')
            print(f'Название вакансии: {name_job}\n'
                  f'Место работы: {address}\n'
                  f'Зарплата: {salary_from} - {salary_to}.{currency}\n'
                  f'Ссылка: {link}\n'
                  f'Описание: {responsibilities}\n')
            break

def save_vacancy_by_salary(min_salary: int):
    if not JSONSaver.vacancies:
        json_load = JSONSaver('vacancy.json')
        json_load.load_from_file()
    filtered_vacancies = []
    for vacancy in JSONSaver.vacancies:
        if vacancy.get('salary_from'):
            if vacancy.get("salary_from") >= min_salary:
                filtered_vacancies.append(vacancy)
        elif vacancy.get('salary_to'):
            if vacancy.get("salary_to") >= min_salary:
                filtered_vacancies.append(vacancy)
    with open('filtered_vacancies.json',  'w', encoding='utf-8') as file:
        json.dump(filtered_vacancies, file, ensure_ascii=False, indent=4)



platform()
method()
