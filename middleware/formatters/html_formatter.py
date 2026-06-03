def format_html(log):
    html = ["<html><body><h2>System Admin Log Detail</h2><table border='1' cellpadding='8' cellspacing='0'>"]

    for key, value in log.items():
        html.append(f"<tr><th style='text-align:left;padding:8px'>{key}</th><td style='padding:8px'>{value}</td></tr>")

    html.append("</table></body></html>")
    return "".join(html)