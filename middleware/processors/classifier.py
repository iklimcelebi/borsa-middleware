def classify_log(log):
    message = (log.get("message") or "").lower()

    payment_keywords = ["payment"]
    auth_keywords = ["login", "auth", "password", "token", "unauthorized", "access denied"]
    database_keywords = ["database", "sql", "connection", "db"]
    network_keywords = ["network", "timeout", "socket"]

    if any(keyword in message for keyword in payment_keywords):
        return "PAYMENT"
    if any(keyword in message for keyword in auth_keywords):
        return "AUTH"
    if any(keyword in message for keyword in database_keywords):
        return "DATABASE"
    if any(keyword in message for keyword in network_keywords):
        return "NETWORK"

    return "GENERAL"
