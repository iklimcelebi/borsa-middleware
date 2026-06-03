from .html_formatter import format_html
from .csv_formatter import format_csv
from .json_formatter import format_json


class FormatterFactory:
    FORMATTERS = {
        "admin": format_html,
        "cyber": format_csv,
        "web": format_json
    }

    @staticmethod
    def get_formatter(role):
        return FormatterFactory.FORMATTERS.get(role, format_json)
