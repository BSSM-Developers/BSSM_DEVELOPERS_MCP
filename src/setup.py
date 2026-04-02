import json
import os
import shutil
import subprocess
import sys
import termios
import tty

SERVER_NAME = "bssm-dev-mcp"

GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
NC = "\033[0m"


def info(msg: str) -> None:
    print(f"{GREEN}[+]{NC} {msg}")


def error(msg: str) -> None:
    print(f"{RED}[x]{NC} {msg}", file=sys.stderr)
    sys.exit(1)


def _get_mcp_command() -> str:
    cmd = shutil.which(SERVER_NAME)
    if not cmd:
        error(f"{SERVER_NAME} 실행 파일을 찾을 수 없습니다. 먼저 설치하세요: uv tool install bssm-dev-mcp")
    return cmd  # type: ignore[return-value]


def _select_client() -> str:
    print(f"\n{CYAN}AI 클라이언트를 선택하세요:{NC}")
    print("  1) Claude Code (기본값)")
    print("  2) Gemini")
    print("  3) OpenCode")
    try:
        choice = input("선택 [1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    clients = {"1": "claude", "2": "gemini", "3": "opencode"}
    if choice not in clients:
        error("올바른 번호를 입력하세요 (1-3)")
    return clients[choice]


def _register_claude(command: str, client_id: str, secret_key: str) -> None:
    if not shutil.which("claude"):
        error("claude CLI가 없습니다. Claude Code를 먼저 설치해주세요.")
    subprocess.run(["claude", "mcp", "remove", SERVER_NAME], capture_output=True)
    result = subprocess.run([
        "claude", "mcp", "add", SERVER_NAME, command,
        "-e", f"BSSM_CLIENT_ID={client_id}",
        "-e", f"BSSM_SECRET_KEY={secret_key}",
    ])
    if result.returncode != 0:
        error("claude mcp add 실패")
    info("등록 완료:")
    subprocess.run(["claude", "mcp", "list"])


def _update_json(path: str, updater: "callable") -> None:  # type: ignore[type-arg]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    config: dict = {}
    if os.path.exists(path):
        with open(path) as f:
            config = json.load(f)
    updater(config)
    with open(path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    info(f"저장됨: {path}")


def _register_gemini(command: str, client_id: str, secret_key: str) -> None:
    path = os.path.expanduser("~/.gemini/settings.json")

    def update(config: dict) -> None:
        config.setdefault("mcpServers", {})[SERVER_NAME] = {
            "command": command,
            "args": [],
            "env": {"BSSM_CLIENT_ID": client_id, "BSSM_SECRET_KEY": secret_key},
        }

    _update_json(path, update)


def _register_opencode(command: str, client_id: str, secret_key: str) -> None:
    path = os.path.expanduser("~/.config/opencode/opencode.json")

    def update(config: dict) -> None:
        config.setdefault("mcp", {})[SERVER_NAME] = {
            "type": "local",
            "command": [command],
            "environment": {"BSSM_CLIENT_ID": client_id, "BSSM_SECRET_KEY": secret_key},
            "enabled": True,
        }

    _update_json(path, update)


def _masked_input(label: str) -> str:
    sys.stdout.write(f"{label}: ")
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    chars: list[str] = []
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                break
            if ch == "\x03":  # Ctrl+C
                raise KeyboardInterrupt
            if ch in ("\x7f", "\x08"):  # backspace
                if chars:
                    chars.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                chars.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write("\n")
    return "".join(chars)


def _prompt(label: str, env_key: str, secret: bool = False) -> str:
    default = os.environ.get(env_key, "")
    try:
        if secret:
            value = _masked_input(label).strip()
        else:
            value = input(f"{label}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    value = value or default
    if not value:
        error(f"{label}을(를) 입력해주세요.")
    return value


def main() -> None:
    client_id = _prompt("Token Client ID", "BSSM_CLIENT_ID")
    secret_key = _prompt("Secret Key", "BSSM_SECRET_KEY", secret=True)
    client = _select_client()
    command = _get_mcp_command()

    if client == "claude":
        _register_claude(command, client_id, secret_key)
    elif client == "gemini":
        _register_gemini(command, client_id, secret_key)
    elif client == "opencode":
        _register_opencode(command, client_id, secret_key)

    info("완료!")
