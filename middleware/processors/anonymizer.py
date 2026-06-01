def anonymize(log):

    # email mask
    if "email" in log:
        email = log["email"]
        parts = email.split("@")
        log["email"] = parts[0][0] + "***@" + parts[1]

    # credit card mask
    if "credit_card" in log:
        cc = log["credit_card"]
        log["credit_card"] = "****-****-****-" + cc[-4:]

    return log