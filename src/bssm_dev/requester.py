import httpx
from typing import Any

from src.core import ProxyRequester


class BssmDevProxyRequester(ProxyRequester):
    """bssm-dev proxy 서버로 실제 HTTP 요청을 전송하는 클래스.

    bssm-dev-token 헤더에 client_id, bssm-dev-secret 헤더에 secret_key를 담아
    proxy 서버(Server-to-Server 모드)로 요청을 전달한다.
    """

    BASE_URL = "https://stg-proxy.bssm-dev.com"

    def __init__(
        self, client_id: str, secret_key: str, base_url: str = BASE_URL
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._client_id = client_id
        self._secret_key = secret_key

    def _build_headers(self) -> dict[str, str]:
        return {
            "bssm-dev-token": self._client_id,
            "bssm-dev-secret": self._secret_key,
            "Content-Type": "application/json",
        }

    def _build_url(self, path: str) -> str:
        return self._base_url + "/" + path.lstrip("/")

    def _parse_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = response.text

        return {
            "status_code": response.status_code,
            "data": data,
        }

    async def get(
        self,
        path: str,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._build_url(path),
                headers=self._build_headers(),
                params=query_params,
            )
        return self._parse_response(response)

    async def post(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._build_url(path),
                headers=self._build_headers(),
                json=body,
                params=query_params,
            )
        return self._parse_response(response)

    async def put(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._build_url(path),
                headers=self._build_headers(),
                json=body,
                params=query_params,
            )
        return self._parse_response(response)

    async def patch(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                self._build_url(path),
                headers=self._build_headers(),
                json=body,
                params=query_params,
            )
        return self._parse_response(response)

    async def delete(
        self,
        path: str,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._build_url(path),
                headers=self._build_headers(),
                params=query_params,
            )
        return self._parse_response(response)
