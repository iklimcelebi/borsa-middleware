def filter_log(log):
    if log["level"] in ["INFO", "DEBUG"]:
        return None
    return log