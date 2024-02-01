import psycopg2


class DBManager:
    """ класс для работы с данными в БД """

    def __init__(self) -> None:
        self.conn = psycopg2.connect(dbname="vacancies_by_company", user="postgres", password="s4v77Am")

    def get_companies_and_vacancies_count(self) -> list:
        """ получает список всех компаний и количество вакансий у каждой компании """
        with self.conn.cursor() as cur:
            cur.execute("SELECT company_name, number_of_vacancies FROM company")
            rows = cur.fetchall()
            cur.close()
            return rows

    def get_all_vacancies(self) -> list:
        """ получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию """
        with self.conn.cursor() as cur:
            cur.execute("SELECT vacancy_name, salary, link, company.company_name FROM vacancies"
                        " LEFT JOIN company USING (id_company)")
            rows = cur.fetchall()
            cur.close()
            return rows

    def get_avg_salary(self) -> int:
        """ получает среднюю зарплату по вакансиям """
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies")
            rows = cur.fetchall()
            cur.close()
            return int(rows[0][0])

    def get_vacancies_with_higher_salary(self) -> list:
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies"
                        " WHERE salary > (SELECT AVG(salary) FROM vacancies)")
            rows = cur.fetchall()
            cur.close()
            return rows

    def get_vacancies_with_keyword(self, word: str) -> list:
        """ получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python """
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies WHERE vacancy_name LIKE '%{word}%'""")
            rows = cur.fetchall()
            cur.close()
            return rows
