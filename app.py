from flask import Flask, render_template, request

from Controller.annotator_controller import AnnotatorController
from Controller.java_controller import JavaController
from Controller.python_controller import PythonController
from conf import settings

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def source_code_annotator():
    if request.method == "POST":
        filename, source_code_string = read_file()
        if source_code_string == '':
            # TODO get java or python from here
            filename = get_file_extension()
            source_code_string = read_text()

        annotate_source_code(filename, source_code_string)


    return render_template('index.html')


def read_file():
    file = request.files['source_code']
    return file.filename, file.read().decode('utf-8')


def read_text():
    source_code_text = request.form['source_code_text']
    return source_code_text


def annotate_source_code(filename: str, source_code_string: str):
    annotator_controller = AnnotatorController(get_controller(filename, source_code_string))
    annotator_controller.generate_report()


def get_controller(source_code_file_name: str, source_code_string: str):
    match settings.get_file_extension(source_code_file_name):
        case 'java':
            return JavaController(source_code_file_name, source_code_string)
        case 'py':
            return PythonController(source_code_file_name, source_code_string)
        case _:
            return NotImplementedError

def get_file_extension():
    # TODO NOT IMPLEMENTED!
    return 'java'


if __name__ == '__main__':
    app.run()
