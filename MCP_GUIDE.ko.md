# bssm-dev MCP 사용 가이드

본 가이드에서는 AI 에이전트(Claude 등)가 bssm-dev API를 직접 호출할 수 있게 해주는 MCP 서버 설치 및 설정 방법을 다루고 있습니다.
잘 읽어주세요 :)

---

## MCP가 뭔가요?

MCP(Model Context Protocol)는 AI 에이전트가 외부 도구나 서비스를 직접 사용할 수 있게 해주는 표준 프로토콜이에요.

bssm-dev MCP를 설치하면 Claude 같은 AI에게 자연어로 요청하는 것만으로 bssm-dev에 등록된 API를 호출할 수 있어요.

```
1학년 2반 학생 명단 조회해줘.
→ AI가 알아서 proxy_get("/student/1/2") 호출
```

---

## 시작하기 전에

bssm-dev MCP를 사용하려면 **API 토큰**이 필요해요.

1. [bssm-dev](https://bssm-dev.com)에 로그인합니다.
2. 토큰을 발급받고, 사용할 API를 토큰에 등록합니다.
3. 등록한 API를 `APPROVED` 상태로 변경합니다.
4. 발급받은 토큰의 **Client ID**와 **Secret Key**를 메모해두세요.

> 토큰 발급 방법은 [API 사용 가이드](https://bssm-dev.com/docs)를 참고해주세요.

---

## 설치

### 요구사항

- [uv](https://docs.astral.sh/uv/) — Python 패키지 관리 도구 (없으면 설치 스크립트가 자동으로 설치합니다)

### 전역 설치 (최초 1회)

터미널에서 아래 명령어를 실행하세요.

```bash
curl -fsSL https://raw.githubusercontent.com/BSSM-Developers/BSSM_DEVELOPERS_MCP/main/install.sh | sh
```

설치가 완료되면 두 가지 명령어를 사용할 수 있어요.

| 명령어 | 설명 |
|---|---|
| `bssm-dev-mcp` | MCP 서버 실행 파일 |
| `bssm-dev-mcp-setup` | AI 클라이언트 자동 등록 도우미 |

---

## 프로젝트별 셋업

MCP는 **프로젝트(디렉토리)마다** 등록해야 해요. AI 클라이언트에 따라 설정 방법이 달라요.

### Claude Code / Gemini / OpenCode (자동 등록)

사용할 프로젝트 디렉토리로 이동한 뒤 실행하세요.

```bash
bssm-dev-mcp-setup
```

실행하면 순서대로 입력을 요청해요.

```
Token Client ID: [발급받은 Client ID 입력]
Secret Key: [발급받은 Secret Key 입력 — 입력값은 *로 표시됩니다]

AI 클라이언트를 선택하세요:
  1) Claude Code (기본값)
  2) Gemini
  3) OpenCode
선택 [1]:
```

선택하면 해당 클라이언트의 설정 파일에 자동으로 등록됩니다.

> AI 클라이언트를 **재시작**해야 MCP가 활성화돼요.

---

### Claude Desktop (수동 등록)

Claude Desktop은 설정 도우미를 지원하지 않아요. 아래와 같이 직접 설정 파일을 편집하세요.

**설정 파일 경로:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**추가할 내용:**

```json
{
  "mcpServers": {
    "bssm-dev-mcp": {
      "command": "uvx",
      "args": ["bssm-dev-mcp"],
      "env": {
        "BSSM_CLIENT_ID": "발급받은-client-id",
        "BSSM_SECRET_KEY": "발급받은-secret-key"
      }
    }
  }
}
```

저장 후 Claude Desktop을 재시작하면 적용돼요.

---

## 업데이트

새 버전이 출시되면 아래 명령어로 업데이트할 수 있어요.

```bash
uv tool upgrade bssm-dev-mcp
```

업데이트 후 AI 클라이언트를 재시작하면 새 버전이 적용됩니다.

---

## 사용 방법

설치가 완료됐다면 AI에게 자연어로 요청하는 것만으로 API를 호출할 수 있어요.

### 사용 가능한 API 확인

```
지금 사용할 수 있는 API 목록을 알려줘.
```

AI가 토큰에 등록된 API 목록과 각 API의 설명을 정리해서 알려줘요.

### API 호출 예시

```
1학년 2반 학생 명단을 조회해줘.

오늘 급식 메뉴 알려줘.

게시글 제목 "안녕하세요", 내용 "첫 게시글입니다"로 등록해줘.
```

AI가 적절한 API 경로와 파라미터를 알아서 판단하고 호출해요.

---

## 권한 안내

등록된 API 외의 경로나 `APPROVED` 상태가 아닌 API는 호출이 거부돼요.
AI가 요청을 거부할 경우, bssm-dev에서 해당 API의 등록 상태를 확인해보세요.
