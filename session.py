# -*- coding: utf-8 -*-
from flask import Flask, request,make_response
from db import DBWorker, check_arguments
from sqlite3 import Error
from uuid import uuid4
import json
from connection import InfoConnect, Connect

app = Flask(__name__)


@app.route("/login")
def login():
    try:
        if not check_arguments(['login', 'password'], request.args):
            raise Exception('Bad arguments')

        login = request.args.get('login')
        password = request.args.get('password')

        if db_worker.confirm_data_login(login, password):
            code = "".join(str(uuid4()).split('-'))
            if Connect.find(InfoConnect(login, code)):
                raise Exception("You logged already")

            item = InfoConnect(login, code)
            Connect.add(item)
            return json.dumps({'code': code})

        raise Exception("No such login and password")

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/logout")
def logout():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get("login")
        code = request.args.get("code")
        if Connect.remove(login, code):
            return json.dumps({'ok': 'ok'})

        raise Exception("You not logged yet")

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/check_connect")
def check_connect():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get("login")
        code = request.args.get("code")
        if Connect.find(InfoConnect(login, code)):
            return json.dumps({'ok': 'ok'})

        raise Exception("Access denied")

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})

if __name__ == "__main__":
    db_worker = DBWorker()
    Connect = Connect()
    app.run(debug=True, port=65011)

