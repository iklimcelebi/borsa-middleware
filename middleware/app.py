import time
from datetime import datetime
import random

from flask import Flask, request, jsonify, render_template

from formatters.formatter_factory import FormatterFactory
from processors.filter import filter_log
from processors.log_factory import LogFactory
from processors.classifier import classify_log
from processors.anonymizer import anonymize
from processors.enricher import enrich_log

app = Flask(__name__)
API_KEY = "borsa-secret-key"
processed_logs = []
performance_results = {
    "total_logs_sent": 0,
    "successful_logs": 0,
    "failed_logs": 0,
    "execution_time_seconds": None,
    "throughput_logs_per_second": None,
    "last_reported_at": None
}
benchmark_result = {
    "total_logs": 0,
    "processed_logs": 0,
    "filtered_logs": 0,
    "execution_time_seconds": None,
    "logs_per_second": None
}
total_received_logs = 0
processed_logs_count = 0
filtered_logs_count = 0


def build_dashboard_stats(logs):
    level_labels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    risk_labels = ["LOW", "MEDIUM", "HIGH", "VERY HIGH"]

    level_counts = {label: 0 for label in level_labels}
    risk_counts = {label: 0 for label in risk_labels}

    for log in logs:
        level = (log.get("level") or "").upper()
        risk = (log.get("risk_level") or "").upper()

        if level in level_counts:
            level_counts[level] += 1
        if risk in risk_counts:
            risk_counts[risk] += 1

    return {
        "total_logs": len(logs),
        "level_counts": level_counts,
        "risk_counts": risk_counts
    }


@app.route("/log", methods=["POST"])
def handle_log():

    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    global total_received_logs, processed_logs_count, filtered_logs_count

    total_received_logs += 1
    log = LogFactory.create_log(request.json or {})

    log = filter_log(log)
    if log is None:
        filtered_logs_count += 1
        return jsonify({"status": "filtered (INFO/DEBUG/WARNING ignored)"})

    log = anonymize(log)
    log = enrich_log(log)
    log["category"] = classify_log(log)

    processed_logs.append(log)
    processed_logs_count += 1

    role = request.args.get("role", "web")
    formatter = FormatterFactory.get_formatter(role)
    formatted = formatter(log)

    return jsonify({"status": "processed", "formatted_data": formatted})


@app.route("/performance-report", methods=["POST"])
def performance_report():
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    report = request.json or {}
    performance_results.update({
        "total_logs_sent": report.get("total_logs_sent", performance_results["total_logs_sent"]),
        "successful_logs": report.get("successful_logs", performance_results["successful_logs"]),
        "failed_logs": report.get("failed_logs", performance_results["failed_logs"]),
        "execution_time_seconds": report.get("execution_time_seconds", performance_results["execution_time_seconds"]),
        "throughput_logs_per_second": report.get("throughput_logs_per_second", performance_results["throughput_logs_per_second"]),
        "last_reported_at": report.get("last_reported_at", performance_results["last_reported_at"])
    })

    return jsonify({"status": "performance updated"})


@app.route("/benchmark", methods=["GET"])
def benchmark():
    global total_received_logs, processed_logs_count, filtered_logs_count, benchmark_result

    total_logs = 1000
    processed = 0
    filtered = 0
    start_time = time.perf_counter()

    for index in range(total_logs):
        total_received_logs += 1
        raw_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": random.choice(["INFO", "WARNING", "ERROR", "CRITICAL"]),
            "message": random.choice([
                "User payment completed successfully",
                "Failed login attempt detected",
                "Database connection timeout",
                "Token validation failed",
                "Credit card authorization request",
                "Socket closed unexpectedly",
                "Unauthorized access denied",
                "User profile updated",
                "SQL query executed",
                "Payment gateway returned error"
            ]),
            "email": f"user{index}@example.com",
            "credit_card": f"4111-1111-1111-{1000 + index % 9000}"
        }

        filtered_log = filter_log(raw_log)
        if filtered_log is None:
            filtered += 1
            filtered_logs_count += 1
            continue

        anonymized = anonymize(filtered_log)
        enriched = enrich_log(anonymized)

        processed_logs.append(enriched)
        processed += 1
        processed_logs_count += 1

    duration = time.perf_counter() - start_time
    logs_per_second = processed / duration if duration > 0 else 0.0

    benchmark_result = {
        "total_logs": total_logs,
        "processed_logs": processed,
        "filtered_logs": filtered,
        "execution_time_seconds": round(duration, 2),
        "logs_per_second": round(logs_per_second, 2)
    }

    return jsonify(benchmark_result)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    stats = build_dashboard_stats(processed_logs)
    latest_logs = list(reversed(processed_logs))[:20]
    return render_template(
        "dashboard.html",
        logs=latest_logs,
        total_received_logs=total_received_logs,
        processed_logs_count=processed_logs_count,
        filtered_logs_count=filtered_logs_count,
        level_counts=stats["level_counts"],
        risk_counts=stats["risk_counts"],
        benchmark_result=benchmark_result
    )


@app.route("/debug", methods=["GET"])
def debug():
    stats = build_dashboard_stats(processed_logs)
    return jsonify({
        "total_received_logs": total_received_logs,
        "processed_logs_count": processed_logs_count,
        "filtered_logs_count": filtered_logs_count,
        "stats": stats,
        "sample_logs": processed_logs[-5:]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


