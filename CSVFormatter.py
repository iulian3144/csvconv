import sys
import jinja2


class CSVFormatter():
    """CSV formatter interface"""
    def print(self, file=sys.stdout):
        out_text = self.render()
        print(out_text, file=file)


class CSVtoHTMLFormatter(CSVFormatter):
    """CSV to HTML formatter"""
    def __init__(self, header, rows):
        self.header = header
        self.rows = rows
    def render(self):
        with open("csvtemplate.html") as template_file:
            csv_template = jinja2.Template(template_file.read())
            out_text = csv_template.render(header=self.header, rows=self.rows)
            return out_text