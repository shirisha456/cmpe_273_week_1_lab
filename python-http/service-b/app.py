from flask import Flask, request, jsonify, g
import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)

SERVICE_A = "http://127.0.0.1:8080"

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(response):
    latency_ms = (time.time() - g.start_time) * 1000
    logging.info(
        f"service=service-b endpoint={request.path} status={response.status_code} latency_ms={latency_ms:.2f}"
    )
    return response

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/call-echo")
def call_echo():
    msg = request.args.get("msg", "")
    try:
        r = requests.get(f"{SERVICE_A}/echo", params={"msg": msg}, timeout=1.0)
        r.raise_for_status()
        data = r.json()
        return jsonify(service_b="ok", service_a=data)
    except requests.exceptions.RequestException as e:
        # Covers connection failure, timeout, and other requests errors
        logging.error(f'service=service-b endpoint=/call-echo error="Service A unavailable: {e}"')
        return jsonify(error="Service A unavailable"), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
