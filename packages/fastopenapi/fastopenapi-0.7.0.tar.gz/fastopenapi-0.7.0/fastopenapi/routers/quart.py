import re
from collections.abc import Callable

from quart import Response, jsonify, request

from fastopenapi.base_router import BaseRouter


class QuartRouter(BaseRouter):
    def add_route(self, path: str, method: str, endpoint: Callable):
        super().add_route(path, method, endpoint)
        if self.app is not None:
            quart_path = re.sub(r"{(\w+)}", r"<\1>", path)

            async def view_func(**path_params):
                json_data = await request.get_json(silent=True) or {}
                query_params = {}
                for key in request.args:
                    values = request.args.getlist(key)
                    query_params[key] = values[0] if len(values) == 1 else values
                all_params = {**query_params, **path_params}
                body = json_data
                try:
                    kwargs = self.resolve_endpoint_params(endpoint, all_params, body)
                except Exception as e:
                    error_response = self.handle_exception(e)
                    return jsonify(error_response), getattr(e, "status_code", 422)
                try:
                    result = await endpoint(**kwargs)
                except Exception as e:
                    error_response = self.handle_exception(e)
                    return jsonify(error_response), getattr(e, "code", 500)

                meta = getattr(endpoint, "__route_meta__", {})
                status_code = meta.get("status_code", 200)
                result = self._serialize_response(result)
                return jsonify(result), status_code

            self.app.add_url_rule(
                quart_path, endpoint.__name__, view_func, methods=[method.upper()]
            )

    def _register_docs_endpoints(self):
        @self.app.route(self.openapi_url, methods=["GET"])
        async def openapi_view():
            return jsonify(self.openapi)

        @self.app.route(self.docs_url, methods=["GET"])
        async def docs_view():
            html = self.render_swagger_ui(self.openapi_url)
            return Response(html, mimetype="text/html")

        @self.app.route(self.redoc_url, methods=["GET"])
        async def redoc_view():
            html = self.render_redoc_ui(self.openapi_url)
            return Response(html, mimetype="text/html")
