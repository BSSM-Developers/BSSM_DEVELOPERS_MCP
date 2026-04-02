# bssm-dev-mcp

> [한국어 README](README.ko.md)

`bssm-dev-mcp` is an MCP (Model Context Protocol) server for communicating with the [bssm-dev](https://bssm-dev.com) proxy API.
It enables AI agents such as Claude to send requests to registered APIs using a bssm-dev API token.

All requests use **Server-to-Server authentication** via `client_id` and `secret_key`.
Only APIs that are registered on the token and have an `APPROVED` status are allowed.

## Installation

### Step 1 — Install globally (once)

```bash
curl -fsSL https://raw.githubusercontent.com/BSSM-Developers/BSSM_DEVELOPERS_MCP/main/install.sh | sh
```

Installs `uv` if needed, then installs `bssm-dev-mcp` and `bssm-dev-mcp-setup` globally via `uv tool`.

### Step 2 — Register per project

Run this inside any project directory:

```bash
bssm-dev-mcp-setup
```

You will be prompted to enter your Token Client ID, Secret Key, and choose an AI client (Claude Code, Gemini, or OpenCode).

## Configuration

Set the following environment variables before running:

| Variable | Description |
|----------|-------------|
| `BSSM_CLIENT_ID` | bssm-dev API token client ID |
| `BSSM_SECRET_KEY` | bssm-dev API token secret key |

**Claude Desktop config (`claude_desktop_config.json`):**
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

## Available Tools

| Tool | Description |
|------|-------------|
| `get_token_detail` | Retrieve API token details by `client_id` (name, status, allowed origins, registered APIs) |
| `proxy_get` | Send a GET request through the bssm-dev proxy |
| `proxy_post` | Send a POST request through the bssm-dev proxy |
| `proxy_put` | Send a PUT request through the bssm-dev proxy |
| `proxy_patch` | Send a PATCH request through the bssm-dev proxy |
| `proxy_delete` | Send a DELETE request through the bssm-dev proxy |

## How to Use

1. Issue an API token from [bssm-dev](https://bssm-dev.com).
2. Register the APIs you want to use on the token and set their status to `APPROVED`.
3. Set `BSSM_CLIENT_ID` and `BSSM_SECRET_KEY` environment variables.

### Example

```
get_token_detail()

proxy_get(
  path="/student/1/2",
  query_params="{\"page\": \"1\"}"
)
```

## Permission Check

Before each request, the server automatically validates against the registered API list on the token.
- Calls to APIs not in `APPROVED` status are rejected.
- Unregistered paths or methods raise a `PermissionError`.
- Path templates such as `/student/{grade}/{classNum}` are supported.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (for `uvx`)
