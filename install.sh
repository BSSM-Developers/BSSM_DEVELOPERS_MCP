#!/bin/sh
set -e

PACKAGE="bssm-dev-mcp"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { printf "${GREEN}[+]${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}[!]${NC} %s\n" "$*"; }
error() { printf "${RED}[x]${NC} %s\n" "$*" >&2; exit 1; }

# ── uv 확인 및 설치 ───────────────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  info "uv가 없습니다. 설치합니다..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# ── 패키지 전역 설치 ──────────────────────────────────────────────────────────
info "${PACKAGE} 설치 중..."
uv tool install "$PACKAGE" --force

info "설치 완료!"
printf "\n프로젝트 디렉토리에서 아래 명령어로 MCP를 등록하세요:\n"
printf "\n  ${GREEN}bssm-dev-mcp-setup --client-id YOUR_CLIENT_ID --secret-key YOUR_SECRET_KEY${NC}\n\n"
