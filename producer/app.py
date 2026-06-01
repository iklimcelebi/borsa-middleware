from flask import Flask, jsonify, request
import requests
import time
from datetime import datetime
import random

app = Flask(__name__)
API_KEY = "borsa-secret-key"
HEADERS = {"x-api-key": API_KEY}

@app.route("/")
@app.route("/send-log")
def send_log():

    # URL'den role al
    role = request.args.get("role", "web")

    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    level = random.choice(levels)
    messages = {
        "INFO": "User viewed stock details",
        "WARNING": "Suspicious login attempt detected",
        "ERROR": "Payment failed during stock transaction",
        "CRITICAL": "Database connection lost"
    }
    log = {
        "timestamp": str(datetime.now()),
        "transaction_id": random.randint(10000, 99999),
        "user": "iklim",
        "email": "iklim@gmail.com",
        "credit_card": "1234-5678-9999-0000",
        "level": level,
        "message": messages[level]
    }

    # Middleware'e gönder
    response = requests.post(
        f"http://middleware:5000/log?role={role}",
        json=log,
        headers=HEADERS
    )

    return jsonify({
        "producer_status": "Log gönderildi",
        "selected_role": role,
        "sent_log": log,
        "middleware_response": response.json()
    })

@app.route("/performance-test")
def performance_test():
    total_logs_sent = 1000
    successful_logs = 0
    failed_logs = 0
    start_time = time.time()

    for i in range(total_logs_sent):
        log = {
            "timestamp": str(datetime.now()),
            "transaction_id": random.randint(10000, 99999),
            "user": f"perf_user_{i}",
            "email": f"perf_user_{i}@example.com",
            "credit_card": "1234-5678-9999-0000",
            "level": random.choice(["ERROR", "WARNING", "INFO", "CRITICAL"]),
            "message": "Performance test log"
        }

        try:
            response = requests.post(
                "http://middleware:5000/log",
                json=log,
                headers=HEADERS,
                timeout=10
            )
            if response.ok:
                successful_logs += 1
            else:
                failed_logs += 1
        except requests.RequestException:
            failed_logs += 1

    end_time = time.time()
    execution_time_seconds = round(end_time - start_time, 3)
    throughput_logs_per_second = round(successful_logs / execution_time_seconds, 2) if execution_time_seconds > 0 else 0

    result = {
        "total_logs_sent": total_logs_sent,
        "successful_logs": successful_logs,
        "failed_logs": failed_logs,
        "execution_time_seconds": execution_time_seconds,
        "throughput_logs_per_second": throughput_logs_per_second,
        "last_reported_at": str(datetime.now())
    }

    try:
        requests.post(
            "http://middleware:5000/performance-report",
            json=result,
            headers=HEADERS,
            timeout=10
        )
    except requests.RequestException:
        pass

    return jsonify(result)


@app.route("/stress-test")
def stress_test():

    total = 1000

    for i in range(total):

        log = {
            "timestamp": str(datetime.now()),
            "transaction_id": random.randint(10000, 99999),
            "user": f"user{i}",
            "email": f"user{i}@gmail.com",
            "credit_card": "1234-5678-9999-0000",
            "level": random.choice(["ERROR", "WARNING", "INFO"]),
            "message": "Stress test log"
        }

        requests.post(
            "http://middleware:5000/log",
            json=log,
            headers=HEADERS
        )

    return {
        "status": "completed",
        "total_logs_sent": total
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)