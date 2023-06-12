import http.client
import os
import sys
import json


def read_file(file_path: str):
    with open(file_path) as file:
        source_code = file.read()
    return source_code


def write_to_file(file_path: str, source_code: str):
    with open(f'{file_path[:-3]}_commented.py', 'w') as file:
        file.write(source_code)


def get_extension_from_file_path(file_path: str):
    extension = file_path.rpartition('.')
    return extension[-1]


def create_request(source_code: str, extension: str = "py"):
    payload = {
        "sourceText": source_code,
        "language": extension,
    }
    json_string = json.dumps(payload)
    return json_string


def send_request_to_webserver(endpoint: str, json_string: str):
    conn = http.client.HTTPConnection("localhost", 5000)
    conn.request("POST", endpoint, body=json_string, headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    annotated_source_code = conn.getresponse()
    data = annotated_source_code.read()
    conn.close()
    return json.loads(data).get("sourceOutput")


def send_request_to_lazydoc(json_string: str):
    return send_request_to_webserver("/lazydoc_vscode", json_string)


def get_files(directory, extensions):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths

if __name__ == '__main__':
    files = get_files(sys.argv[1], ['.py', '.java'])
    for path in files:
        code = read_file(path)
        file_extension = get_extension_from_file_path(path)
        jsonified = create_request(code, file_extension)
        commented = send_request_to_lazydoc(jsonified)
        write_to_file(file_path=path, source_code=commented)
