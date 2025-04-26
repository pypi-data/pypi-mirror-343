import json

import requests
import yaml

from autotests_coverage.config import EnvConfig


def __delete_ignored_paths_from_json(api_doc_data: requests.Response, paths_to_delete: list) -> dict:
    data: dict = api_doc_data.json()

    for path in paths_to_delete:
        if path in data["paths"]:
            del data["paths"][path]

    return data


def __delete_ignored_paths_from_yaml(api_doc_data: requests.Response, paths_to_delete: list) -> dict:
    data: dict = yaml.safe_load(str(api_doc_data.text))

    for path in paths_to_delete:
        if path in data["paths"]:
            del data["paths"][path]

    return data


def __write_api_doc_to_json(file_path: str, api_doc_data: requests.Response, paths_to_delete: list):
    variables = EnvConfig.get_variables()

    api_doc_data = __delete_ignored_paths_from_json(api_doc_data, paths_to_delete)

    if variables.api_docs_type == "swagger" and not api_doc_data.get("swagger", None):
        api_doc_data["swagger"] = "2.0"

    with open(file_path, "w+") as file:
        file.write(json.dumps(api_doc_data))


def __write_api_doc_to_yaml(file_path: str, api_doc_data: requests.Response, paths_to_delete: list):
    variables = EnvConfig.get_variables()

    data = __delete_ignored_paths_from_yaml(api_doc_data, paths_to_delete)

    if variables.api_docs_type == "swagger" and not data.get("swagger", None):
        data["swagger"] = "2.0"

    with open(file_path, "w+") as file:
        file.write(yaml.safe_dump(data, indent=4, sort_keys=False))


def write_api_doc_to_file(file_path: str, api_doc_data: requests.Response, paths_to_delete: list):
    variables = EnvConfig.get_variables()

    if variables.api_docs_format == "json":
        __write_api_doc_to_json(file_path, api_doc_data, paths_to_delete)
    else:
        __write_api_doc_to_yaml(file_path, api_doc_data, paths_to_delete)
