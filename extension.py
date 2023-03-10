import sys
# import openai
import demo
from Controller.controller_factory import ControllerFactory

# def openai_request(file_path: str):
#     with open(file_path, 'r') as source_code_file:
#         source_code = source_code_file.read()
#         language = get_file_extension(file_path)
#
#     if language == "java":
#         prompt = "can you create javadoc comments for the following java class\n" + source_code
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             max_tokens=1000,
#             temperature=0.6
#         )
#     else:
#         prompt = "can you create doc comments for the following python class\n" + source_code
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             max_tokens=1000,
#             temperature=0.6
#         )
#
#     return response.choices[0].text


def annotate_with_lazydoc(file_path: str):
    language = get_file_extension(file_path)
    with open(file_path) as source_code_file:
        source_code = source_code_file.read()
    annotator_controller = annotate_source_code(language, source_code)
    return demo.lazydoc_entry_point(annotator_controller)


def annotate_source_code(filename: str, source_code_string: str):
    if filename == 'py':
        return 'Success'
    controller = ControllerFactory(filename, source_code_string).get_controller()
    return controller


def get_file_extension(file_path: str):
    extension = file_path.rpartition('.')
    return extension[-1]


if __name__ == '__main__':
    engine = sys.argv[1]
    path = sys.argv[2]

    if engine == 'lazydoc':
        annotated_source_code = annotate_with_lazydoc(path)
    #
    # else:
    #     annotated_source_code = openai_request(path)

    print(annotated_source_code)