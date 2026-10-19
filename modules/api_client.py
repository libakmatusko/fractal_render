"""Small standard-library JSON API client."""

import json
from typing import Any
from urllib.request import Request, urlopen


def get_json(url: str) -> Any:
    """Fetch and decode a JSON response from a URL."""
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))
