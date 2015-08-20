from flask import Flask, request, make_response
from db import DBWorker, check_arguments
import json
from sqlite3 import Error

app = Flask(__name__)

@app.route("/short_info")
def short_info():
    try:
        if not check_arguments(['id'], request.args):
            raise Exception("Bad arguments")

        result = db_worker.get_short_mobile_info_by_id(request.args.get("id"))
        if len(result) != 0:
            return json.dumps(result[0], ensure_ascii=False)

        raise Exception("No such mobile")

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/full_info")
def full_info():
    try:
        if not check_arguments(['id'], request.args):
            raise Exception("Bad arguments")

        _id = request.args.get("id")
        result = db_worker.get_full_mobile_info_by_id(_id)
        if len(result) != 0:
            return json.dumps(result[0], ensure_ascii=False)

        raise Exception("No such mobile, id={0}".format(_id))

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})


@app.route("/get_all_mobiles")
def get_all_mobiles():
    try:
        if not check_arguments(['page'], request.args):
            raise Exception("Bad arguments")

        page = request.args.get('page')
        count_per_page = 2

        return json.dumps(db_worker.get_all_mobiles(page, count_per_page))

    except Exception as e:
        return make_response(str(e), 400, {'olol':'ololol'})

if __name__ == "__main__":
    db_worker = DBWorker()
    app.run(debug=True, port=65013)