from flask import Flask, render_template, request, jsonify, Response
import os
import openai

import demo
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

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/openai', methods=['POST'])
def openai_request():
    source_code = request.form["sourceText"]
    prompt = "can you create javadoc comments for the following java class\n" + source_code

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.6
    )
    source_output = response.choices[0].text

    return render_template("index.html", sourceText=source_code, sourceOutput=source_output)


def read_file():
    file = request.files['source_code']
    return file.filename, file.read().decode('utf-8')


@app.route('/lazydoc', methods=['GET', 'POST'])
def read_text():
    source_code_text = request.form['sourceText']
    try:
        annotator_controller = annotate_source_code('java', source_code_text)
        source_output = demo.lazydoc_entry_point(annotator_controller)
    except Exception as exception:
        source_output = "Java Syntax Error"
    return render_template('index.html', sourceText=source_code_text, sourceOutput=source_output)


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.form['sourceOutput']:
        download_content = request.form['sourceOutput']
    return Response(
        download_content,
        mimetype="text/plain",
        headers={"Content-disposition":
                 "attachment; filename=output.java"})


def annotate_source_code(filename: str, source_code_string: str):
    controller = ControllerFactory(filename, source_code_string).get_controller()
    return controller


def get_file_extension():
    # TODO NOT IMPLEMENTED!
    return 'java'


if __name__ == '__main__':
    app.run()
