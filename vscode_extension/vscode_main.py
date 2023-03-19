import http.client
import sys
import json


def read_file(file_path: str):
    with open(file_path) as file:
        source_code = file.read()
    return source_code


def get_extension_from_file_path(file_path: str):
    extension = file_path.rpartition('.')
    return extension[-1]


def get_request_from_vscode(file_path: str, extension: str = "java"):
    source_code = read_file(file_path)
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


def send_request_to_chatgpt(json_string: str):
    return send_request_to_webserver("/openai_vscode", json_string)


if __name__ == '__main__':
    engine = sys.argv[1]
    path = sys.argv[2]
    code = read_file(path)
    file_extension = get_extension_from_file_path(path)

    jsonified = get_request_from_vscode(path, file_extension)

    if engine == 'lazydoc':
        commented = send_request_to_lazydoc(jsonified)

    else:
        commented = send_request_to_chatgpt(jsonified)

    print(commented)