from rich.align import Align
from rich.console import Console
from rich.text import Text

BSSM = """\
▛▀▖ ▞▀▖ ▞▀▖ ▙▗▌
▙▄▘ ▚▄  ▚▄  ▌▘▌
▌ ▌ ▖ ▌ ▖ ▌ ▌ ▌
▀▀  ▝▀  ▝▀  ▘ ▘\
"""

DEVELOPERS = """\
▛▀▖             ▜
▌ ▌ ▞▀▖ ▌ ▌ ▞▀▖ ▐  ▞▀▖ ▛▀▖ ▞▀▖ ▙▀▖ ▞▀▘
▌ ▌ ▛▀  ▐▐  ▛▀  ▐  ▌ ▌ ▙▄▘ ▛▀  ▌   ▝▀▖
▀▀  ▝▀▘  ▘  ▝▀▘  ▘ ▝▀  ▌   ▝▀▘ ▘   ▀▀ \
"""

MCP = """\
▙▗▌ ▞▀▖ ▛▀▖
▌▘▌ ▌   ▙▄▘
▌ ▌ ▌ ▖ ▌
▘ ▘ ▝▀  ▘  \
"""

BORDER_PERIOD = 32


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _bssm_color(t: float) -> tuple[int, int, int]:
    stops = [
        (255, 30, 30),
        (40, 80, 255),
        (255, 220, 30),
        (150, 255, 210),
    ]
    n = len(stops) - 1
    pos = t * n
    i = min(int(pos), n - 1)
    lt = pos - i
    return (
        _lerp(stops[i][0], stops[i + 1][0], lt),
        _lerp(stops[i][1], stops[i + 1][1], lt),
        _lerp(stops[i][2], stops[i + 1][2], lt),
    )


def _mcp_color(t: float) -> tuple[int, int, int]:
    return (
        _lerp(0, 170, t),
        _lerp(210, 80, t),
        _lerp(255, 255, t),
    )


def _border_color(pos: int) -> tuple[int, int, int]:
    return _bssm_color((pos % BORDER_PERIOD) / BORDER_PERIOD)


def _colorize_line(line: str, max_col: int, color_fn) -> Text:
    text = Text(no_wrap=True)
    for col, ch in enumerate(line):
        r, g, b = color_fn(col / max_col if max_col else 0)
        text.append(ch, style=f"bold #{r:02x}{g:02x}{b:02x}")
    return text


def print_banner() -> None:
    console = Console(stderr=True, highlight=False)

    bssm_lines = BSSM.split("\n")
    devs_lines = DEVELOPERS.split("\n")
    mcp_lines = MCP.split("\n")

    content_width = max(
        max(len(l) for l in bssm_lines),
        max(len(l) for l in devs_lines),
        max(len(l) for l in mcp_lines),
    )
    bssm_max = max(len(l) for l in bssm_lines)
    devs_max = max(len(l) for l in devs_lines)
    mcp_max = max(len(l) for l in mcp_lines)

    terminal_w = console.width or 80
    inner_w = terminal_w - 2  # subtract border chars
    h_pad = (inner_w - content_width) // 2
    counter = [0]

    def next_border(ch: str) -> Text:
        t = Text(no_wrap=True)
        r, g, b = _border_color(counter[0])
        counter[0] += 1
        t.append(ch, style=f"bold #{r:02x}{g:02x}{b:02x}")
        return t

    def border_row(chars: str) -> Text:
        t = Text(no_wrap=True)
        for ch in chars:
            r, g, b = _border_color(counter[0])
            counter[0] += 1
            t.append(ch, style=f"bold #{r:02x}{g:02x}{b:02x}")
        return t

    def content_row(content: Text, raw_len: int) -> Text:
        line = Text(no_wrap=True)
        line.append_text(next_border("│"))
        line.append(" " * h_pad)
        line.append_text(content)
        line.append(" " * (content_width - raw_len + h_pad))
        line.append_text(next_border("│"))
        return line

    def empty_row() -> Text:
        return content_row(Text("", no_wrap=True), 0)

    output = []
    output.append(border_row("╭" + "─" * inner_w + "╮"))
    output.append(empty_row())

    for line in bssm_lines:
        output.append(content_row(_colorize_line(line, bssm_max, _bssm_color), len(line)))

    output.append(empty_row())
    output.append(empty_row())

    for line in devs_lines:
        output.append(content_row(Text(line, style="bold #1a237e", no_wrap=True), len(line)))

    output.append(empty_row())
    output.append(empty_row())

    for line in mcp_lines:
        output.append(content_row(_colorize_line(line, mcp_max, _mcp_color), len(line)))

    output.append(empty_row())
    output.append(border_row("╰" + "─" * inner_w + "╯"))

    console.print()
    for line in output:
        console.print(line)
    console.print()
