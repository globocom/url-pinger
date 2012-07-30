from flask import Flask, render_template
import datetime
import socket
import requests


app = Flask(__name__)

@app.route('/')
def home():
    sites = open("sites.txt").read().split()
    result = []
    for site in sites:
        try:
            response = requests.get(site, timeout=1, allow_redirects=True)
            assert response.text != ''
            assert response.status_code == 200
        except (requests.exceptions.RequestException, socket.timeout, AssertionError) as err:
            result.append((site, "fail"))
        else:
            result.append((site, "ok"))
    now = datetime.datetime.now()
    return render_template('pinger.html', result=result, last_update=now)


if __name__ == '__main__':
    app.run(debug=True)


