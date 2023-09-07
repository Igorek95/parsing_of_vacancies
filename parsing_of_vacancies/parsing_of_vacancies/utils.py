import json
import os

from headhunter import HeadHunterAPI
from json_saver import JSONSaver
from superjob import SuperJobAPI

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
            hh_save = JSONSaver('vacancy_hh.json')
            hh_save.save_to_file()
            sj.get_vacancies(user_vacancy)
            sj_save = JSONSaver('vacancy_sj.json')
            sj_save.save_to_file()
            JSONSaver.merge_json_files('vacancy_hh.json', 'vacancy_sj.json', 'vacancy.json')
            os.remove('vacancy_sj.json')
            os.remove('vacancy_hh.json')
            break
        elif user_input == '4':
            os.remove('vacancy.json')
            os.remove('filtered_vacancies.json')
            exit()

        else:
            print('Вы ввели неверное число')


def console_output(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data_vacancy = json.load(file)
        for vacancy in data_vacancy:
            name_job = vacancy.get('name_job')
            address = vacancy.get('address')
            avr_salary = vacancy.get('_Vacancy__avr_salary')
            currency = vacancy.get('currency')
            responsibilities = vacancy.get('responsibilities')
            link = vacancy.get('link')
            print(f'Название вакансии: {name_job}\n'
                  f'Место работы: {address}\n'
                  f'Зарплата: {avr_salary}.{currency}\n'
                  f'Ссылка: {link}\n'
                  f'Описание: {responsibilities}\n')
    except:
        raise FileNotFoundError('Нет такого файла')


def method():
    while True:
        for k, v in choice_method.items():
            print(f'{k} -> {v}')
        user_input = input('Выберите действие: \n-> ')
        if user_input == '1':
            console_output('vacancy.json')
        elif user_input == '2':
            user_salary = int(input('Введите минимальную зарплату: \n-> '))
            while True:
                user_action = input(
                    'Что вы хотите сделать:\n1: Вывести в консоль.\n2: Сохранить\n3: Вернуться назад\n ->')
                if user_action == '1':
                    get_vacancies_by_salary(user_salary)
                elif user_action == '2':
                    save_vacancy_by_salary(user_salary)
                elif user_action == '3':
                    method()
        elif user_input == '3':
            user_delete = input(
                'Выберите какие данные удалить:\n1: Список вакансий\n2: Список отфильтрованных вакансий\n3: Вернуться '
                'назад')
            if user_delete == '1':
                delete_daata_vacancy('vacancy.json')
            elif user_delete == '2':
                delete_daata_vacancy('filtered_vacancies.json')
            elif user_delete == '3':
                method()
        elif user_input == '4':
            while True:
                user_top = input(
                    'Выберите из какого списка вывести топ#10 \n1: Список всех вакансий \n2: Список отфильтрованных '
                    'вакансий\n'
                    '3: Выйти назад\n')
                if user_top == '1':
                    top_vacancy('vacancy.json')
                elif user_top == '2':
                    try:
                        top_vacancy('filtered_vacancies.json')
                    except FileNotFoundError:
                        print('Вы не фильтровали по зарплате')
                elif user_top == '3':
                    method()
        elif user_input == '5':
            platform()
            method()


def get_vacancies_by_salary(min_salary: int):
    json_load = JSONSaver('vacancy.json')
    json_load.load_from_file()
    for vacancy in JSONSaver.vacancies:
        if vacancy.get("_Vacancy__avr_salary") >= min_salary:
            for d in vacancy:
                name_job = d.get('name_job')
                address = d.get('address')
                avr_salary = d.get('_Vacancy__avr_salary')
                currency = d.get('currency')
                responsibilities = d.get('responsibilities')
                link = d.get('link')
                print(f'Название вакансии: {name_job}\n'
                      f'Место работы: {address}\n'
                      f'Зарплата: {avr_salary}.{currency}\n'
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
    with open('filtered_vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_vacancies, file, ensure_ascii=False, indent=4)


def top_vacancy(filename):
    load_json = JSONSaver(filename)
    load_json.load_from_file()
    sorted_json = sorted(load_json.vacancies, key=lambda x: x.get('_Vacancy__avr_salary'), reverse=True)
    for vacancy in sorted_json[:10]:
        name_job = vacancy.get('name_job')
        address = vacancy.get('address')
        avr_salary = vacancy.get('_Vacancy__avr_salary')
        currency = vacancy.get('currency')
        responsibilities = vacancy.get('responsibilities')
        link = vacancy.get('link')
        print(f'Название вакансии: {name_job}\n'
              f'Место работы: {address}\n'
              f'Зарплата: {avr_salary}.{currency}\n'
              f'Ссылка: {link}\n'
              f'Описание: {responsibilities}\n')


def delete_data_vacancy(filename):
    delete_json = JSONSaver(filename)
    delete_json.delete_vacancy()



