import os
import datetime
import socket
import requests
from flask import Flask, render_template


SITES_TXT = os.getenv("SITES_TXT", "sites.txt")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "1"))
REFRESH_TIMEOUT = float(os.getenv("REFRESH_TIMEOUT", "60"))
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "true") == "true"

app = Flask(__name__)


@app.route('/')
def home():
    sites = get_lines(SITES_TXT)
    result = []
    for line in sites:
        site, auth = extract_site_and_auth(line.strip())
        try:
            response = requests.get(site, timeout=REQUEST_TIMEOUT, allow_redirects=True, auth=auth)
            assert response.text != ''
            assert response.status_code == 200
        except (requests.exceptions.Timeout, socket.timeout) as err:
            print("Timeout to read {0} (timeout={1}): {2}".format(site, REQUEST_TIMEOUT, str(err)))
            result.append((site, "timeout"))
        except (requests.exceptions.RequestException, AssertionError) as err:
            print("Failed to read {0} (timeout={1}): {2}".format(site, REQUEST_TIMEOUT, str(err)))
            result.append((site, "fail"))
        else:
            result.append((site, "ok"))
    now = datetime.datetime.now()
    template_vars = dict(
        result=result,
        last_update=now,
        refresh_timeout=REFRESH_TIMEOUT)
    return render_template('pinger.html', **template_vars)


def get_lines(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def extract_site_and_auth(line):
    if ' ' in line:
        site, auth = line.rsplit(' ', 1)
        user, password = auth.split(':')
        return (site, (user, password))
    else:
        return [line, ()]


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)


