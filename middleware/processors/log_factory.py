class LogFactory:
    @staticmethod
    def create_log(data):
        return {
            "timestamp": data.get("timestamp"),
            "transaction_id": data.get("transaction_id"),
            "user": data.get("user"),
            "email": data.get("email"),
            "credit_card": data.get("credit_card"),
            "level": data.get("level"),
            "message": data.get("message")
        }
