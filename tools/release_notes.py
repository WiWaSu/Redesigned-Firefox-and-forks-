#!/usr/bin/env python3
"""Описание релиза для GitHub: changes/v<версия>.md.

Берёт раздел версии из CHANGELOG.md и оборачивает его в «витрину»: название,
что изменилось, картинки, как установить. {{REPO}} и {{TAG}} подставляет
GitHub Actions при публикации релиза (.github/workflows/release.yml).

    python3 tools/release_notes.py 1.14.0
"""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
ver = sys.argv[1]
log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
m = re.search(r"(?ms)^## " + re.escape(ver) + r"(?: — (\S+))?\n(.*?)(?=^## |\Z)", log)
if not m:
    sys.exit(f"нет раздела {ver} в CHANGELOG.md")
date, body = m.group(1) or "", m.group(2).strip()
IMG = "https://raw.githubusercontent.com/{{REPO}}/{{TAG}}/docs/"
# картинки из CHANGELOG (docs/...) — полными ссылками, чтобы работали в релизе
body = body.replace("](docs/", "](" + IMG)
text = f"""<div align="center">

# Redesigned Fox {ver}

**A redesign for Floorp, Firefox and Firefox forks** · {date}

![Redesigned Fox]({IMG}hero.jpg)

</div>

## Что нового / What's new

{body}

## Скриншоты / Screenshots

| | |
|---|---|
| ![One UI]({IMG}theme-oneui.jpg) | ![iOS]({IMG}theme-ios.jpg) |
| ![Night Drive]({IMG}theme-nightdrive.jpg) | ![Cyberpunk]({IMG}theme-cyber.jpg) |
| ![Wallpapers]({IMG}wallpaper-picker.jpg) | ![Studio]({IMG}studio-menus.jpg) |

## Установка / Install

1. Скачайте **RedesignedFox-v{ver}.zip** ниже и распакуйте. / Download **RedesignedFox-v{ver}.zip** below and unzip.
2. Запустите **Setup.cmd**, выберите тему и браузеры, нажмите «Установить». / Run **Setup.cmd**, pick a theme and browsers, press Install.
3. Перезапустите браузер. / Restart the browser.

Уже стоит более старая версия — просто установите поверх, настройки сохранятся. / Already installed — just install over it, your settings are kept.

[Все изменения / Full changelog](https://github.com/{{{{REPO}}}}/blob/main/CHANGELOG.md)
"""
(root / "changes" / f"v{ver}.md").write_text(text, encoding="utf-8")
print(f"changes/v{ver}.md")
