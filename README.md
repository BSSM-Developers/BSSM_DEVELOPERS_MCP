# bssm-dev-mcp

Claude 등 AI 에이전트가 [bssm-dev](https://bssm-dev.com) 프록시 API를 직접 호출할 수 있게 해주는 MCP(Model Context Protocol) 서버입니다.

API 토큰의 `client_id`와 `secret_key`를 환경변수로 설정하면, AI가 토큰에 등록된 API를 자동으로 파악하고 요청을 대신 전송합니다.

---

## 설치

### 요구사항

- [uv](https://docs.astral.sh/uv/) (없으면 설치 스크립트가 자동으로 설치합니다)

### Step 1 — 전역 설치 (최초 1회)

```bash
curl -fsSL https://raw.githubusercontent.com/BSSM-Developers/BSSM_DEVELOPERS_MCP/main/install.sh | sh
```

`bssm-dev-mcp`와 설정 도우미 `bssm-dev-mcp-setup`이 전역으로 설치됩니다.

### Step 2 — 프로젝트에 MCP 등록

사용할 프로젝트 디렉토리 안에서 실행합니다:

```bash
bssm-dev-mcp-setup
```

Token Client ID, Secret Key를 입력하고 AI 클라이언트를 선택하면 자동으로 설정 파일에 등록됩니다.

> **지원 클라이언트:** Claude Code · Gemini · OpenCode
>
> Claude Desktop은 설정 도우미를 지원하지 않습니다. [수동 설정](#수동-설정)을 사용하세요.

### 업데이트

```bash
uv tool upgrade bssm-dev-mcp
```

업데이트 후 AI 클라이언트를 재시작하면 새 버전이 적용됩니다.

---

## 수동 설정

`bssm-dev-mcp-setup` 대신 직접 설정 파일을 편집할 수도 있습니다.

**Claude Code:**
```bash
claude mcp add bssm-dev-mcp uvx bssm-dev-mcp \
  -e BSSM_CLIENT_ID=your-client-id \
  -e BSSM_SECRET_KEY=your-secret-key
```

**Claude Desktop (`claude_desktop_config.json`):**
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

| 환경변수 | 설명 |
|---|---|
| `BSSM_CLIENT_ID` | bssm-dev API 토큰의 Client ID |
| `BSSM_SECRET_KEY` | bssm-dev API 토큰의 Secret Key |

---

## 사용 방법

1. [bssm-dev](https://bssm-dev.com)에서 API 토큰을 발급받습니다.
2. 토큰에 사용할 API를 등록하고 `APPROVED` 상태로 설정합니다.
3. 위 설치 과정을 마치면 AI 클라이언트에서 바로 사용할 수 있습니다.

AI에게 자연어로 요청하면 됩니다:

```
현재 사용 가능한 API 목록을 알려줘.

1학년 2반 학생 명단을 조회해줘.
```

---

## 제공 도구 (Tools)

### `get_token_detail`

토큰에 등록된 API 목록, 인증 방법, 허용 도메인 등 상세 정보를 조회합니다.
AI가 어떤 API를 어떻게 호출할 수 있는지 파악할 때 사용됩니다.

```
get_token_detail()
```

### `proxy_get` / `proxy_post` / `proxy_put` / `proxy_patch` / `proxy_delete`

각 HTTP 메서드로 bssm-dev 프록시를 통해 API를 호출합니다.

```
proxy_get(
  path="/student/1/2",
  query_params="{\"page\": \"1\"}"
)

proxy_post(
  path="/api/posts",
  body="{\"title\": \"안녕하세요\", \"content\": \"내용입니다\"}"
)
```

| 파라미터 | 설명 |
|---|---|
| `path` | API 경로 (예: `/student/1/2/3`) |
| `body` | JSON 형식의 요청 바디 (POST·PUT·PATCH) |
| `query_params` | JSON 형식의 쿼리 파라미터 |

### `proxy_stream`

업스트림 API가 SSE(Server-Sent Events)를 반환할 때 사용합니다.
`Accept: text/event-stream` 헤더를 포함하여 요청하고, 수신된 이벤트를 모아 반환합니다. (최대 60초)

```
proxy_stream(
  method="GET",
  path="/api/chat/stream",
  body="{\"prompt\": \"안녕하세요\"}"
)
```

| 파라미터 | 설명 |
|---|---|
| `method` | HTTP 메서드 (GET, POST 등) |
| `path` | API 경로 |
| `body` | JSON 형식의 요청 바디 |
| `query_params` | JSON 형식의 쿼리 파라미터 |

---

## 권한 검사

모든 요청은 프록시로 전달되기 전에 토큰의 등록 API 목록을 자동으로 확인합니다.

- `APPROVED` 상태가 아닌 API 호출은 거부됩니다.
- 등록되지 않은 경로 또는 메서드는 `PermissionError`가 발생하며 승인된 API 목록을 함께 알려줍니다.
- 경로 템플릿(`/student/{grade}/{classNum}`)을 지원합니다.

---

## 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
