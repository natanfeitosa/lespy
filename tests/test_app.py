
import pytest

# Importe create_app, Request e call_app do módulo do projeto.


@pytest.mark.parametrize(
    ("registered_methods", "request_method", "expected_status"),
    [
        pytest.param(["GET"], "GET", "200 OK", id="get-allowed"),
        pytest.param(["POST"], "POST", "200 OK", id="post-allowed"),
        pytest.param(["GET"], "POST", "404 Not Found", id="post-not-registered"),
        pytest.param(["POST"], "GET", "404 Not Found", id="get-not-registered"),
        pytest.param(["GET", "POST"], "GET", "200 OK", id="get-multiple-methods"),
        pytest.param(["GET", "POST"], "POST", "200 OK", id="post-multiple-methods"),
    ],
)
def test_route_method_matching(
    registered_methods: list[str],
    request_method: str,
    expected_status: str,
) -> None:
    app = create_app()

    @app.route("/", registered_methods)
    def handler(req: Request) -> bytes:
        return req.method.encode()

    body, status, headers = call_app(app, "/", request_method)

    assert status == expected_status

    if expected_status == "200 OK":
        assert body == request_method.encode()
    else:
        assert body != request_method.encode()