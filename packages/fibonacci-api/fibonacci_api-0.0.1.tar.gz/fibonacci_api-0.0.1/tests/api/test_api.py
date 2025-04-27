"""Open-api property-based testing.

[Docs](https://schemathesis.readthedocs.io/en/stable/index.html)
"""

import schemathesis
from schemathesis.specs.openapi.loaders import from_asgi

from fibonacci_api.main import app

# Globally enable OpenAPI 3.1 experimental feature
schemathesis.experimental.OPEN_API_3_1.enable()

schema = from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api(case):
    response = case.call_asgi()
    case.validate_response(response)
