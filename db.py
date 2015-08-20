# -*- coding: utf-8 -*-
import sqlite3


def check_arguments(what, where):
    if not where:
        return False

    for i in what:
        if not i in where:
            return False

    return True


class DBWorker:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_name = "mydatabase.sqlite"
        self.records_per_page = 2

    def execute_query(self, query):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        records = self.cursor.execute(query).fetchall()
        self.connection.commit()
        self.connection.close()
        return records

    def execute_and_return_json(self, query):
        records = self.execute_query(query)
        records_json = [dict(rec) for rec in records]
        return records_json

    def insert_into_data_login_table(self, login, password):
        query = "INSERT INTO data_login VALUES ('{0}', '{1}')".format(login, password)
        self.execute_query(query)

    def delete_from_data_login_table(self, login):
        query = "DELETE FROM data_login WHERE login='{0}'".format(login)
        return self.execute_query(query)

    def insert_into_data_users_table(self, login, fname, sname, age, city, email, like, my):
        query = "INSERT INTO data_users VALUES (NULL, '{0}', '{1}', '{2}', {3}, '{4}', '{5}')".\
                format(login, fname, sname, email, like, my)
        self.execute_query(query)

    def delete_from_data_users_table(self, login):
        query = "DELETE FROM data_users WHERE login='{0}'".format(login)
        return self.execute_query(query)

    def update_data_users_table(self, login, fname, sname, email, like, my):
        query = "UPDATE data_users set firstname='{0}', secondname='{1}', email='{2}' " \
				"like_mobiles='{3}', my_mobiles='{4}' " \
                "where login='{5}'".format(fname, sname, email, like, my, login)
        return self.execute_query(query)

    def confirm_data_login(self, login, password):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        query = "SELECT * FROM data_login WHERE login='{0}' AND password='{1}'".format(login, password)
        records = self.execute_query(query)
        return len(records) > 0

    def get_user_data_by_id(self, _id):
        query = "SELECT firstname, secondname, email, like_mobiles, my_mobiles" \
                " FROM data_users WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_user_data_by_login(self, login):
        query = "SELECT firstname, secondname, email, like_mobiles, my_mobiles" \
                " FROM data_users WHERE login='{0}'".format(login)
        return self.execute_and_return_json(query)

    def get_id_by_login(self, login):
        query = "SELECT id FROM data_users WHERE login='{0}'".format(login)
        return self.execute_and_return_json(query)

    def get_short_mobile_info_by_id(self, _id):
        query = "SELECT firm, model, description FROM data_mobiles WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_full_mobile_info_by_id(self, _id):
        query = "SELECT firm, model, color, cost, description FROM data_mobiles WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_all_mobiles(self, page, count_per_page):
        offset = (int(page)-1) * count_per_page
        query = "SELECT firm, model, color, cost, description FROM data_mobiles " \
                "LIMIT {0} OFFSET {1}".format(count_per_page, offset)
        return self.execute_and_return_json(query)