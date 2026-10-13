<div align="center">

# Redesigned Fox

<sub>formerly Floorp Modern</sub>

**A complete redesign for Floorp, Firefox and Firefox forks on Windows.**
12 themes · live design studio · new-tab wallpapers · iOS-style animations · reworked PDF viewer

![Version](https://img.shields.io/badge/version-1.19.0-8e6bff)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078d4)
![Floorp](https://img.shields.io/badge/Floorp-12-6b4dff)
![Firefox](https://img.shields.io/badge/Firefox-156%2B-ff7139)
![License](https://img.shields.io/badge/license-MIT-2ea44f)

[Русская версия ниже](#русский) · [Changelog](CHANGELOG.md) · [Release notes by version](changes/)

![12 themes](docs/hero.jpg)

</div>

## Supported browsers

Floorp · Firefox · Firefox Developer Edition · Firefox Nightly · LibreWolf · Waterfox · Zen Browser · Mercury

## Features

### 🎨 12 themes
| Theme | Look |
|---|---|
| **One UI** | Samsung Galaxy: pure black, pill-shaped tabs and buttons, thin lock-screen clock |
| **iOS · Liquid Glass** | iOS 26: wallpaper behind the window, floating glass toolbar, glass tabs, menus and clock |
| **Material You** | Android / Pixel: tonal colors from your accent, stacked clock |
| **Windows 11** | Fluent: crisp corners, accent underline, Bloom wallpaper |
| **macOS** | Traffic-light window buttons, blue menus, wave wallpaper |
| **Nothing** | Monochrome, red dot, dot-matrix clock |
| **Night Drive** | Night road behind a fogged car window: blurred lights at the edges, thin glowing clock |
| **Aero** | Windows 7: glossy blue glass, shiny buttons |
| **Retro 98** | Windows 98: grey bevelled buttons, navy title bars, teal desktop, zero rounding |
| **Terminal** | Green phosphor, monospace everything, scanlines, blinking cursor |
| **Paper** | Warm paper, serif font, flat and calm |
| **Cyberpunk** | Cut corners, yellow neon, pink and cyan city grid |

### 🎛 Quick panel — switch themes right in the browser
Click the **palette button** on the toolbar: pick any of the 12 themes, turn **all rounded corners off**, switch light / dark and the accent color. Everything applies instantly in every window, the new tab, settings pages and PDFs — no installer, no restart. The choice is also written to `userChrome.css` / `userContent.css`, so it stays after a restart.

![Quick panel](docs/quick-panel.jpg)

### 🛠 Redesigned Fox Studio — tweak everything, live
Open with **All design settings…** in the quick panel, **☰ → Design**, or `Alt+Shift+S`. Every change applies instantly, on top of any theme:

- **Theme** — the same 12 themes, switched live

- **Colors** — accent, window background, fields, menus, text; menu transparency and blur
- **Shape** — **no rounded corners at all** (one switch), page corner radius, gap and shadow, menu radius, button shape, density
- **Hide tabs completely** — not the compact strip: tabs slide out from the window edge on hover, or stay fully hidden (`Alt+Shift+T` toggles)
- **Tabs** — 6 shapes (pill, rounded, square, underline, card, Chrome-like), 6 selected-tab styles (incl. none), height, width, close button, font weight
- **Address bar** — height, radius, alignment, border style
- **Right-click menus** — 7 styles: One UI, iOS glass, Windows 11, macOS, Touch, Nothing, Neon
- **Ctrl+Tab switcher** — preview window with 4 styles: iOS, Windows 11, list, neon
- **Font** — any installed font, UI text size
- **Animations** — speed and springiness
- **New tab** — clock size, weight, font and position, date, search width, shortcuts, wallpaper blur
- **Show / hide** — bookmarks bar, toolbar buttons, Now Bar, call bar, loading line
- 6 ready-made presets, export / import settings as a file, one-click reset

![Studio](docs/studio.jpg)

### 📞 Call bar
A call in another tab (Telegram, Discord, WhatsApp, Meet…) shows a small island at the top: site, call timer, mute mic, turn camera off, jump to the call. It shrinks to a timer pill after a few seconds. `Alt+Shift+M` mutes the mic from any tab.

![Call bar](docs/call-bar.jpg)

### 🔔 Update check
Once a day the browser checks the [releases repo](https://github.com/WiWaSu/Redesigned-Firefox-and-forks-). A new version shows a notification and a red dot on the Design button; the quick panel has **Download**, **What's new** and **Later**. Nothing is downloaded automatically. Turn it off in Studio → Updates.

### 🖼 New-tab wallpapers
Button at the bottom left of the new tab: 10 built-in wallpapers, **your own picture**, dimming slider. Applies to every open new tab at once. Can also be chosen in the installer.

![Wallpapers](docs/wallpapers.jpg)

### ✨ Animations
Real spring physics like on iPhone: tabs pop in, menus and panels unfold from where you clicked, buttons respond to presses, the new tab's clock fades in from blur, shortcuts bounce in one by one. Four modes in the installer: **iOS springs**, **Smooth**, **System** (follows Windows), **Off**. Works even when Windows animation effects are disabled.

### 🧩 Extras
- **Now Bar** — music playing in another tab shows a draggable bar with artwork, progress, previous / next, pause and mute (YouTube, Telegram and more)
- Page-loading line under the toolbar
- Theme button: Auto / Light / Dark in one click
- Toasts: downloads finished, page zoom, tab muted
- `Alt+Shift+C` copy page address · `Alt+Shift+D` close duplicate tabs · `Alt+Shift+Z` focus mode
- Lock-screen clock on the Firefox / LibreWolf / Waterfox new tab too
- Restyled screenshot tool and screen-sharing indicator

### 📄 PDF viewer
- New toolbar and icons; floats over the pages in the iOS theme
- Interface theme (auto / light / dark) and page tone (paper / sepia / night)
- **Edge-style ink** — drawings have no selection frame, grab them only by the strokes, keep drawing right next to them
- Reopens every PDF on the page where you stopped
- **Page bookmarks** with notes — ribbon button, `Ctrl+B` for the current page
- Quick text — click a "……" gap or double-click empty space and type
- Own color picker instead of the Windows color dialog
- Auto-redraws pages after a GPU switch (integrated ↔ discrete)

## Screenshots

<table>
<tr><td><img src="docs/theme-oneui.jpg" alt="One UI"><br><b>One UI</b></td><td><img src="docs/theme-ios.jpg" alt="iOS · Liquid Glass"><br><b>iOS · Liquid Glass</b></td></tr>
<tr><td><img src="docs/theme-material.jpg" alt="Material You"><br><b>Material You</b></td><td><img src="docs/theme-fluent.jpg" alt="Windows 11"><br><b>Windows 11</b></td></tr>
<tr><td><img src="docs/theme-macos.jpg" alt="macOS"><br><b>macOS</b></td><td><img src="docs/theme-nothing.jpg" alt="Nothing"><br><b>Nothing</b></td></tr>
<tr><td><img src="docs/theme-nightdrive.jpg" alt="Night Drive"><br><b>Night Drive</b></td><td><img src="docs/theme-aero.jpg" alt="Aero"><br><b>Aero</b></td></tr>
<tr><td><img src="docs/theme-retro.jpg" alt="Retro 98"><br><b>Retro 98</b></td><td><img src="docs/theme-terminal.jpg" alt="Terminal"><br><b>Terminal</b></td></tr>
<tr><td><img src="docs/theme-paper.jpg" alt="Paper"><br><b>Paper</b></td><td><img src="docs/theme-cyber.jpg" alt="Cyberpunk"><br><b>Cyberpunk</b></td></tr>
<tr><td><img src="docs/wallpaper-picker.jpg" alt="Wallpapers"><br><b>Wallpaper picker</b></td><td><img src="docs/studio-menus.jpg" alt="Studio"><br><b>Studio: right-click menu styles</b></td></tr>
</table>

## Install

1. Download the latest release (or `Code → Download ZIP`) and unzip it.
2. Run **`Setup.cmd`** and allow administrator rights (needed once to put a tiny script loader into the browser folder).
3. Pick a theme, wallpaper, accent color, light/dark mode, corners, animations and features, then choose the browsers.
4. Press **Install** and restart the browser.

Prefer the console? `install.cmd` does the same with text prompts. If SmartScreen appears: *More info → Run anyway*.

Use the built-in browser theme **"System theme — auto"** — third-party themes repaint the window frame.

## Uninstall

`Setup.cmd` → **Remove theme** (or `uninstall.cmd`). The previous look, the stock PDF viewer and default settings come back after a restart. Your own `userChrome.css` / `userContent.css` rules are kept; backups are saved as `*.bak-floorp-modern`.

## After a browser update

A major update may remove the loader from the program folder. If the toolbar buttons or PDF features disappear, run `Setup.cmd` again.

## How it works

| Where | What |
|---|---|
| Browser folder (`C:\Program Files\…`) | `config.js` + `defaults\pref\config-prefs.js` — AutoConfig loader |
| Profile `chrome\userChrome.css` | Browser interface (block `FLOORP-MODERN`) |
| Profile `chrome\userContent.css` | New tab, settings pages, PDF viewer (blocks `FLOORP-MODERN`, `PDF-TWEAKS`) |
| Profile `chrome\pdf-tweaks\` | Window features, PDF actor, Studio, wallpapers, themes for live switching (`themes\`) |
| Profile `user.js` | A few prefs (stylesheets, Nova, animations) |

The theme is stored in the `floorp.modern.theme` pref; the theme block inside the CSS files sits between `FM-THEME BEGIN/END` markers, so the browser can swap it itself. Studio settings are stored in the `floorp.modern.studio` pref and applied as a live stylesheet — no restart needed. Logs for troubleshooting: `chrome\pdf-tweaks\fm-log.json` and `fm-boot.json`.

## Development

CSS is generated by the scripts in `tools/`:

```sh
python3 tools/gen_chrome.py files                 # base chrome + content CSS
python3 tools/gen_css.py > files/pdf-viewer-theme.css
python3 tools/gen_ios.py src/themes               # iOS overlay (source)
python3 tools/gen_themes.py src/themes            # other theme overlays (source)
python3 tools/pack_themes.py                      # themes for installer + live switching
sh tools/build.sh                                 # release zip
```

## Disclaimer

Unofficial community mod, not affiliated with or endorsed by Mozilla or Ablaze (Floorp). It uses the browsers' documented customization mechanisms (`userChrome.css`, `userContent.css`, AutoConfig). Use at your own risk.

## License

[MIT](LICENSE)

---

<a id="русский"></a>

## Русский

**Полный редизайн Floorp, Firefox и форков Firefox для Windows.** (раньше назывался Floorp Modern)
12 тем · живая настройка дизайна · обои новой вкладки · анимации как в iOS · новый просмотрщик PDF

**Поддерживаются:** Floorp, Firefox, Firefox Developer Edition, Firefox Nightly, LibreWolf, Waterfox, Zen Browser, Mercury.

### 🎨 12 тем
- **One UI** — как Samsung Galaxy: чёрный фон, вкладки и кнопки-«таблетки», тонкие часы.
- **iOS · Liquid Glass** — как iOS 26: обои под окном, парящая стеклянная панель, стеклянные вкладки, меню и часы.
- **Material You** — как Android / Pixel: тональные цвета из акцента, часы столбиком.
- **Windows 11** — Fluent: строгие углы, акцентная полоска, обои Bloom.
- **macOS** — «светофор» вместо кнопок окна, синие меню, обои-волны.
- **Nothing** — монохром, красная точка, часы из точек.
- **Night Drive** — ночная дорога за запотевшим стеклом машины: размытые огни по краям, тонкие светящиеся часы.
- **Aero** — Windows 7: голубое стекло с бликом, глянцевые кнопки.
- **Retro 98** — Windows 98: серые выпуклые кнопки, синие заголовки, бирюзовый рабочий стол, никаких скруглений.
- **Terminal** — зелёный фосфор, всё моноширинное, строки развёртки, мигающий курсор.
- **Paper** — тёплая бумага, шрифт с засечками, плоско и спокойно.
- **Cyberpunk** — срезанные углы, жёлтый неон, розово-голубой город.

### 🎛 Быстрая панель — темы прямо в браузере
Кнопка **с палитрой** на панели: любая из 12 тем, **«Без скруглений»**, светлое / тёмное оформление, цвет акцента. Всё меняется сразу во всех окнах, на новой вкладке, в настройках и в PDF — без установщика и без перезапуска. Выбор записывается и в `userChrome.css` / `userContent.css`, так что после перезапуска всё остаётся.

### 🛠 Redesigned Fox Studio — настройка всего, сразу
**«Все настройки дизайна…»** в быстрой панели, **☰ → Дизайн** или `Alt+Shift+S`. Всё меняется мгновенно, поверх любой темы:

- **Тема** — те же 12 тем, меняются сразу

- **Цвета** — акцент, фон окна, поля, меню, текст; прозрачность и размытие меню
- **Форма** — **без скруглений вообще** (один переключатель), скругление, отступ и тень страницы, скругление меню, форма кнопок, плотность
- **Скрыть вкладки целиком** — не компактный вид: выезжают от края окна при наведении или не видны совсем (`Alt+Shift+T`)
- **Вкладки** — 6 форм (таблетки, скруглённые, прямые, подчёркивание, карточки, как в Chrome), 6 стилей выбранной вкладки (в том числе без подсветки), высота, ширина, крестик, жирность
- **Адресная строка** — высота, скругление, выравнивание, рамка
- **Меню правой кнопки** — 7 стилей: One UI, стекло iOS, Windows 11, macOS, сенсорное, Nothing, неон
- **Ctrl+Tab** — окно с превью вкладок, 4 стиля: iOS, Windows 11, список, неон
- **Шрифт** — любой установленный, размер текста
- **Анимации** — скорость и пружинистость
- **Новая вкладка** — размер, толщина, шрифт и место часов, дата, ширина поиска, ярлыки, размытие обоев
- **Показать / скрыть** — панель закладок, кнопки, Now Bar, плашку звонка, полоску загрузки
- 6 готовых наборов, сохранение и загрузка настроек файлом, сброс

### 📞 Плашка звонка
Звонок в другой вкладке (Telegram, Discord, WhatsApp, Meet…) — сверху появляется «островок»: сайт, время звонка, выключить микрофон или камеру, перейти к звонку. Через пару секунд сворачивается в таблетку с таймером. `Alt+Shift+M` — микрофон из любой вкладки.

### 🔔 Проверка обновлений
Раз в сутки браузер смотрит в [репозиторий релизов](https://github.com/WiWaSu/Redesigned-Firefox-and-forks-). Есть новая версия — уведомление и красная точка на кнопке «Дизайн», в быстрой панели «Скачать», «Что нового», «Позже». Сам ничего не скачивает. Выключить — Studio → «Обновления».

### 🖼 Обои новой вкладки
Кнопка слева внизу: 10 готовых обоев, **своя картинка**, затемнение. Меняются сразу во всех вкладках. Можно выбрать и в установщике.

### ✨ Анимации
Настоящие «пружины», как на iPhone: вкладки выныривают, меню раскрываются из точки нажатия, кнопки пружинят, часы проявляются из размытия, ярлыки выпрыгивают по очереди. В установщике 4 режима: **Как в iOS**, **Плавные**, **Как в Windows**, **Выкл**. Работают, даже если в Windows анимации выключены.

### 🧩 Дополнительно
- **Now Bar** — музыка в другой вкладке: плашка с обложкой, прогрессом, назад/вперёд, паузой и звуком (YouTube, Telegram и др.), её можно перетаскивать
- Полоска загрузки страницы
- Кнопка темы: Авто / Светлая / Тёмная
- Уведомления: загрузка файла, масштаб, звук вкладки
- `Alt+Shift+C` — копировать адрес · `Alt+Shift+D` — закрыть одинаковые вкладки · `Alt+Shift+Z` — режим фокуса
- Часы экрана блокировки и на новой вкладке Firefox / LibreWolf / Waterfox
- Новый вид снимков экрана и плашки демонстрации экрана

### 📄 Просмотрщик PDF
- Новая панель и иконки; в теме iOS парит над страницами
- Тема интерфейса (авто / светлая / тёмная) и цвет страниц (бумага / сепия / ночь)
- **Рисование как в Edge** — без рамок, рисунок хватается только за линии, рядом можно рисовать дальше
- Открывает PDF на той странице, где вы остановились
- **Закладки страниц** с заметками — кнопка-ленточка, `Ctrl+B` для текущей страницы
- Быстрый текст — клик по пропуску «……» или двойной клик по пустому месту
- Своя палитра цветов вместо системного окна Windows
- Сам перерисовывает страницы после переключения видеокарты

### Скриншоты
См. раздел [Screenshots](#screenshots) выше.

### Установка
1. Скачайте последний релиз (или `Code → Download ZIP`) и распакуйте.
2. Запустите **`Setup.cmd`** и разрешите права администратора (один раз, чтобы положить загрузчик в папку браузера).
3. Выберите тему, обои, акцент, светлую/тёмную, скругления, анимации и функции, отметьте браузеры.
4. Нажмите **Установить** и перезапустите браузер.

Консольный вариант — `install.cmd`. Тема браузера должна быть встроенной: **«Системная тема — авто»**.

### Удаление
`Setup.cmd` → **«Удалить оформление»** (или `uninstall.cmd`). Ваши собственные стили не трогаются.

### После обновления браузера
Если пропали кнопки на панели или функции PDF — запустите `Setup.cmd` ещё раз.

Неофициальный мод, не связан с Mozilla и Ablaze. Используйте на свой страх и риск. Лицензия MIT.
