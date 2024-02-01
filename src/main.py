from pprint import pprint
from src.utils import (getting_data_from_file, get_vacancies, get_employer, creating_databases, creating__tables,
                       filling_company_with_data, filling_vacancies_with_data)
from src.DBManager import DBManager

data_company = getting_data_from_file('company.json')  # список id компаний
list_company = [get_employer(company) for company in data_company]  # список с данными по компаниям
list_vacancies = [get_vacancies(vacancy) for vacancy in data_company
                  if get_vacancies(vacancy) != []]  # список с данными по вакансиям

creating_databases()
print('''База данных "vacancies_by_company" успешно создана
''')
creating__tables()
print('''Таблицы "company" и "vacancies" успешно созданы
''')

# Заполнение таблиц данными с hh.ru
filling_company_with_data(list_company)
for vacancies in list_vacancies:
    filling_vacancies_with_data(vacancies)

# Получение данных из таблиц
manager_bd = DBManager()
# pprint(manager_bd.get_companies_and_vacancies_count())  # все компании и количество вакансий в каждой
# pprint(manager_bd.get_all_vacancies())  # вакансии с указанием компании, названия, зарплаты и ссылки на вакансию
# pprint(manager_bd.get_avg_salary())  # Средняя зп
# pprint(manager_bd.get_vacancies_with_higher_salary())  # вакансии с зп выше средней по выборке
word = input("Введите ключевое слово для поиска:  ")
pprint(manager_bd.get_vacancies_with_keyword(word))