from flask import Flask, request, jsonify, render_template

from formatters.json_formatter import format_json
from formatters.csv_formatter import format_csv
from formatters.html_formatter import format_html

from processors.filter import filter_log
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

    log = request.json

    # 1. FILTER
    log = filter_log(log)
    if log is None:
        return jsonify({
            "status": "filtered (INFO/DEBUG ignored)"
        })

    # 2. ANONYMIZE
    log = anonymize(log)

    # 3. ENRICH
    log = enrich_log(log)

    processed_logs.append(log)

    role = request.args.get("role", "web")

    if role == "admin":
        formatted = format_html(log)

    elif role == "cyber":
        formatted = format_csv(log)

    else:
        formatted = format_json(log)

    return jsonify({
        "status": "processed",
        "formatted_data": formatted
    })


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


@app.route("/dashboard", methods=["GET"])
def dashboard():
    stats = build_dashboard_stats(processed_logs)
    latest_logs = list(reversed(processed_logs))
    recent_logs = latest_logs[:20]
    return render_template(
        "dashboard.html",
        logs=recent_logs,
        total_logs=stats["total_logs"],
        level_counts=stats["level_counts"],
        risk_counts=stats["risk_counts"],
        performance_results=performance_results
    )


@app.route("/debug", methods=["GET"])
def debug():
    stats = build_dashboard_stats(processed_logs)
    return jsonify({
        "processed_logs_count": len(processed_logs),
        "stats": stats,
        "sample_logs": processed_logs[-5:]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)