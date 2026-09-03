# Python HTTP Track

Service A (8080): `/health`, `/echo?msg=...`
Service B (8081): `/health`, `/call-echo?msg=...` (calls Service A)

## Run Service A

```bash
cd python-http/service-a
pip install -r requirements.txt
python app.py
```

## Run Service B (new terminal)

```bash
cd python-http/service-b
pip install -r requirements.txt
python app.py
```

## Test

```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

![Success demonstration](python-http/image-3.png)

Stop Service A and rerun the curl command to observe failure handling.

```bash
curl -i "http://127.0.0.1:8081/call-echo?msg=hello"
```

Returns `503` with `{"error": "Service A unavailable"}`. Service B's `/health` still returns `200`.

![Failure demonstration](python-http/image-1.png)

## What Makes This Distributed?

Service A and Service B run as separate processes and communicate over HTTP instead of calling each other's functions directly. Each can fail independently — if Service A goes down, Service B stays up, handles the failed request, and returns 503 instead of crashing.
