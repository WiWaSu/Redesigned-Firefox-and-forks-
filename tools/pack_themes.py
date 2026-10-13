#!/usr/bin/env python3
"""Redesigned Fox — упаковка тем для переключения прямо в браузере.

Берёт «сырые» темы из src/themes/<id>-{chrome,content,pdf}.css (их пишут
gen_themes.py и gen_ios.py) и кладёт в files/pdf-tweaks/themes/:

  <id>-chrome.css / -content.css / -pdf.css
      то, что установщик вписывает в userChrome.css / userContent.css.
      Каждое правило получает «замок» :root:not([fm-theme]:not([fm-theme="<id>"])):
      пока скрипт не сказал, какая тема выбрана (атрибута нет) — тема работает,
      как только в браузере выбрали другую (fm-theme="другая") — она отключается
      без перезапуска. Части обрамлены метками FM-THEME BEGIN / END, чтобы
      браузер мог сам заменить тему в файлах.

  <id>-live.css
      те же три части для подключения «на лету» (через nsIStyleSheetService):
      замок строгий — :root[fm-theme="<id>"], стили окна ограничены chrome://.

  themes.json — список тем с цветами для плиток выбора.

Запуск: python3 tools/pack_themes.py
"""

import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "themes"
OUT = ROOT / "files" / "pdf-tweaks" / "themes"

# порядок = порядок плиток в установщике и в браузере
# id, название, [фон окна, панель, акцент, текст] (тёмный вариант — для плитки)
THEMES = [
    ("oneui", "One UI", ["#0f1012", "#1c1d21", "#3e91ff", "#f2f3f5"]),
    ("ios", "iOS Liquid Glass", ["#05060b", "#1c1c1e", "#0a84ff", "#ffffff"]),
    ("material", "Material You", ["#131418", "#1d2027", "#a8c7fa", "#e4e2e6"]),
    ("fluent", "Windows 11", ["#202020", "#2b2b2b", "#4cc2ff", "#ffffff"]),
    ("macos", "macOS", ["#1e1e1e", "#2c2c2e", "#0a84ff", "#f5f5f7"]),
    ("nothing", "Nothing", ["#000000", "#111111", "#d71921", "#ffffff"]),
    ("nightdrive", "Night Drive", ["#07080d", "#151822", "#ffb25b", "#eef0f6"]),
    ("aero", "Aero", ["#163a6b", "#1d4a85", "#5ab0ff", "#ffffff"]),
    ("retro", "Retro 98", ["#008080", "#c0c0c0", "#000080", "#000000"]),
    ("terminal", "Terminal", ["#030803", "#081108", "#33ff66", "#b7ffc4"]),
    ("paper", "Paper", ["#f3eee3", "#fbf8f1", "#b4532a", "#2b2620"]),
    ("cyber", "Cyberpunk", ["#0a0612", "#15111f", "#ff00aa", "#f3f0ff"]),
]
PARTS = ("chrome", "content", "pdf")


# ------------------------------------------------------------------ мини-разбор CSS
def split_top(text):
    """Делит CSS на узлы верхнего уровня: ("comment", txt), ("at-block", prelude, body),
    ("at-stmt", txt), ("rule", prelude, body), ("ws", txt)."""
    nodes, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            nodes.append(("ws", text[i:j]))
            i = j
            continue
        if text.startswith("/*", i):
            j = text.index("*/", i) + 2
            nodes.append(("comment", text[i:j]))
            i = j
            continue
        # прелюдия до { или ;
        j, depth, quote = i, 0, None
        while j < n:
            ch = text[j]
            if quote:
                if ch == "\\":
                    j += 2
                    continue
                if ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
            elif text.startswith("/*", j):
                j = text.index("*/", j) + 2
                continue
            elif ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            elif depth == 0 and ch in "{;":
                break
            j += 1
        prelude = text[i:j]
        if j >= n or text[j] == ";":
            nodes.append(("at-stmt", text[i:j + 1]))
            i = j + 1
            continue
        # тело до парной }
        k, depth, quote = j + 1, 1, None
        while k < n and depth:
            ch = text[k]
            if quote:
                if ch == "\\":
                    k += 2
                    continue
                if ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
            elif text.startswith("/*", k):
                k = text.index("*/", k) + 2
                continue
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            k += 1
        body = text[j + 1:k - 1]
        kind = "at-block" if prelude.lstrip().startswith("@") else "rule"
        nodes.append((kind, prelude, body))
        i = k
    return nodes


