from flask import Flask, request, make_response
from db import DBWorker, check_arguments
import json
from sqlite3 import Error

app = Flask(__name__)


@app.route("/me")
def me():
    try:
        if not check_arguments(['login'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        result = db_worker.get_user_data_by_login(login)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Exception("No such user")

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/add_login", methods=['POST'])
def add_login():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'password'], data_json):
            raise Exception("Bad arguments")

        db_worker.insert_into_data_login_table(data_json['login'], data_json['password'])

        return json.dumps({'ok': 'ok'})

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/add_user", methods=['POST'])
def add_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'email', 'like', 'my'], data_json):
            raise Exception("Bad arguments")

        db_worker.insert_into_data_users_table(data_json['login'], data_json['first'], data_json['second'],
                                               data_json['age'], data_json['city'], data_json['email'],
                                               data_json['like'], data_json['my'])

        return json.dumps({'ok': 'ok'})

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/remove_login", methods=['DELETE'])
def remove_login():
    try:
        data_json = request.get_json()
        if not check_arguments(['login'], data_json):
            raise Exception("Bad arguments")

        db_worker.delete_from_data_login_table(data_json['login'])

        return json.dumps({'ok': 'ok'})

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/remove_user", methods=['DELETE'])
def remove_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login'], data_json):
            raise Exception("Bad arguments")

        db_worker.delete_from_data_users_table(data_json['login'])

        return json.dumps({'ok': 'ok'})

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/update_user", methods=['PUT'])
def update_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'email', 'like', 'my'], data_json):
            raise Exception("Bad arguments")

        db_worker.update_data_users_table(data_json['login'], data_json['first'], data_json['second'],
                                          data_json['age'], data_json['city'], data_json['email'],
                                          data_json['like'], data_json['my'])

        return json.dumps({'ok': 'ok'})

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/user/<_id>")
def user_info(_id):
    try:
        result = db_worker.get_user_data_by_id(_id)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Exception("No user with such id {0}".format(_id))

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/login_to_id")
def login_to_id():
    try:
        if not check_arguments(['login'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        result = db_worker.get_id_by_login(login)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Exception("No user with such login {0}".format(login))

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})

		



if __name__ == "__main__":
    db_worker = DBWorker()
    app.run(debug=True, port=65012)