from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from sqlite3 import Error
from time import ctime
import json
import db
import helper


app = Flask(__name__)


@app.route("/")
def homepage():
    view =  "<a href='http://localhost:65010/login'>Sign In</a><br>"
    view += "<a href='http://localhost:65010/register'>Sign Up</a><br>"
    view += "<a href='http://localhost:65010/status'>Who I am?</a><br>"
    view += "<a href='http://localhost:65010/logout'>Logout</a><br>"
    return view


@app.route("/login")
def login():
    return render_template("SignIn.html")


@app.route("/register")
def registration():
    return render_template("SignUp.html")


@app.route("/logout")
def logout():
    redirect_to_login = redirect('/login')
    response = app.make_response(redirect_to_login)
    response.set_cookie('login', expires=0)
    return response


@app.route("/SignUp", methods=['POST'])
def confirm_registration():
    try:
        login = request.form['login']
        email = request.form['email']
        firstname = request.form['firstname']
        password = request.form['pwd']
        if not (login and email and firstname and password):
            return "All fields must be not empty. Check it, please."
        password_confirm = request.form['confirm']
        if password != password_confirm:
            return "Passwords not equal. Check it, please."
        db_worker.insert_into_data_user_table(login, firstname, email)
        db_worker.insert_into_data_login_table(login, password)
        return "Registration completed!"
    except Error as e:
        return str(e)


@app.route("/SignIn", methods=['POST'])
def SignIn():
    try:
        login = request.form['login']
        password = request.form['pwd']
        if not (login and password):
            return "Login or password is empty. It is impossible."
        if db_worker.confirm_data_login(login, password):
            redirect_to_home = redirect('/')
            response = app.make_response(redirect_to_home)
            response.set_cookie('login', value=login)
            return response
        return "No such login and password."
    except Error as e:
        return str(e)


@app.route("/status", methods=['GET'])
def check_status():
    login = request.cookies.get('login')
    return json.dumps({'answer': login})


@app.route("/oauth/authorize")
def oauth_authorize():
    try:
        login = request.cookies.get('login')
        if login:
            client_id = request.args.get('client_id')
            if db_worker.check_user_and_client_id(login, client_id):
                state = request.args.get('state')
		if not state:
                    return json.dumps({'error': "state is null"})
                uri = request.args.get('redirect_uri')

                if not uri:
                    return json.dumps({'error': "redirect_uri is null"})
                code = helper.generate_random_code()
                exp_time = helper.get_exp_time_for_code()
                db_worker.add_to_data_code(login, client_id, code, exp_time, uri)
                uri = "http://"+uri+"?code={0}".format(code)
                if state:
                    uri += "&state={0}".format(state)
                return redirect(uri)
        return redirect("/login")

    except Error as e:
        return str(e)


@app.route("/oauth/token", methods=['POST'])
def oauth_token():
    try:
        if not ('code' in request.form and
                'client_id' in request.form and
                'client_secret' in request.form and
                'redirect_uri' in request.form):
            return json.dumps({'error': "invalid parameters"})

        code = request.form['code']
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        uri = request.form['redirect_uri']

        login = db_worker.get_login_by_client_id(client_id)
        db_worker.check_code_for_getting_token(login, code, client_id, client_secret, uri)

        access_token = helper.generate_random_code()
        refresh_token = helper.generate_random_code()
        exp_time = helper.get_exp_time_for_access_token()

        db_worker.add_to_data_access(client_id, access_token, refresh_token, exp_time)
        db_worker.remove_from_data_code(login, client_id)

        return json.dumps([{'access_token': access_token},
                           {'refresh_token': refresh_token},
                           {'expiration_time': ctime(exp_time)},
                           {'type': "Bearer"}])
    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/oauth/refresh", methods=['POST'])
def oauth_refresh():
    try:
        if not ('client_id' in request.form and
                'client_secret' in request.form and
                'refresh_token' in request.form):
            return json.dumps({'error': "invalid parameters"})

        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        refresh_token_old = request.form['refresh_token']

        db_worker.check_for_refresh_token(client_id, client_secret, refresh_token_old)

        access_token = helper.generate_random_code()
        refresh_token = helper.generate_random_code()
        exp_time = helper.get_exp_time_for_access_token()

        db_worker.update_data_access(client_id, refresh_token_old, access_token, refresh_token, exp_time)

        return json.dumps([{'access_token': access_token},
                           {'refresh_token': refresh_token},
                           {'expiration_time': ctime(exp_time)},
                           {'type': "Bearer"}])

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/me", methods=['GET'])
def me_request():
    try:
        authorization = request.headers.get('Authorization')
        if authorization:
            params = authorization.split()
            if len(params) == 2 and params[0] == "Bearer":
                access_token = params[1]
                db_worker.check_token(access_token)
                return json.dumps(db_worker.get_me_data(access_token)[0])
        raise Exception("bad parameters")

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/users", methods=['GET'])
def users_request():
    try:
        page = request.args.get('page')
        page = page if page else 1
        total = db_worker.get_count_records_in_table("data_user")
        result = db_worker.get_all_users(page)
        return json.dumps({'total': total, 'page': page,
                           'per_page': helper.records_per_page, 'items': result})

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/users/<_id>", methods=['GET'])
def user_by_id_request(_id):
    try:
        result = process_request(request, db_worker.get_user_by_id,  _id)
        result = result[0] if len(result) != 0 else {}
        return json.dumps(result)

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/mobile", methods=['GET'])
def mobile_request():
    try:
	
        page = request.args.get('page')
        page = page if page else 1
        total = db_worker.get_count_records_in_table("data_mobile")
        result = process_request(request, db_worker.get_all_mobile, page)
        return json.dumps({'total': total, 'page': page,
                           'per_page': helper.records_per_page, 'items': result})

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/mobile/<_id>", methods=['GET'])
def mobile_by_id_request(_id):
    try:
        result = process_request(request, db_worker.get_mobile_by_id, _id)
        result = result[0] if len(result) != 0 else {}
        return json.dumps(result, ensure_ascii=False)

    except Error as e:
        return str(e)
    except Exception as e:
        return json.dumps({'error': str(e)})


def process_request(request, func, args):
    authorization = request.headers.get('Authorization')
    if authorization:
        params = authorization.split()
        if len(params) == 2 and params[0] == "Bearer":
            access_token = params[1]
            db_worker.check_token(access_token)
            return func(args)
    raise Exception("bad parameters")


if __name__ == "__main__":
    db_worker = db.DBWorker()
    app.run(debug=True, port=65010)
