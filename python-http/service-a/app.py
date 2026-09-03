from flask import Flask, request, jsonify, g
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(response):
    latency_ms = (time.time() - g.start_time) * 1000
    logging.info(
        f"service=service-a endpoint={request.path} status={response.status_code} latency_ms={latency_ms:.2f}"
    )
    return response

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/echo")
def echo():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
