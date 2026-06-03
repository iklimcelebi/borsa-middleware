def format_csv(log):
    fields = ["timestamp", "level", "message", "category", "risk_level", "sender_id", "transaction_no"]
    values = [str(log.get(field, "")) for field in fields]
    return ",".join(values)