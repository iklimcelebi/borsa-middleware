import random
from datetime import datetime

from processors.classifier import classify_log

def enrich_log(log):
    log["processed_at"] = str(datetime.now())
    log["category"] = classify_log(log)

    level = (log.get("level") or "").upper()
    if level == "INFO":
        log["risk_level"] = "LOW"
    elif level == "WARNING":
        log["risk_level"] = "MEDIUM"
    elif level == "ERROR":
        log["risk_level"] = "HIGH"
    elif level == "CRITICAL":
        log["risk_level"] = "VERY HIGH"
    else:
        log["risk_level"] = "UNKNOWN"

    log["sender_id"] = "middleware-service"
    log["transaction_no"] = random.randint(100000, 999999)
    return log