def split_selectors(prelude):
    out, depth, cur = [], 0, ""
    for ch in prelude:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def guard_selector(sel, lock):
    s = sel.strip()
    if not s:
        return sel
    if s.startswith(":root"):
        return ":root" + lock + s[5:]
    if re.match(r"html(?![\w-])", s):
        return "html" + lock + s[4:]
    return ":root" + lock + " " + s


def guard(text, lock):
    res = []
    for node in split_top(text):
        kind = node[0]
        if kind in ("ws", "comment", "at-stmt"):
            res.append(node[1])
        elif kind == "at-block":
            prelude, body = node[1], node[2]
            name = prelude.strip().split()[0].lower()
            if name in ("@-moz-document", "@media", "@supports", "@layer"):
                res.append(prelude + "{" + guard(body, lock) + "}")
            else:  # @keyframes, @font-face — без изменений
                res.append(prelude + "{" + body + "}")
        else:
            prelude, body = node[1], node[2]
            lead = prelude[: len(prelude) - len(prelude.lstrip())]
            sels = ", ".join(guard_selector(s, lock) for s in split_selectors(prelude.strip()))
            res.append(lead + sels + " {" + body + "}")
    return "".join(res)


def only_chrome(text):
    """Для подключения на лету: правила вне @-moz-document — только для chrome://."""
    loose, docs = [], []
    for node in split_top(text):
        if node[0] == "at-block" and node[1].strip().lower().startswith("@-moz-document"):
            docs.append(node[1] + "{" + node[2] + "}")
        elif node[0] in ("rule", "at-block"):
            loose.append(node[1] + "{" + node[2] + "}")
        elif node[0] == "at-stmt":
            loose.append(node[1])
    out = ""
    if loose:
        out += '@-moz-document url-prefix("chrome://") {\n' + "\n".join(loose) + "\n}\n"
    return out + "\n".join(docs)


def baked_lock(tid):
    return f':not([fm-theme]:not([fm-theme="{tid}"]))'


def live_lock(tid):
    return f'[fm-theme="{tid}"][fm-theme]'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.css"):
        old.unlink()
    listing = []
    for tid, name, sw in THEMES:
        live = [f"/* Redesigned Fox — тема «{name}», подключается на лету */"]
        for part in PARTS:
            src = SRC / f"{tid}-{part}.css"
            raw = src.read_text(encoding="utf-8") if src.exists() else ""
            if tid != "oneui" and not raw:
                sys.exit(f"нет {src}")
            body = guard(raw, baked_lock(tid)).strip("\n") if raw else ""
            text = f"/* FM-THEME BEGIN {tid} {part} */\n{body}\n/* FM-THEME END {part} */\n"
            assert text.count("{") == text.count("}"), (tid, part)
            (OUT / f"{tid}-{part}.css").write_text(text, encoding="utf-8")
            if raw:
                g = guard(raw, live_lock(tid))
                live.append(only_chrome(g) if part == "chrome" else g)
        lt = "\n".join(live) + "\n"
        assert lt.count("{") == lt.count("}"), tid
        (OUT / f"{tid}-live.css").write_text(lt, encoding="utf-8")
        listing.append({"id": tid, "name": name, "swatch": sw})
    # CSS «Без скруглений» — в модуль Studio (тот же текст, что читает установщик)
    pt = ROOT / "files" / "pdf-tweaks"
    studio = pt / "FloorpModernStudio.sys.mjs"
    js = studio.read_text(encoding="utf-8")
    block = "// SQUARE-CSS BEGIN\n"
    for name, var in (("square-chrome.css", "SQUARE_CHROME"), ("square-content.css", "SQUARE_CONTENT")):
        css = (pt / name).read_text(encoding="utf-8")
        block += f"const {var} = {json.dumps(css, ensure_ascii=False)};\n"
    block += "// SQUARE-CSS END"
    js = re.sub(r"// SQUARE-CSS BEGIN[\s\S]*?// SQUARE-CSS END", lambda m: block, js)
    studio.write_text(js, encoding="utf-8")
    (OUT / "themes.json").write_text(json.dumps(listing, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok:", ", ".join(t[0] for t in THEMES))


if __name__ == "__main__":
    main()
