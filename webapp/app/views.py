from flask import render_template, request, jsonify
from prometheus_client import Counter
import requests
import libhoney
from app import app

prom_counter = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'code'])


@app.route('/')
def index():
    label_dict = {"method": request.method,
                  "endpoint": "/",
                  "code": ""}

    prom_counter.labels(**label_dict).inc()

    return render_template('index.html')

@app.route('/get-repos', methods=["GET"])
def get_repos():
    ev = libhoney.Event()
    username = request.args.get("username")
    ev.add_field("username",username)

    api_url = "https://api.github.com/users/{}/repos".format(username)
    with ev.timer("gitub_request_ms"):
        resp = requests.get(api_url)

    label_dict = {"method": "GET",
                  "endpoint": "/get-repos",
                  "code": resp.status_code}
    ev.add(label_dict)

    prom_counter.labels(**label_dict).inc()

    resp_dict = resp.json()
    ev.add_field("num_repos", len(resp_dict))
    ev.send()

    repos = [x["name"] for x in resp_dict]

    return jsonify(repos=repos)

