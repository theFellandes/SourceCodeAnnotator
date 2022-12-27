from flask import Flask, render_template, request
import os
import openai

from Controller.annotator_controller import AnnotatorController
from Controller.controller_factory import ControllerFactory

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def source_code_annotator():
    if request.method == "POST":
        # TODO get java or python from here
        filename = "java"
        source_code_string = read_text()
        annotate_source_code(filename, source_code_string)

    return render_template('index.html')


@app.route('/openai', methods=['GET', 'POST'])
def openai_request():
    openai.Model.list()
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Say this is a test",
            max_tokens=7,
            temperature=0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("animal.html", result=result)


def read_file():
    file = request.files['source_code']
    return file.filename, file.read().decode('utf-8')


@app.route('/lazydoc', methods=['GET', 'POST'])
def read_text():
    source_code_text = request.form['sourceCode']
    return source_code_text


def annotate_source_code(filename: str, source_code_string: str):
    controller = ControllerFactory(filename, source_code_string).get_controller()
    annotator_controller = AnnotatorController(controller)
    annotator_controller.generate_report()


def get_file_extension():
    # TODO NOT IMPLEMENTED!
    return 'java'


if __name__ == '__main__':
    app.run()
