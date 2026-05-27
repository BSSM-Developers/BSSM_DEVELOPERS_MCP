# bssm-dev-mcp

> [한국어 README](README.ko.md)

An MCP (Model Context Protocol) server that lets AI agents like Claude call [bssm-dev](https://bssm-dev.com) proxy APIs directly.

Set your API token's `client_id` and `secret_key` as environment variables, and the AI will automatically discover the registered APIs and send requests on your behalf.

---

## Installation

### Requirements

- [uv](https://docs.astral.sh/uv/) (auto-installed by the install script if missing)

### Step 1 — Install globally (once)

```bash
curl -fsSL https://raw.githubusercontent.com/BSSM-Developers/BSSM_DEVELOPERS_MCP/main/install.sh | sh
```

This installs `bssm-dev-mcp` and the setup helper `bssm-dev-mcp-setup` globally.

### Step 2 — Register per project

Run this inside your project directory:

```bash
bssm-dev-mcp-setup
```

Enter your Token Client ID and Secret Key, then choose your AI client. The tool writes the config automatically.

> **Supported clients:** Claude Code · Claude Desktop · Gemini · OpenCode

### Updating

```bash
uv tool upgrade bssm-dev-mcp
```

Restart your AI client after upgrading to apply the new version.

---

## Manual Configuration

You can also edit config files directly instead of using `bssm-dev-mcp-setup`.

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

| Variable | Description |
|---|---|
| `BSSM_CLIENT_ID` | bssm-dev API token Client ID |
| `BSSM_SECRET_KEY` | bssm-dev API token Secret Key |

---

## Usage

1. Issue an API token from [bssm-dev](https://bssm-dev.com).
2. Register the APIs you want to use on the token and set them to `APPROVED`.
3. Complete the installation above — your AI client is ready to use.

Just ask in natural language:

```
Show me the list of available APIs.

Fetch the student roster for grade 1, class 2.
```

---

## Available Tools

### `get_token_detail`

Retrieves the list of APIs registered on the token, authentication instructions, and allowed origins.
Used by the AI to understand which APIs are available and how to call them.

```
get_token_detail()
```

### `proxy_get` / `proxy_post` / `proxy_put` / `proxy_patch` / `proxy_delete`

Calls an API through the bssm-dev proxy using the corresponding HTTP method.

```
proxy_get(
  path="/student/1/2",
  query_params="{\"page\": \"1\"}"
)

proxy_post(
  path="/api/posts",
  body="{\"title\": \"Hello\", \"content\": \"World\"}"
)
```

| Parameter | Description |
|---|---|
| `path` | API path (e.g. `/student/1/2/3`) |
| `body` | JSON request body (POST · PUT · PATCH) |
| `query_params` | JSON query parameters |

### `proxy_stream`

Use this when the upstream API returns SSE (Server-Sent Events).
Sends the request with an `Accept: text/event-stream` header and returns all received events. (up to 60 seconds)

```
proxy_stream(
  method="GET",
  path="/api/chat/stream",
  body="{\"prompt\": \"Hello\"}"
)
```

| Parameter | Description |
|---|---|
| `method` | HTTP method (GET, POST, etc.) |
| `path` | API path |
| `body` | JSON request body |
| `query_params` | JSON query parameters |

---

## Permission Check

Every request is validated against the token's registered API list before being forwarded to the proxy.

- Requests to APIs not in `APPROVED` status are rejected.
- Unregistered paths or methods raise a `PermissionError` along with a list of approved APIs.
- Path templates such as `/student/{grade}/{classNum}` are supported.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
