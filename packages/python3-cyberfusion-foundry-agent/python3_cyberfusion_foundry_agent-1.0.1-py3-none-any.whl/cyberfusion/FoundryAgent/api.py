import requests
from requests.adapters import HTTPAdapter, Retry
from typing import Any


class APIClient:
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def call(
        self,
        method: str,
        path: str,
        *,
        parameters: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        session = requests.Session()

        adapter = HTTPAdapter(
            max_retries=Retry(
                total=10,
                backoff_factor=2.5,
                allowed_methods=None,
            )
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.request(
            method,
            self.api_url + "/" + path,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            params=parameters,
            json=json,
            timeout=30,
        )

        response.raise_for_status()

        return response.text
