import httpx

from src.core import ApiTokenDetail, RegisteredApi, TokenFetcher

BSSM_DEV_BASE_URL = "https://staging.bssm-dev.com"


class BssmDevTokenFetcher(TokenFetcher):
    """https://staging.bssm-dev.com/api/token/client/{client-id} 로 토큰 상세를 조회한다."""

    def __init__(self, base_url: str = BSSM_DEV_BASE_URL) -> None:
        self._base_url = base_url.rstrip("/")

    async def fetch(self, client_id: str) -> ApiTokenDetail:
        url = f"{self._base_url}/api/token/client/{client_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        payload = response.json()
        data = payload["data"]

        registered_apis = [
            RegisteredApi(
                api_id=api["apiId"],
                name=api["name"],
                endpoint=api["endpoint"],
                api_method=api["apiMethod"],
                api_use_state=api["apiUseState"],
            )
            for api in data.get("registeredApis", [])
        ]

        return ApiTokenDetail(
            api_token_id=data["apiTokenId"],
            api_token_name=data["apiTokenName"],
            api_token_client_id=data["apiTokenClientId"],
            state=data["state"],
            origins=data.get("origins", []),
            registered_apis=registered_apis,
        )
