#!/bin/sh
set -e

PACKAGE="bssm-dev-mcp"
SERVER_NAME="bssm-dev-mcp"

# ── 색상 ──────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { printf "${GREEN}[+]${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}[!]${NC} %s\n" "$*"; }
error() { printf "${RED}[x]${NC} %s\n" "$*" >&2; exit 1; }

# ── 인자 파싱 ─────────────────────────────────────────────────────────────────
CLIENT_ID="${BSSM_CLIENT_ID:-}"
SECRET_KEY="${BSSM_SECRET_KEY:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --client-id)  CLIENT_ID="$2";  shift 2 ;;
    --secret-key) SECRET_KEY="$2"; shift 2 ;;
    *) error "알 수 없는 옵션: $1" ;;
  esac
done

# ── 자격증명 확인 ─────────────────────────────────────────────────────────────
if [ -z "$CLIENT_ID" ] || [ -z "$SECRET_KEY" ]; then
  echo ""
  echo "사용법:"
  echo "  curl -fsSL https://raw.githubusercontent.com/BSSM-Developers/BSSM_DEVELOPERS_MCP/main/install.sh \\"
  echo "    | sh -s -- --client-id <CLIENT_ID> --secret-key <SECRET_KEY>"
  echo ""
  echo "또는 환경변수로 전달:"
  echo "  BSSM_CLIENT_ID=xxx BSSM_SECRET_KEY=xxx \\"
  echo "    curl -fsSL ... | sh"
  echo ""
  error "BSSM_CLIENT_ID와 BSSM_SECRET_KEY가 필요합니다."
fi

# ── AI 클라이언트 선택 ────────────────────────────────────────────────────────
printf "\n${CYAN}AI 클라이언트를 선택하세요:${NC}\n"
printf "  1) Claude Code (기본값)\n"
printf "  2) Gemini\n"
printf "  3) OpenCode\n"
printf "선택 [1]: "
read -r CHOICE </dev/tty
CHOICE="${CHOICE:-1}"

case "$CHOICE" in
  1|"") CLIENT="claude" ;;
  2)    CLIENT="gemini" ;;
  3)    CLIENT="opencode" ;;
  *)    error "올바른 번호를 입력하세요 (1-3)" ;;
esac

# ── uv 확인 및 설치 ───────────────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  info "uv가 없습니다. 설치합니다..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# ── 패키지 설치 ───────────────────────────────────────────────────────────────
info "${PACKAGE} 설치 중..."
uv tool install "$PACKAGE" --force

COMMAND="$(uv tool dir)/bin/${SERVER_NAME}"
if [ ! -f "$COMMAND" ]; then
  COMMAND="$(command -v $SERVER_NAME 2>/dev/null || true)"
fi
[ -z "$COMMAND" ] && error "설치 후 실행 파일을 찾을 수 없습니다."

# ── 클라이언트별 MCP 등록 ─────────────────────────────────────────────────────

register_claude() {
  if ! command -v claude >/dev/null 2>&1; then
    warn "claude CLI가 없습니다. 수동으로 연결하세요:"
    printf "\n  claude mcp add %s \"%s\" \\\\\n    -e BSSM_CLIENT_ID=%s \\\\\n    -e BSSM_SECRET_KEY=%s\n\n" \
      "$SERVER_NAME" "$COMMAND" "$CLIENT_ID" "$SECRET_KEY"
    return
  fi
  info "Claude Code MCP 서버 등록 중..."
  claude mcp remove "$SERVER_NAME" 2>/dev/null || true
  claude mcp add "$SERVER_NAME" "$COMMAND" \
    -e BSSM_CLIENT_ID="$CLIENT_ID" \
    -e BSSM_SECRET_KEY="$SECRET_KEY"
  info "등록 완료:"
  claude mcp list
}

register_gemini() {
  CONFIG_DIR="$HOME/.gemini"
  CONFIG_FILE="$CONFIG_DIR/settings.json"
  mkdir -p "$CONFIG_DIR"

  info "Gemini 설정 파일 업데이트 중... ($CONFIG_FILE)"
  python3 - <<PYEOF
import json, os

path = "$CONFIG_FILE"
config = {}
if os.path.exists(path):
    with open(path) as f:
        config = json.load(f)

config.setdefault("mcpServers", {})
config["mcpServers"]["$SERVER_NAME"] = {
    "command": "$COMMAND",
    "args": [],
    "env": {
        "BSSM_CLIENT_ID": "$CLIENT_ID",
        "BSSM_SECRET_KEY": "$SECRET_KEY"
    }
}

with open(path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("  저장됨:", path)
PYEOF
}

register_opencode() {
  CONFIG_DIR="$HOME/.config/opencode"
  CONFIG_FILE="$CONFIG_DIR/opencode.json"
  mkdir -p "$CONFIG_DIR"

  info "OpenCode 설정 파일 업데이트 중... ($CONFIG_FILE)"
  python3 - <<PYEOF
import json, os

path = "$CONFIG_FILE"
config = {}
if os.path.exists(path):
    with open(path) as f:
        config = json.load(f)

config.setdefault("mcp", {})
config["mcp"]["$SERVER_NAME"] = {
    "type": "local",
    "command": ["$COMMAND"],
    "environment": {
        "BSSM_CLIENT_ID": "$CLIENT_ID",
        "BSSM_SECRET_KEY": "$SECRET_KEY"
    },
    "enabled": True
}

with open(path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("  저장됨:", path)
PYEOF
}

# ── 실행 ──────────────────────────────────────────────────────────────────────
case "$CLIENT" in
  claude)   register_claude ;;
  gemini)   register_gemini ;;
  opencode) register_opencode ;;
esac

info "완료!"
