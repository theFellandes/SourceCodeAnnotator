import demo
import openai as openai
import vscode

from Controller.controller_factory import ControllerFactory

ext = vscode.Extension(
    name="lazy-doc",
    display_name="Lazy Doc",
    version="0.0.1",
    description="Use Lazy Doc to comment out your source code",
    icon="./icon.png",
    repository={"type": "git", "url": "https://github.com/theFellandes/SourceCodeAnnotator"}
)
ext.set_default_category("Search")


@ext.command("LazyDoc")
def lazydoc() -> None:
    comment_source_code("lazydoc")


@ext.command("ChatGPT")
def chat_gpt() -> None:
    comment_source_code("chatgpt")


def annotate_source_code(filename: str, source_code_string: str):
    controller = ControllerFactory(filename, source_code_string).get_controller()
    return controller


def comment_source_code(engine) -> None:
    editor = vscode.window.ActiveTextEditor()
    source_code = ""
    if editor != vscode.ext.undefined:
        source_code = editor.document.get_text(editor.selection)

    if engine == 'lazydoc':
        annotator_controller = annotate_source_code('java', source_code)
        source_output = demo.lazydoc_entry_point(annotator_controller)

    else:
        prompt = "can you create javadoc comments for the following java class\n" + source_code

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.6
        )
        source_output = response.choices[0].text

    editor.document.replace(editor.selection, source_output)



vscode.build(ext, publish=True)
