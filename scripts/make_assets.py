"""生成首页 README 用的 SVG 素材（头图 / 终端面板 / 状态徽标），亮暗两套。

只依赖标准库：改这里的文字或配色后重跑即可，不用 PS、不用联网：

    python scripts/make_assets.py

产出（全部落在 assets/）：
    banner-light.svg / banner-dark.svg      顶部头图（名字 + 方向 + 雷达纹）
    terminal-light.svg / terminal-dark.svg  终端面板（放项目概览，带光标闪烁动画）
    status-<名称>-light.svg / -dark.svg     状态徽标（在做 / 已完成 / 在学）

约定：SVG 里只写系统字体族（monospace / sans-serif），且不引用外部资源，
所以在 GitHub 的 <img> 里也能正常显示；CSS 动画在 <img> 中同样会跑。
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"

# ---------- 配色（亮暗两套，取 GitHub 自己的配色习惯） ----------
THEMES = {
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "grid": "#0969da",
        "title": "#0b1220",
        "sub": "#57606a",
        "accent": "#0e7490",
        "accent2": "#b45309",
        "chip_bg": "#f6f8fa",
        "chip_border": "#d0d7de",
        "term_bg": "#f6f8fa",
        "term_head": "#eaeef2",
        "term_dot": ("#ff5f57", "#febc2e", "#28c840"),
        "ok": "#1a7f37",
        "warn": "#9a6700",
        "dim": "#8c959f",
    },
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "grid": "#58a6ff",
        "title": "#e6edf3",
        "sub": "#8b949e",
        "accent": "#22d3ee",
        "accent2": "#f59e0b",
        "chip_bg": "#161b22",
        "chip_border": "#30363d",
        "term_bg": "#0b0f14",
        "term_head": "#161b22",
        "term_dot": ("#ff5f57", "#febc2e", "#28c840"),
        "ok": "#3fb950",
        "warn": "#d29922",
        "dim": "#6e7681",
    },
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Courier New', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def banner(theme: str, name: str, tagline: str, chips: list[str], radar_label: str) -> str:
    """头图：左侧名字 + 标语，右侧雷达扫描纹（安全/侦察意象），底部四个方向小 chip。"""
    c = THEMES[theme]
    w, h = 1200, 264
    chip_svg = []
    x = 56
    for text in chips:
        cw = 20 + len(text) * 8.6
        chip_svg.append(
            f'<rect x="{x:.0f}" y="196" width="{cw:.0f}" height="30" rx="15" '
            f'fill="{c["chip_bg"]}" stroke="{c["chip_border"]}" />'
            f'<text x="{x + cw / 2:.0f}" y="216" text-anchor="middle" font-size="14" '
            f'font-family="{MONO}" fill="{c["sub"]}">{esc(text)}</text>'
        )
        x += cw + 12
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(name)}">
  <defs>
    <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M26 0H0V26" fill="none" stroke="{c["grid"]}" stroke-opacity="0.07" stroke-width="1" />
    </pattern>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{c["accent"]}" />
      <stop offset="100%" stop-color="{c["accent2"]}" />
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{c["accent"]}" stop-opacity="0.42" />
      <stop offset="100%" stop-color="{c["accent"]}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}" />
  <rect width="{w}" height="{h}" rx="18" fill="url(#grid)" />
  <rect x="0" y="34" width="6" height="{h - 68}" rx="3" fill="url(#bar)" />

  <text x="56" y="112" font-size="50" font-weight="700" letter-spacing="1.5"
        font-family="{MONO}" fill="{c["title"]}">{esc(name)}</text>
  <text x="58" y="152" font-size="19" letter-spacing="2.4"
        font-family="{MONO}" fill="{c["accent"]}">{esc(tagline)}</text>
  {"".join(chip_svg)}

  <!-- 右侧雷达：同心弧 + 旋转扫描扇面 -->
  <g transform="translate(1012,132)">
    <circle r="86" fill="none" stroke="{c["grid"]}" stroke-opacity="0.18" />
    <circle r="60" fill="none" stroke="{c["grid"]}" stroke-opacity="0.14" />
    <circle r="34" fill="none" stroke="{c["grid"]}" stroke-opacity="0.10" />
    <circle r="3" fill="{c["accent2"]}" />
    <g>
      <path d="M0 0 L44 -38 A58 58 0 0 0 0 -58 Z" fill="url(#sweep)" />
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite" />
    </g>
    <circle cx="34" cy="-16" r="3.2" fill="{c["ok"]}" />
    <circle cx="-42" cy="26" r="2.6" fill="{c["accent"]}" />
    <circle cx="16" cy="46" r="2.2" fill="{c["warn"]}" />
    <text x="0" y="112" text-anchor="middle" font-size="13" letter-spacing="2"
          font-family="{MONO}" fill="{c["dim"]}">{esc(radar_label)}</text>
  </g>
</svg>
'''


def terminal(theme: str, title: str, lines: list[tuple[str, str]]) -> str:
    """终端面板：窗口栏 + 等宽正文；最后一行的光标会闪。"""
    c = THEMES[theme]
    w = 620
    line_h = 26
    top = 74
    h = top + line_h * len(lines) + 26
    dots = "".join(
        f'<circle cx="{24 + i * 20}" cy="26" r="6" fill="{col}" />'
        for i, col in enumerate(c["term_dot"])
    )
    body = []
    for i, (kind, text) in enumerate(lines):
        y = top + i * line_h
        if kind == "cmd":
            body.append(
                f'<text x="24" y="{y}" font-size="15" font-family="{MONO}" fill="{c["title"]}">'
                f'<tspan fill="{c["ok"]}">$ </tspan>{esc(text)}</text>'
            )
        elif kind == "out":
            body.append(
                f'<text x="40" y="{y}" font-size="15" font-family="{MONO}" '
                f'fill="{c["sub"]}">{esc(text)}</text>'
            )
        elif kind == "hl":
            body.append(
                f'<text x="40" y="{y}" font-size="15" font-family="{MONO}" '
                f'fill="{c["accent"]}">{esc(text)}</text>'
            )
        else:  # comment
            body.append(
                f'<text x="24" y="{y}" font-size="15" font-family="{MONO}" '
                f'fill="{c["dim"]}">{esc(text)}</text>'
            )
    cursor_y = top + len(lines) * line_h
    body.append(
        f'<rect x="24" y="{cursor_y - 14}" width="9" height="17" fill="{c["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.5;0.5;0.99;1" '
        f'dur="1.4s" repeatCount="indefinite" /></rect>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <rect width="{w}" height="{h}" rx="12" fill="{c["term_bg"]}" stroke="{c["border"]}" />
  <path d="M0 12a12 12 0 0 1 12-12h{w - 24}a12 12 0 0 1 12 12v40H0z" fill="{c["term_head"]}" />
  <line x1="0" y1="52" x2="{w}" y2="52" stroke="{c["border"]}" />
  {dots}
  <text x="{w / 2:.0f}" y="31" text-anchor="middle" font-size="14" font-family="{MONO}"
        fill="{c["sub"]}">{esc(title)}</text>
  {"".join(body)}
</svg>
'''


def status_badge(theme: str, label: str, color_key: str) -> str:
    """状态徽标：左侧圆点 + 文字，窄条药丸形。"""
    c = THEMES[theme]
    color = c[color_key]
    w = 22 + len(label) * 13.5
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="32" viewBox="0 0 {w:.0f} 32" role="img" aria-label="{esc(label)}">
  <rect width="{w:.0f}" height="32" rx="16" fill="{c["chip_bg"]}" stroke="{c["chip_border"]}" />
  <circle cx="16" cy="16" r="4.5" fill="{color}" />
  <text x="28" y="21" font-size="14" font-family="{SANS}" fill="{c["sub"]}">{esc(label)}</text>
</svg>
'''


def fetch_languages(user: str) -> tuple[dict[str, int], str]:
    """按公开仓库的语言字节数汇总（默认跳过 fork），返回 ({语言: 字节}, 数据日期)。

    联网拉 GitHub 公开接口（不需要令牌，6 个仓库 6 次请求，够用）；
    拉不到就退回下面这份离线快照，保证脚本永远能跑。
    """
    import json
    import urllib.request
    from datetime import date

    try:
        api = f"https://api.github.com/users/{user}/repos?per_page=100"
        req = urllib.request.Request(api, headers={"User-Agent": "profile-assets"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            repos = json.load(resp)
        names = [r["name"] for r in repos if not r.get("fork")]
        totals: dict[str, int] = {}
        for name in names:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{user}/{name}/languages",
                headers={"User-Agent": "profile-assets"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                for lang, size in json.load(resp).items():
                    totals[lang] = totals.get(lang, 0) + size
        if totals:
            return totals, date.today().isoformat()
    except Exception as exc:  # 离线/限流都没关系，用快照
        print(f"  [提示] 语言数据拉取失败（{type(exc).__name__}），改用离线快照")
    return FALLBACK_LANGS, FALLBACK_LANG_DATE


def langcard(theme: str, totals: dict[str, int], as_of: str, top: int = 6) -> str:
    """语言构成卡：一条堆叠比例条 + 图例，数据来自公开仓库语言字节统计。"""
    c = THEMES[theme]
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    head, rest = ranked[:top], ranked[top:]
    if rest:
        head = head + [("其他 · Others", sum(v for _, v in rest))]
    total = sum(v for _, v in head) or 1

    w, h = 1200, 232
    bar_x, bar_y, bar_w, bar_h = 56, 116, w - 112, 26
    segs = []
    legend = []
    x = bar_x
    for i, (lang, size) in enumerate(head):
        frac = size / total
        seg_w = bar_w * frac
        color = LANG_COLORS.get(lang.split(" · ")[0], c["dim"])
        segs.append(
            f'<rect x="{x:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" '
            f'fill="{color}" rx="{3 if i in (0, len(head) - 1) else 0}" />'
        )
        if frac >= 0.055:  # 太窄的段不写字，避免糊成一团
            segs.append(
                f'<text x="{x + seg_w / 2:.1f}" y="{bar_y + 18}" text-anchor="middle" '
                f'font-size="12.5" font-family="{MONO}" fill="#ffffff" '
                f'fill-opacity="0.92">{frac * 100:.1f}%</text>'
            )
        legend.append((lang, color, frac))
        x += seg_w

    legend_svg = []
    lx = 56
    for lang, color, frac in legend:
        text = f"{lang} {frac * 100:.1f}%"
        cw = 26 + len(text) * 8.4
        legend_svg.append(
            f'<rect x="{lx:.0f}" y="164" width="{cw:.0f}" height="28" rx="14" '
            f'fill="{c["chip_bg"]}" stroke="{c["chip_border"]}" />'
            f'<circle cx="{lx + 15:.0f}" cy="178" r="4.5" fill="{color}" />'
            f'<text x="{lx + 26:.0f}" y="183" font-size="13" font-family="{MONO}" '
            f'fill="{c["sub"]}">{esc(text)}</text>'
        )
        lx += cw + 10

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="语言构成">
  <rect width="{w}" height="{h}" rx="14" fill="{c["bg"]}" stroke="{c["border"]}" />
  <text x="56" y="62" font-size="22" font-weight="600" font-family="{MONO}" fill="{c["title"]}">Language Mix</text>
  <text x="56" y="90" font-size="13.5" font-family="{MONO}" fill="{c["dim"]}">公开仓库语言字节占比（不含 fork）· 数据日期 {esc(as_of)}</text>
  {"".join(segs)}
  {"".join(legend_svg)}
</svg>
'''


FALLBACK_LANG_DATE = "2026-09-22"
FALLBACK_LANGS = {
    "Python": 2418736, "Vue": 101841, "C++": 61928, "JavaScript": 20292,
    "Batchfile": 21069, "CSS": 18385, "Shell": 18702, "PowerShell": 6791,
    "HTML": 1254, "Java": 1655, "Hack": 767, "PHP": 374, "Dockerfile": 314,
}
LANG_COLORS = {
    "Python": "#3776AB", "Vue": "#41B883", "C++": "#00599C", "JavaScript": "#E8B100",
    "Batchfile": "#C1F12E", "CSS": "#663399", "Shell": "#89E051", "TypeScript": "#3178C6",
    "Go": "#00ADD8", "PowerShell": "#5391FE", "HTML": "#E34F26", "Java": "#B07219",
    "其他 · Others": "#8B949E", "Others": "#8B949E",
}


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    written = []

    langs, lang_date = fetch_languages("junfennie162-sketch")
    print(f"  语言数据：{len(langs)} 种，日期 {lang_date}")

    for theme in ("light", "dark"):
        written.append(("langcard-%s.svg" % theme, langcard(theme, langs, lang_date)))
        written.append(("banner-%s.svg" % theme, banner(
            theme,
            name="junfennie162-sketch",
            tagline="RAG  ·  LLM AGENT  ·  SECURITY TOOLING",
            chips=["Python", "FastAPI", "Vue 3", "PyTorch / SUPA", "Docker"],
            radar_label="RECON",
        )))
        written.append(("terminal-%s.svg" % theme, terminal(
            theme,
            title="junfennie162-sketch — zsh",
            lines=[
                ("cmd", "whoami"),
                ("out", "中北大学 · 翻斗花园 · LLM 应用 & 安全工具"),
                ("cmd", "ls ~/projects --sort=size"),
                ("hl", "textbook-exercise-rag/   教材习题解析生成器（RAG）"),
                ("hl", "birensupa-spectralconv/  壁仞 SUPA 算子 + FNO-NS"),
                ("hl", "corehacker/             AI 渗透测试框架"),
                ("cmd", "python -m pytest -q"),
                ("out", "158 passed"),
            ],
        )))
        for key, label, color_key in (
            ("building", "在做 · Building", "accent"),
            ("shipped", "已完成 · Shipped", "ok"),
            ("learning", "在学 · Learning", "warn"),
        ):
            written.append(("status-%s-%s.svg" % (key, theme), status_badge(theme, label, color_key)))

    for name, content in written:
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"  写出 assets/{name}  ({len(content.encode('utf-8'))} B)")
    print(f"\n共 {len(written)} 个素材，目录：{ASSETS}")


if __name__ == "__main__":
    main()
