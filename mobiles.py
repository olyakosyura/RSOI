from flask import Flask, request
from db import DBWorker, check_arguments
import json
from sqlite3 import Error

app = Flask(__name__)

@app.route("/short_info")
def short_info():
    try:
        if not check_arguments(['id'], request.args):
            raise Error("Bad arguments")

        result = db_worker.get_short_mobile_info_by_id(request.args.get("id"))
        if len(result) != 0:
            return json.dumps(result[0], ensure_ascii=False)

        raise Error("No such mobile")

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/full_info")
def full_info():
    try:
        if not check_arguments(['id'], request.args):
            raise Error("Bad arguments")

        _id = request.args.get("id")
        result = db_worker.get_full_mobile_info_by_id(_id)
        if len(result) != 0:
            return json.dumps(result[0], ensure_ascii=False)

        raise Error("No such mobile, id={0}".format(_id))

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/get_all_mobiles")
def get_all_mobiles():
    try:
        if not check_arguments(['page'], request.args):
            raise Error("Bad arguments")

        page = request.args.get('page')
        count_per_page = 2

        return json.dumps(db_worker.get_all_mobiles(page, count_per_page))

    except Error as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    db_worker = DBWorker()
    app.run(debug=True, port=65013)