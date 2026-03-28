from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisteredApi:
    api_id: str
    name: str
    endpoint: str
    api_method: str
    api_use_state: str


@dataclass(frozen=True)
class ApiTokenDetail:
    api_token_id: int
    api_token_name: str
    api_token_client_id: str
    state: str
    origins: list[str]
    registered_apis: list[RegisteredApi]


class TokenFetcher(ABC):
    """client_id로 API 토큰 상세 정보를 조회하는 추상 클래스."""

    @abstractmethod
    async def fetch(self, client_id: str) -> ApiTokenDetail:
        """client_id에 해당하는 API 토큰 상세 정보를 반환한다."""
        raise NotImplementedError
