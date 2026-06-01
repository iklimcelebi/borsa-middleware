import random
from datetime import datetime

def enrich_log(log):
    log["processed_at"] = str(datetime.now())

    if log["level"] == "INFO":
        log["risk_level"] = "LOW"
    elif log["level"] == "WARNING":
        log["risk_level"] = "MEDIUM"
    elif log["level"] == "ERROR":
        log["risk_level"] = "HIGH"
    elif log["level"] == "CRITICAL":
        log["risk_level"] = "VERY HIGH"
    else:
        log["risk_level"] = "UNKNOWN"

    log["sender_id"] = "middleware-service"
    log["transaction_no"] = random.randint(100000, 999999)
    return log