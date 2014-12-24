from flask import Flask, redirect, request
import requests
import requests.auth
application = Flask(__name__)

client_id = '3272315213.3280099727'
client_secret = '210be9038f11fa17e3849e577a20d8ac'

redirect_uri = 'http://127.0.0.1/app'

@application.route("/")
def index():
    url = 'https://slack.com/oauth/authorize'
    resp_type = "code"
    reqtext = url + "?" + "client_id=" + client_id + "&response_type=" + resp_type + "&redirect_uri=" + redirect_uri
    return redirect(reqtext, 302)

@application.route("/app", methods=['GET', 'POST'])
def app():
    if request.method == "POST":
        return request.data
    else:
        code = request.args.get('code')

        if code is None:
            return "Sorry :("

        url = 'https://slack.com/api/oauth.access?client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=authorization_code' + '&redirect_uri=' + redirect_uri + '&code=' + code
        k = requests.get(url)
        if k.status_code != 200:
            return "Internal request error"
        access_token = k.json()["access_token"]

        url = r'https://slack.com/api/auth.test?token=' + access_token

        response = requests.get(url)
        if response.status_code != 200:
            return "Internal request error"
        return response.text

if __name__ == "__main__":
    application.run(port=80, debug=True)
