from requests import Response

from autotests_coverage.results_writers.base_schemas_manager import ApiDocsManagerBase
from autotests_coverage.uri import URI


class OpenApiSchemasManager(ApiDocsManagerBase):
    def __init__(self, uri: URI, method: str, response: Response, kwargs: dict):
        super().__init__(uri, response, kwargs, method)

    def _paths(self):
        path_ = self._uri.raw.split("?")[0]
        params = (
            self._get_path_params()
            + self._get_query_params()
            + self._get_header_params()
        )
        dict_ = {
            path_: {
                self._method: {
                    "parameters": params,
                    "responses": {self._response.status_code: {}},
                }
            }
        }

        body_params = self._get_body_params()

        if body_params:
            dict_[path_][self._method]["requestBody"] = body_params

        return dict_

    def _get_schema(self):
        schema_dict = {
            self.variables.api_docs_type: self.variables.api_docs_version,
            "info": {"title": "Recorded Request"},
            "paths": self._paths(),
        }

        return schema_dict
