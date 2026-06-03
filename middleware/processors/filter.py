def filter_log(log):
    level = (log.get("level") or "").upper()
    if level in ["INFO", "DEBUG", "WARNING"]:
        return None
    return log