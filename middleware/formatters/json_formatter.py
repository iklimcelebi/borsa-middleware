def format_json(log):
    return {
        "timestamp": log.get("timestamp"),
        "level": log.get("level"),
        "message": log.get("message"),
        "category": log.get("category")
    }