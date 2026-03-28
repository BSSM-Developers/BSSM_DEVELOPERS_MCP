import re

from src.bssm_dev import BssmDevTokenFetcher
from src.core import RegisteredApi

_token_fetcher = BssmDevTokenFetcher()


def _template_to_pattern(endpoint: str) -> re.Pattern:
    """/student/{grade}/{classNum} → ^/student/[^/]+/[^/]+$ 로 변환한다."""
    escaped = re.escape(endpoint)
    pattern = re.sub(r"\\\{[^}]+\\}", "[^/]+", escaped)
    return re.compile(f"^{pattern}$")


def is_allowed(registered_apis: list[RegisteredApi], method: str, path: str) -> bool:
    """registeredApis 중 APPROVED 상태이고 method·path가 일치하는 항목이 있으면 True."""
    request_path = path.split("?")[0].rstrip("/") or "/"
    for api in registered_apis:
        if api.api_use_state != "APPROVED":
            continue
        if api.api_method.upper() != method.upper():
            continue
        if _template_to_pattern(api.endpoint).match(request_path):
            return True
    return False


async def check_permission(client_id: str, method: str, path: str) -> None:
    """허용되지 않은 요청이면 PermissionError를 발생시킨다."""
    token_detail = await _token_fetcher.fetch(client_id)
    if not is_allowed(token_detail.registered_apis, method, path):
        approved = [
            f"{a.api_method} {a.endpoint} ({a.name})"
            for a in token_detail.registered_apis
            if a.api_use_state == "APPROVED"
        ]
        raise PermissionError(
            f"'{method} {path}' 요청은 허용되지 않습니다. "
            f"승인된 API 목록: {approved if approved else '없음'}"
        )
