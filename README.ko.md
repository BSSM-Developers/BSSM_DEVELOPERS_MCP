# bssm-dev-mcp

> [English README](README.md)

`bssm-dev-mcp`는 [bssm-dev](https://bssm-dev.com) proxy API와 통신하는 MCP(Model Context Protocol) 서버입니다.
Claude 등 AI 에이전트가 bssm-dev API 토큰을 통해 등록된 API에 요청을 보낼 수 있도록 합니다.

모든 요청은 `client_id`와 `secret_key`를 사용하는 **Server-to-Server 인증** 방식으로 처리되며,
토큰에 등록되고 `APPROVED` 상태인 API에 대해서만 요청이 허용됩니다.

## 설치 및 실행

실행 전 아래 환경변수를 설정해야 합니다:

| 환경변수 | 설명 |
|----------|------|
| `BSSM_CLIENT_ID` | bssm-dev API 토큰의 client ID |
| `BSSM_SECRET_KEY` | bssm-dev API 토큰의 secret key |

**Claude Desktop 설정 (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "bssm-dev-mcp": {
      "command": "uvx",
      "args": ["bssm-dev-mcp"],
      "env": {
        "BSSM_CLIENT_ID": "your-client-id",
        "BSSM_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

**Claude Code CLI:**
```bash
claude mcp add bssm-dev-mcp uvx bssm-dev-mcp \
  -e BSSM_CLIENT_ID=your-client-id \
  -e BSSM_SECRET_KEY=your-secret-key
```

## 제공 도구 (Tools)

| 도구 | 설명 |
|------|------|
| `get_token_detail` | `client_id`로 API 토큰 상세 정보 조회 (이름, 상태, 허용 도메인, 등록 API 목록) |
| `proxy_get` | bssm-dev proxy 서버에 GET 요청 전송 |
| `proxy_post` | bssm-dev proxy 서버에 POST 요청 전송 |
| `proxy_put` | bssm-dev proxy 서버에 PUT 요청 전송 |
| `proxy_patch` | bssm-dev proxy 서버에 PATCH 요청 전송 |
| `proxy_delete` | bssm-dev proxy 서버에 DELETE 요청 전송 |

## 사용 방법

1. [bssm-dev](https://bssm-dev.com)에서 API 토큰을 발급받습니다.
2. 토큰에 사용할 API를 등록하고 승인(APPROVED) 상태로 설정합니다.
3. `BSSM_CLIENT_ID`와 `BSSM_SECRET_KEY` 환경변수를 설정합니다.

### 예시

```
get_token_detail()

proxy_get(
  path="/student/1/2",
  query_params="{\"page\": \"1\"}"
)
```

## 권한 검사

요청 전 토큰에 등록된 API 목록을 자동으로 확인합니다.
- `APPROVED` 상태가 아닌 API는 호출이 거부됩니다.
- 등록되지 않은 경로 또는 메서드는 `PermissionError`가 발생합니다.
- 경로 템플릿(`/student/{grade}/{classNum}`)을 지원합니다.

## 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`uvx` 사용 시)
