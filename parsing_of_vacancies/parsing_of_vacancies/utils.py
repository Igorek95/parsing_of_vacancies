import json
import os
from headhunter import HeadHunterAPI
from json_saver import JSONSaver
from superjob import SuperJobAPI

# Константы для выбора платформы и метода
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
    """
    Функция для выбора платформы и выполнения связанных задач.
    """
    while True:
        conclusion_of_elections(platforms)
        user_input = input("Выберите платформу: \n-> ")

        if user_input == '1':
            process_platform(HeadHunterAPI(), 'vacancy.json')
            break
        elif user_input == '2':
            process_platform(SuperJobAPI(), 'vacancy.json')
            break
        elif user_input == '3':
            process_both_platforms()
            break
        elif user_input == '4':
            exit()
        else:
            print('Вы ввели неверное число')


def conclusion_of_elections(data):
    """
    Отображает список выбора пользователю.

    Args:
        data (dict): Словарь вариантов для отображения.
    """
    for k, v in data.items():
        print(f'{k} -> {v}')


def process_platform(api, filename):
    """
    Обрабатывает вакансии для одной платформы.

    Args:
        api: Экземпляр API платформы для поиска вакансий.
        filename (str): Имя JSON-файла для сохранения результатов.
    """
    user_vacancy = input("Введите название вакансии: \n-> ")
    api.get_vacancies(user_vacancy)
    json_saver = JSONSaver(filename)
    json_saver.save_to_file()


def process_both_platforms():
    """
    Обрабатывает вакансии для обеих платформ HH.ru и SuperJob, а затем объединяет результаты.
    """
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


def console_output(filename):
    """
    Выводит детали вакансий из JSON-файла в консоль.

    Args:
        filename (str): Имя JSON-файла для чтения.
    """
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
    """
    Главная функция для обработки выбора пользователя и выполнения связанных задач.
    """
    while True:
        conclusion_of_elections(choice_method)
        user_input = input('Выберите действие: \n-> ')

        if user_input == '1':
            console_output('vacancy.json')
        elif user_input == '2':
            user_salary = int(input('Введите минимальную зарплату: \n-> '))
            user_action = input('Что вы хотите сделать:\n1: Вывести в консоль.\n2: Сохранить\n3: Вернуться назад\n ->')

            if user_action == '1':
                get_vacancies_by_salary(user_salary)
            elif user_action == '2':
                save_vacancy_by_salary(user_salary)
            elif user_action == '3':
                continue
            else:
                print('Вы ввели неверное число')

        elif user_input == '3':
            user_delete = input(
                'Выберите какие данные удалить:\n1: Список вакансий\n2: Список отфильтрованных вакансий\n3: Вернуться '
                'назад\n')

            if user_delete == '1':
                delete_data_vacancy('vacancy.json')
            elif user_delete == '2':
                delete_data_vacancy('filtered_vacancies.json')
            elif user_delete == '3':
                continue
            else:
                print('Вы ввели неверное число')

        elif user_input == '4':
            while True:
                user_top = input(
                    'Выберите из какого списка вывести топ#10 \n1: Список всех вакансий \n2: Список отфильтрованных '
                    'вакансий\n3: Выйти назад\n')

                if user_top == '1':
                    top_vacancy('vacancy.json')
                elif user_top == '2':
                    try:
                        top_vacancy('filtered_vacancies.json')
                    except FileNotFoundError:
                        print('Вы не фильтровали по зарплате')
                elif user_top == '3':
                    break
                else:
                    print('Вы ввели неверное число')

        elif user_input == '5':
            platform()
        else:
            print('Вы ввели неверное число')


def get_vacancies_by_salary(min_salary: int):
    """
    Выводит вакансии с зарплатой не ниже указанной в консоль.

    Args:
        min_salary (int): Минимальная зарплата для фильтрации вакансий.
    """
    json_load = JSONSaver('vacancy.json')
    json_load.load_from_file()
    for vacancy in JSONSaver.vacancies:
        if vacancy.get("_Vacancy__avr_salary") >= min_salary:
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
            break


def save_vacancy_by_salary(min_salary: int):
    """
    Сохраняет вакансии с зарплатой не ниже указанной в JSON-файл.

    Args:
        min_salary (int): Минимальная зарплата для фильтрации вакансий.
    """
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
    """
    Выводит топ-10 вакансий с наивысшей зарплатой из JSON-файла в консоль.

    Args:
        filename (str): Имя JSON-файла для чтения.
    """
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
    """
    Удаляет данные о вакансиях из JSON-файла.

    Args:
        filename (str): Имя JSON-файла для удаления данных.
    """
    delete_json = JSONSaver(filename)
    delete_json.delete_vacancy()
