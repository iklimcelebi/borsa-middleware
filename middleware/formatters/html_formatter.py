def format_html(log):
    html = "<html><body><ul>"

    for key, value in log.items():
        html += f"<li><b>{key}</b>: {value}</li>"

    html += "</ul></body></html>"

    return html