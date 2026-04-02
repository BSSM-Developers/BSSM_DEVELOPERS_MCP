import json
import os
from typing import Any

from fastmcp import FastMCP

from src.bssm_dev import BssmDevProxyRequester, BssmDevTokenFetcher
from src.mcp.permission import check_permission

PROXY_BASE_URL = "https://proxy.bssm-dev.com"

mcp = FastMCP(
    name="bssm-dev-mcp",
    instructions=(
        "bssm-dev proxy API 서버와 통신하는 MCP 서버입니다. "
        "인증 정보는 환경변수 BSSM_CLIENT_ID, BSSM_SECRET_KEY로 설정됩니다. "
        "요청 전에 토큰에 등록된 API(registeredApis) 목록을 확인하여 "
        "허용된 엔드포인트와 메서드에만 요청을 전송합니다."
    ),
)

_token_fetcher = BssmDevTokenFetcher()


def _get_credentials() -> tuple[str, str]:
    client_id = os.environ.get("BSSM_CLIENT_ID", "")
    secret_key = os.environ.get("BSSM_SECRET_KEY", "")
    if not client_id or not secret_key:
        raise RuntimeError(
            "BSSM_CLIENT_ID와 BSSM_SECRET_KEY 환경변수를 설정해주세요."
        )
    return client_id, secret_key


def _get_requester() -> BssmDevProxyRequester:
    client_id, secret_key = _get_credentials()
    return BssmDevProxyRequester(
        base_url=PROXY_BASE_URL,
        client_id=client_id,
        secret_key=secret_key,
    )


def _format_result(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_token_detail() -> str:
    """환경변수에 설정된 토큰의 상세 정보를 조회한다.

    토큰 이름, 상태, 허용 도메인(origins), 등록된 API 목록(registeredApis)을 반환한다.
    """
    client_id, _ = _get_credentials()
    token_detail = await _token_fetcher.fetch(client_id)
    result = {
        "proxyBaseUrl": PROXY_BASE_URL,
        "apiTokenId": token_detail.api_token_id,
        "apiTokenName": token_detail.api_token_name,
        "apiTokenClientId": token_detail.api_token_client_id,
        "state": token_detail.state,
        "origins": token_detail.origins,
        "registeredApis": [
            {
                "apiId": api.api_id,
                "name": api.name,
                "endpoint": api.endpoint,
                "fullUrl": f"{PROXY_BASE_URL}{api.endpoint}",
                "apiMethod": api.api_method,
                "apiUseState": api.api_use_state,
            }
            for api in token_detail.registered_apis
        ],
    }
    return _format_result(result)


@mcp.tool()
async def proxy_get(
    path: str,
    query_params: str = "{}",
) -> str:
    """bssm-dev proxy 서버에 GET 요청을 전송한다.

    토큰에 등록된 registeredApis 중 APPROVED 상태인 GET 엔드포인트에만 요청할 수 있다.

    Args:
        path: 요청할 API 경로 (예: /student/1/2/3)
        query_params: JSON 형식의 쿼리 파라미터 (예: {"page": "1", "size": "10"})
    """
    client_id, _ = _get_credentials()
    await check_permission(client_id, "GET", path)
    params: dict[str, str] = json.loads(query_params) if query_params.strip() else {}
    result = await _get_requester().get(path=path, query_params=params or None)
    return _format_result(result)


@mcp.tool()
async def proxy_post(
    path: str,
    body: str = "{}",
    query_params: str = "{}",
) -> str:
    """bssm-dev proxy 서버에 POST 요청을 전송한다.

    토큰에 등록된 registeredApis 중 APPROVED 상태인 POST 엔드포인트에만 요청할 수 있다.

    Args:
        path: 요청할 API 경로 (예: /api/posts)
        body: JSON 형식의 요청 바디 (예: {"title": "Hello", "content": "World"})
        query_params: JSON 형식의 쿼리 파라미터
    """
    client_id, _ = _get_credentials()
    await check_permission(client_id, "POST", path)
    req_body: dict[str, Any] = json.loads(body) if body.strip() else {}
    params: dict[str, str] = json.loads(query_params) if query_params.strip() else {}
    result = await _get_requester().post(
        path=path,
        body=req_body or None,
        query_params=params or None,
    )
    return _format_result(result)


@mcp.tool()
async def proxy_put(
    path: str,
    body: str = "{}",
    query_params: str = "{}",
) -> str:
    """bssm-dev proxy 서버에 PUT 요청을 전송한다.

    토큰에 등록된 registeredApis 중 APPROVED 상태인 PUT 엔드포인트에만 요청할 수 있다.

    Args:
        path: 요청할 API 경로 (예: /api/posts/1)
        body: JSON 형식의 요청 바디 (예: {"title": "Updated"})
        query_params: JSON 형식의 쿼리 파라미터
    """
    client_id, _ = _get_credentials()
    await check_permission(client_id, "PUT", path)
    req_body: dict[str, Any] = json.loads(body) if body.strip() else {}
    params: dict[str, str] = json.loads(query_params) if query_params.strip() else {}
    result = await _get_requester().put(
        path=path,
        body=req_body or None,
        query_params=params or None,
    )
    return _format_result(result)


@mcp.tool()
async def proxy_patch(
    path: str,
    body: str = "{}",
    query_params: str = "{}",
) -> str:
    """bssm-dev proxy 서버에 PATCH 요청을 전송한다.

    토큰에 등록된 registeredApis 중 APPROVED 상태인 PATCH 엔드포인트에만 요청할 수 있다.

    Args:
        path: 요청할 API 경로 (예: /api/posts/1)
        body: JSON 형식의 요청 바디 (예: {"title": "Partial Update"})
        query_params: JSON 형식의 쿼리 파라미터
    """
    client_id, _ = _get_credentials()
    await check_permission(client_id, "PATCH", path)
    req_body: dict[str, Any] = json.loads(body) if body.strip() else {}
    params: dict[str, str] = json.loads(query_params) if query_params.strip() else {}
    result = await _get_requester().patch(
        path=path,
        body=req_body or None,
        query_params=params or None,
    )
    return _format_result(result)


@mcp.tool()
async def proxy_delete(
    path: str,
    query_params: str = "{}",
) -> str:
    """bssm-dev proxy 서버에 DELETE 요청을 전송한다.

    토큰에 등록된 registeredApis 중 APPROVED 상태인 DELETE 엔드포인트에만 요청할 수 있다.

    Args:
        path: 요청할 API 경로 (예: /api/posts/1)
        query_params: JSON 형식의 쿼리 파라미터
    """
    client_id, _ = _get_credentials()
    await check_permission(client_id, "DELETE", path)
    params: dict[str, str] = json.loads(query_params) if query_params.strip() else {}
    result = await _get_requester().delete(path=path, query_params=params or None)
    return _format_result(result)


def main() -> None:
    from src.mcp.banner import print_banner
    print_banner()
    mcp.run(show_banner=False)
