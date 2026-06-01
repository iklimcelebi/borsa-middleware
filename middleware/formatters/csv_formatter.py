def format_csv(log):
    values = [str(v) for v in log.values()]
    return ",".join(values)