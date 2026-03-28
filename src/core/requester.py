from abc import ABC, abstractmethod
from typing import Any


class ProxyRequester(ABC):
    """bssm-dev proxy API 요청을 위한 추상 클래스."""

    @abstractmethod
    async def get(
        self,
        path: str,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET 요청을 프록시 서버로 전달한다."""
        raise NotImplementedError

    @abstractmethod
    async def post(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """POST 요청을 프록시 서버로 전달한다."""
        raise NotImplementedError

    @abstractmethod
    async def put(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """PUT 요청을 프록시 서버로 전달한다."""
        raise NotImplementedError

    @abstractmethod
    async def patch(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """PATCH 요청을 프록시 서버로 전달한다."""
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        path: str,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """DELETE 요청을 프록시 서버로 전달한다."""
        raise NotImplementedError
