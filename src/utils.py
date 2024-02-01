import json
import os
from typing import Any
import psycopg2
import requests


def getting_data_from_file(filename: str) -> Any:
    """ принимает на вход путь до файла и возвращает список данных. Если есть ошибка,
    функция возвращает пустой список """
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_directory, 'data', filename)
    try:
        with open(file_path, encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def get_vacancies(employer_id) -> list:
    """Получение данных вакансий по API"""
    params = {
        'area': 1,
        'page': 0,
        'per_page': 50
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params).json()
    vacancies_data = [{
            'id_vacancy': int(item['id']),
            'vacancy_name': item['name'],
            'salary': item["salary"]['from'] if item["salary"] else None,
            'link': item['alternate_url'],
            'id_company': employer_id} for item in data_vacancies["items"] if item["salary"] != None]
    return vacancies_data


def get_employer(employer_id) -> dict:
    """Получение данных о работодателях по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    hh_company = {
        "id_company": int(employer_id),
        "company_name": data_vacancies['name'],
        "number_of_vacancies": data_vacancies['open_vacancies']
        }
    return hh_company

def creating_databases() -> None:
    """ Создание базы данных vacancies_by_company """
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="s4v77Am")
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute("CREATE DATABASE vacancies_by_company")


def creating__tables() -> None:
    """ Создание в vacancies_by_company две таблицы: company, vacancies """
    conn = psycopg2.connect(dbname="vacancies_by_company", user="postgres", password="s4v77Am")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE company (id_company SERIAL PRIMARY KEY,"
                   " company_name VARCHAR(100), number_of_vacancies INTEGER)")
    cursor.execute("CREATE TABLE vacancies (id_vacancy SERIAL PRIMARY KEY,"
                   " vacancy_name VARCHAR(150), salary INTEGER, link VARCHAR(150),"
                   " id_company INTEGER REFERENCES company(id_company))")
    conn.commit()


def filling_company_with_data(data_list: list) -> None:
    """ Заполнение данными таблицу company """
    conn = psycopg2.connect(dbname="vacancies_by_company", user="postgres", password="s4v77Am")
    with conn.cursor() as cur:
        for data in data_list:
            cur.execute("INSERT INTO company (id_company, company_name, number_of_vacancies)"
                        "VALUES (%s, %s, %s)",
                        (data["id_company"], data["company_name"],
                         data["number_of_vacancies"]))
        conn.commit()

def filling_vacancies_with_data(data_list: list) -> None:
    """ Заполнение данными таблицу vacancies """
    conn = psycopg2.connect(dbname="vacancies_by_company", user="postgres", password="s4v77Am")
    with conn.cursor() as cur:
        for data in data_list:
            cur.execute("INSERT INTO vacancies (id_vacancy, vacancy_name, salary, link, id_company)"
                            "VALUES (%s, %s, %s, %s, %s)",
                            (data["id_vacancy"], data["vacancy_name"],
                             data["salary"], data["link"], data["id_company"]))
    conn.commit()
    cur.close()
    conn.close()
