#!/usr/bin/env python3
"""Floorp Modern — дополнительные темы: Material You, Windows 11 Fluent, macOS, Nothing.

Каждая тема — надстройка поверх базового оформления (One UI), как и тема iOS:
установщик вставляет её перед END-маркерами базовых блоков. Для каждой темы
пишутся три файла: <id>-chrome.css, <id>-content.css, <id>-pdf.css.

Тема описывается словарём: цвета (через light-dark для светлой/тёмной),
скругления, шрифт, цвет плиток главного меню и свои дополнения CSS.
Цвет акцента везде берётся как var(--fm-user-accent, ...), чтобы установщик
мог заменить его выбранным пользователем."""

import sys, pathlib

UA = "var(--fm-user-accent, AccentColor)"   # акцент Windows (или выбранный в установщике)

TILE_IDS = [
    "#appMenu-new-tab-button2", "#appMenu-new-window-button2", "#appMenu-new-classic-window-button",
    "#appMenu-new-private-window-button2", "#appMenu-history-button", "#appMenu-bookmarks-button",
    "#appMenu-downloads-button", "#appMenu-passwords-button", "#appMenu-extensions-themes-button",
    "#appMenu-unified-extensions-button", "#appMenu-print-button2", "#appMenu-save-file-button2",
    "#appMenu-translate-button", "#appMenu-find-button2", "#appMenu-settings-button", "#appMenu-more-button2",
    "#appMenu-help-button2", "#appMenu-profiles-button", "#appMenu-create-profile-button",
    "#appMenu-tab-groups-button", "#appMenu-quit-button2", "#appMenu-fullscreen-button2",
]
TILE_SEL = ", ".join(TILE_IDS)
PREFIXES = '@-moz-document url-prefix("about:"), url-prefix("chrome://browser/content/"), url-prefix("chrome://mozapps/"), url-prefix("chrome://global/content/")'
NEWTAB = '@-moz-document url-prefix("chrome://noraneko-newtab/"), url("about:newtab"), url("about:home")'
CLOCK = ".absolute.top-4.right-4"
SEARCH = ".group.cursor-pointer:has(input[readonly])"
SEARCH_INPUT = SEARCH + " :is(input, input:focus, input:hover)"

THEMES = {}

# ------------------------------------------------------------------ Material You
THEMES["material"] = dict(
    name="Material You",
    accent=f"light-dark(color-mix(in srgb, {UA} 80%, black), color-mix(in srgb, {UA} 55%, white))",
    on_accent="light-dark(#ffffff, #10131a)",
    frame=f"light-dark(color-mix(in srgb, {UA} 5%, #fbf9fd), color-mix(in srgb, {UA} 7%, #111317))",
    bar=f"light-dark(color-mix(in srgb, {UA} 10%, #ffffff), color-mix(in srgb, {UA} 12%, #1b1d22))",
    field=f"light-dark(color-mix(in srgb, {UA} 14%, #ffffff), color-mix(in srgb, {UA} 18%, #22252b))",
    menu=f"light-dark(color-mix(in srgb, {UA} 8%, #f7f5fa), color-mix(in srgb, {UA} 14%, #202328))",
    ink="light-dark(#1b1b1f, #e4e2e6)", muted="light-dark(#5e5e66, #a3a3ad)",
    line=f"light-dark(color-mix(in srgb, {UA} 14%, transparent), color-mix(in srgb, {UA} 18%, transparent))",
    hover=f"color-mix(in srgb, {UA} 12%, transparent)", press=f"color-mix(in srgb, {UA} 20%, transparent)",
    soft=f"color-mix(in srgb, {UA} 24%, transparent)",
    radius="28px", r_menu="24px", r_item="999px", r_tab="999px", r_url="999px", r_btn="999px",
    font='"Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif',
    tile="var(--fm-accent)", tile_radius="50%", tile_mono=False,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* вкладки и закладки — тональные «таблетки», как в Android 16 */
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: var(--fm-soft) !important; box-shadow: none !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-ink) !important; font-weight: 600 !important; }
#urlbar-background, .urlbar-background { background-color: var(--fm-field) !important; box-shadow: none !important; }
#urlbar { --urlbar-min-height: 42px !important; }
#nav-bar { padding-block: 6px !important; }
menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]) { background-color: var(--fm-soft) !important; }
#appMenu-mainView .subviewbutton:not([disabled]):hover { background: var(--fm-soft) !important; }
""",
    newtab=rf"""
  html {{ background: color-mix(in srgb, {UA} 25%, #0d0f14) !important; }}
  #root::before {{
    background:
      radial-gradient(60% 60% at 20% 20%, color-mix(in srgb, {UA} 70%, transparent), transparent 70%),
      radial-gradient(55% 55% at 85% 80%, color-mix(in srgb, {UA} 45%, #ff9e80), transparent 70%),
      color-mix(in srgb, {UA} 22%, #0d0f14) !important;
  }}
  /* часы Pixel: часы над минутами */
  {CLOCK} .tabular-nums {{
    display: block !important; width: 2.4ch !important; font-variant-numeric: tabular-nums !important; margin-inline: auto !important;
    text-align: center !important; word-break: break-all !important;
    font-size: clamp(84px, 10.5vw, 160px) !important; font-weight: 400 !important;
    line-height: .86 !important; letter-spacing: 0 !important;
    color: color-mix(in srgb, {UA} 35%, white) !important; text-shadow: none !important;
  }}
  {CLOCK} .tabular-nums > .animate-pulse {{ display: none !important; }}
  {CLOCK} > div > .flex {{ flex-direction: column-reverse !important; gap: 14px !important; }}
  {CLOCK} {{ top: 7vh !important; }}
  .w-full.min-h-screen.flex.flex-col.justify-center.items-center {{ padding-top: 38vh !important; }}
  {SEARCH} {{
    border-radius: 999px !important; border: 0 !important;
    background: color-mix(in srgb, {UA} 30%, #1b1d22) !important;
    box-shadow: 0 10px 30px rgb(0 0 0 / .25) !important;
  }}
""",
    pdf_bar=f"light-dark(color-mix(in srgb, {UA} 8%, #ffffff), color-mix(in srgb, {UA} 12%, #1b1d22))",
    pdf_well=f"light-dark(color-mix(in srgb, {UA} 14%, #ffffff), color-mix(in srgb, {UA} 18%, #24272d))",
)

# ------------------------------------------------------------------ Windows 11 Fluent
THEMES["fluent"] = dict(
    name="Windows 11",
    accent=f"light-dark({UA}, color-mix(in srgb, {UA} 70%, white))",
    on_accent="light-dark(#ffffff, #000000)",
    frame="light-dark(#f3f3f3, #202020)", bar="light-dark(#fbfbfb, #2b2b2b)",
    field="light-dark(#ffffff, #2d2d2d)", menu="light-dark(#f9f9f9, #2c2c2c)",
    ink="light-dark(#1a1a1a, #ffffff)", muted="light-dark(#5f5f5f, #c5c5c5)",
    line="light-dark(rgb(0 0 0 / .08), rgb(255 255 255 / .08))",
    hover="light-dark(rgb(0 0 0 / .04), rgb(255 255 255 / .06))",
    press="light-dark(rgb(0 0 0 / .08), rgb(255 255 255 / .04))",
    soft=f"color-mix(in srgb, {UA} 14%, transparent)",
    radius="8px", r_menu="8px", r_item="4px", r_tab="6px", r_url="4px", r_btn="4px",
    font='"Segoe UI Variable Text", "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif',
    tile="transparent", tile_radius="4px", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Fluent: выделение — тонкий акцентный «индикатор» слева, как в меню Windows 11 */
menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]),
.subviewbutton:not([disabled]):hover, #appMenu-mainView .subviewbutton:not([disabled]):hover {
  background-color: var(--fm-hover) !important; color: var(--fm-ink) !important;
}
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: var(--fm-bar) !important;
  box-shadow: 0 0 0 1px var(--fm-line), 0 1px 2px light-dark(rgb(0 0 0 / .06), rgb(0 0 0 / .4)) !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-ink) !important; }
#tabbrowser-tabs[orient="vertical"] .tabbrowser-tab[selected] > .tab-stack > .tab-background {
  box-shadow: inset 3px 0 0 var(--fm-accent), 0 0 0 1px var(--fm-line) !important;
}
#urlbar-background, .urlbar-background {
  background-color: var(--fm-field) !important;
  box-shadow: inset 0 -1px 0 light-dark(rgb(0 0 0 / .14), rgb(255 255 255 / .1)) !important;
}
#urlbar:is([focused], [open]) > :is(#urlbar-background, .urlbar-background) {
  box-shadow: inset 0 -2px 0 var(--fm-accent) !important;
}
#PlacesToolbarItems > .bookmark-item { background: transparent !important; box-shadow: none !important; }
#PlacesToolbarItems > .bookmark-item:hover { background: var(--fm-hover) !important; }
.tabbrowser-tab .tab-label, #urlbar-input { font-size: 12.5px !important; }
""",
    newtab=rf"""
  html {{ background: #0b1a3a !important; }}
  /* обои в духе «Bloom» Windows 11 */
  #root::before {{
    animation: none !important;
    background:
      radial-gradient(45% 55% at 52% 60%, rgb(120 170 255 / .9), transparent 62%),
      radial-gradient(35% 40% at 40% 50%, rgb(40 100 230 / .9), transparent 70%),
      radial-gradient(60% 60% at 70% 45%, rgb(80 60 200 / .7), transparent 70%),
      linear-gradient(160deg, #07122b, #0b2a6b 60%, #0a1838) !important;
  }}
  {CLOCK} > div > .flex {{ flex-direction: column !important; gap: 0 !important; }}
  {CLOCK} .tabular-nums {{
    font-family: "Segoe UI Variable Display", "Segoe UI", sans-serif !important;
    font-weight: 600 !important; font-size: clamp(90px, 11vw, 150px) !important;
    letter-spacing: -0.01em !important; text-shadow: 0 2px 20px rgb(0 0 0 / .3) !important;
  }}
  {CLOCK} .tabular-nums > .animate-pulse {{ animation: none !important; opacity: 1 !important; }}
  {CLOCK} .flex-col.text-right > div {{ font-size: 22px !important; font-weight: 500 !important; }}
  {SEARCH} {{
    border-radius: 8px !important; border: 0 !important; min-height: 50px !important;
    background: rgb(32 32 32 / .85) !important;
    box-shadow: inset 0 -2px 0 {UA}, 0 16px 40px rgb(0 0 0 / .3) !important;
  }}
""",
    pdf_bar="light-dark(#fbfbfb, #2b2b2b)", pdf_well="light-dark(#ffffff, #323232)",
)

# ------------------------------------------------------------------ macOS
THEMES["macos"] = dict(
    name="macOS",
    accent="light-dark(var(--fm-user-accent, #007AFF), var(--fm-user-accent, #0A84FF))",
    on_accent="#ffffff",
    frame="light-dark(#e7e5ea, #1f1e23)", bar="light-dark(#f6f5f8, #2a292f)",
    field="light-dark(#ffffff, #38373d)", menu="light-dark(rgb(246 245 248 / .97), rgb(40 39 44 / .97))",
    ink="light-dark(#1d1d1f, #f5f5f7)", muted="light-dark(#6e6e73, #98989d)",
    line="light-dark(rgb(0 0 0 / .1), rgb(255 255 255 / .1))",
    hover="light-dark(rgb(0 0 0 / .05), rgb(255 255 255 / .07))",
    press="light-dark(rgb(0 0 0 / .1), rgb(255 255 255 / .12))",
    soft="light-dark(rgb(0 122 255 / .14), rgb(10 132 255 / .24))",
    radius="12px", r_menu="12px", r_item="6px", r_tab="8px", r_url="10px", r_btn="7px",
    font='"SF Pro Display", "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif',
    tile="var(--fm-tile-color)", tile_radius="7px", tile_mono=False,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* кнопки окна — «светофор» macOS */
.titlebar-buttonbox .titlebar-button {
  list-style-image: none !important; padding: 0 7px !important; background: transparent !important;
}
.titlebar-buttonbox .titlebar-button > .toolbarbutton-icon {
  width: 13px !important; height: 13px !important; border-radius: 50% !important;
  box-shadow: inset 0 0 0 .5px rgb(0 0 0 / .25) !important;
}
.titlebar-close > .toolbarbutton-icon { background: #ff5f57 !important; }
.titlebar-min > .toolbarbutton-icon { background: #febc2e !important; }
:is(.titlebar-max, .titlebar-restore) > .toolbarbutton-icon { background: #28c840 !important; }
:root:not([tabsintitlebar]) .titlebar-buttonbox .titlebar-button:not(:hover) > .toolbarbutton-icon { filter: saturate(.9); }
.titlebar-buttonbox .titlebar-button:hover > .toolbarbutton-icon { filter: brightness(.9); }
/* меню как в macOS: выделение — сплошной синий, белый текст */
menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]) {
  background-color: var(--fm-accent) !important; color: #fff !important;
}
menupopup > :is(menuitem, menu) { min-height: 26px !important; padding-block: 3px !important; }
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: var(--fm-field) !important;
  box-shadow: 0 1px 2px light-dark(rgb(0 0 0 / .12), rgb(0 0 0 / .5)), 0 0 0 .5px var(--fm-line) !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-ink) !important; }
#urlbar-background, .urlbar-background { background-color: var(--fm-field) !important; }
#urlbar:not([focused], [open]) #urlbar-input { text-align: center !important; }
#PlacesToolbarItems > .bookmark-item { background: transparent !important; box-shadow: none !important; }
#PlacesToolbarItems > .bookmark-item:hover { background: var(--fm-hover) !important; }
""",
    tiles={  # цветные «иконки приложений» macOS
        "#appMenu-new-tab-button2": "#0A84FF", "#appMenu-history-button": "#FF9F0A",
        "#appMenu-bookmarks-button": "#FFD60A", "#appMenu-downloads-button": "#30D158",
        "#appMenu-passwords-button": "#8E8E93", "#appMenu-extensions-themes-button, #appMenu-unified-extensions-button": "#BF5AF2",
        "#appMenu-settings-button": "#8E8E93", "#appMenu-quit-button2": "#FF453A",
        "#appMenu-new-private-window-button2": "#5E5CE6", "#appMenu-translate-button": "#64D2FF",
    },
    newtab=r"""
  html { background: #1a1030 !important; }
  /* обои в духе macOS: тёплые и холодные волны */
  #root::before {
    animation: none !important;
    background:
      radial-gradient(70% 50% at 20% 85%, rgb(255 140 60 / .85), transparent 65%),
      radial-gradient(60% 55% at 85% 20%, rgb(90 120 255 / .85), transparent 65%),
      radial-gradient(55% 50% at 60% 60%, rgb(200 70 160 / .7), transparent 70%),
      linear-gradient(170deg, #1d1440, #3a1d5c 50%, #20123a) !important;
  }
  .absolute.top-4.right-4 > div > .flex { flex-direction: column-reverse !important; gap: 0 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div { font-size: 20px !important; font-weight: 600 !important; color: rgb(255 255 255 / .9) !important; }
  .absolute.top-4.right-4 .tabular-nums {
    font-weight: 600 !important; font-size: clamp(100px, 12vw, 180px) !important;
    letter-spacing: -0.02em !important; color: rgb(255 255 255 / .92) !important;
    text-shadow: 0 2px 30px rgb(0 0 0 / .25) !important;
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 14px !important; border: 0 !important;
    background: rgb(255 255 255 / .16) !important; backdrop-filter: blur(24px) saturate(180%) !important;
    box-shadow: inset 0 0 0 .5px rgb(255 255 255 / .3), 0 16px 40px rgb(0 0 0 / .3) !important;
  }
""",
    pdf_bar="light-dark(#f6f5f8, #2a292f)", pdf_well="light-dark(#ffffff, #38373d)",
)

# ------------------------------------------------------------------ Nothing
THEMES["nothing"] = dict(
    name="Nothing",
    accent="var(--fm-user-accent, #D71921)", on_accent="#ffffff",
    frame="light-dark(#f2f2f2, #000000)", bar="light-dark(#ffffff, #111111)",
    field="light-dark(#ffffff, #000000)", menu="light-dark(#ffffff, #0d0d0d)",
    ink="light-dark(#000000, #ffffff)", muted="light-dark(#666666, #8a8a8a)",
    line="light-dark(rgb(0 0 0 / .25), rgb(255 255 255 / .22))",
    hover="light-dark(rgb(0 0 0 / .06), rgb(255 255 255 / .08))",
    press="light-dark(rgb(0 0 0 / .12), rgb(255 255 255 / .14))",
    soft="light-dark(rgb(0 0 0 / .08), rgb(255 255 255 / .1))",
    radius="20px", r_menu="20px", r_item="999px", r_tab="999px", r_url="999px", r_btn="999px",
    font='"Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif',
    tile="transparent", tile_radius="50%", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Nothing: монохром, выбранное — «инверсия» (белая таблетка с чёрным текстом) */
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: var(--fm-ink) !important; box-shadow: none !important;
}
.tabbrowser-tab[selected] :is(.tab-label, .tab-close-button) { color: var(--fm-frame) !important; fill: var(--fm-frame) !important; }
#urlbar-background, .urlbar-background {
  background-color: var(--fm-field) !important;
  box-shadow: inset 0 0 0 1px var(--fm-line) !important;
}
#PlacesToolbarItems > .bookmark-item { background: transparent !important; box-shadow: inset 0 0 0 1px var(--fm-line) !important; }
#appMenu-mainView .subviewbutton:is(@TILESEL@) > .toolbarbutton-icon { box-shadow: inset 0 0 0 1px var(--fm-line) !important; }
.panel-header > h1, #appMenu-popup .panel-header h1 {
  font-family: "Cascadia Mono", Consolas, ui-monospace, monospace !important;
  text-transform: uppercase !important; letter-spacing: .12em !important; font-size: 13px !important;
}
.fm-toast-dot, .fm-nowbar-eq { background: var(--fm-accent) !important; }
""",
    newtab=r"""
  html { background: #000 !important; }
  /* чёрный фон с еле заметной точечной сеткой */
  #root::before {
    animation: none !important; inset: 0 !important;
    background: radial-gradient(circle, rgb(255 255 255 / .07) 1px, transparent 1.5px) 0 0 / 22px 22px, #000 !important;
  }
  #root::after { display: none !important; }
  /* часы точками, как на экране Nothing Phone */
  .absolute.top-4.right-4 .tabular-nums {
    font-family: "Segoe UI Black", "Arial Black", "Segoe UI", sans-serif !important;
    font-weight: 900 !important; font-size: clamp(120px, 15vw, 230px) !important; letter-spacing: .04em !important;
    color: transparent !important;
    background: radial-gradient(circle, #fff 42%, transparent 46%) 0 0 / 11px 11px !important;
    -webkit-background-clip: text !important; background-clip: text !important;
    text-shadow: none !important;
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div {
    font-family: "Cascadia Mono", Consolas, monospace !important; text-transform: uppercase !important;
    letter-spacing: .2em !important; font-size: 15px !important; color: #fff !important;
  }
  .absolute.top-4.right-4 .flex-col.text-right > div:first-child::before {
    content: ""; display: inline-block; width: 8px; height: 8px; margin-inline-end: 10px;
    border-radius: 50%; background: var(--fm-user-accent, #D71921); vertical-align: middle;
  }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 999px !important; background: #000 !important;
    border: 1px solid rgb(255 255 255 / .35) !important; box-shadow: none !important;
  }
  .group.cursor-pointer:has(input[readonly]) input { font-family: "Cascadia Mono", Consolas, monospace !important; }
""",
    pdf_bar="light-dark(#ffffff, #0d0d0d)", pdf_well="light-dark(#ffffff, #000000)",
)


def tok(t):
    keys = [("accent", "accent"), ("on-accent", "on_accent"), ("frame", "frame"), ("bar", "bar"), ("field", "field"),
            ("menu", "menu"), ("ink", "ink"), ("muted", "muted"), ("line", "line"), ("hover", "hover"),
            ("press", "press"), ("soft", "soft"), ("radius", "radius"), ("font", "font")]
    return "\n".join(f"  --fm-{css}: {t[py]} !important;" for css, py in keys)


def chrome(tid, t):
    tiles = ""
    if t.get("tiles"):
        tiles = "\n".join(f"{sel} {{ --fm-tile-color: {c}; }}" for sel, c in t["tiles"].items())
        tiles = f"#appMenu-mainView {{ --fm-tile-color: #8E8E93; }}\n" + tiles
    mono = ""
    if t["tile_mono"]:
        mono = """
#appMenu-mainView .subviewbutton:is(@TILESEL@) > .toolbarbutton-icon { box-shadow: none !important; }
@media (prefers-color-scheme: light) {
  #appMenu-mainView .subviewbutton:is(@TILESEL@) > .toolbarbutton-icon { filter: invert(1) !important; }
}"""
    css = f"""
/* ---------------- Тема: {t['name']} ---------------- */
:root, menupopup, panel, tooltip, #urlbar, .urlbarView {{
{tok(t)}
  --fm-ring: color-mix(in srgb, var(--fm-accent) 40%, transparent) !important;
  --fm-ring-focus: color-mix(in srgb, var(--fm-accent) 65%, transparent) !important;
  --fm-ring-glow: color-mix(in srgb, var(--fm-accent) 10%, transparent) !important;
  --panel-background-color: var(--fm-menu) !important;
  --arrowpanel-background: var(--fm-menu) !important;
  --panel-border-radius: {t['r_menu']} !important;
  --arrowpanel-border-radius: {t['r_menu']} !important;
  --menuitem-border-radius: {t['r_item']} !important;
  --arrowpanel-menuitem-border-radius: {t['r_item']} !important;
  --urlbarview-border-radius: {t['r_menu']} !important;
  --toolbarbutton-border-radius: {t['r_btn']} !important;
  --tab-border-radius: {t['r_tab']} !important;
  --urlbarview-background-color-selected: var(--fm-soft) !important;
}}
:root:not([inDOMFullscreen], [inFullscreen]) #tabbrowser-tabpanels .browserContainer {{ border-radius: var(--fm-radius) !important; }}
menupopup::part(content), panel::part(content) {{
  border-radius: {t['r_menu']} !important; background-color: var(--fm-menu) !important; background-image: none !important;
}}
menupopup > :is(menuitem, menu), .subviewbutton, #appMenu-mainView .subviewbutton {{ border-radius: {t['r_item']} !important; }}
.tabbrowser-tab > .tab-stack > .tab-background {{ border-radius: {t['r_tab']} !important; }}
#urlbar-background, .urlbar-background {{ border-radius: {t['r_url']} !important; }}
#urlbar[open] > :is(#urlbar-background, .urlbar-background) {{ border-radius: {t['r_menu']} !important; }}
toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack, .toolbarbutton-text),
#PlacesToolbarItems > .bookmark-item, .urlbarView-row-inner, .tab-close-button {{ border-radius: {t['r_btn']} !important; }}
.urlbarView-favicon {{ border-radius: {t['r_btn']} !important; }}
#appMenu-mainView .subviewbutton:is(@TILESEL@) > .toolbarbutton-icon {{
  border-radius: {t['tile_radius']} !important; background: {t['tile']} !important;
}}
moz-toggle {{ --toggle-background-color-pressed: {t['toggle']} !important; }}
.fm-nowbar, .fm-toast {{ border-radius: {t['r_menu'] if t['r_btn'] != '999px' else '999px'} !important; }}
{tiles}
{mono}
{t['chrome_extra']}
"""
    return css.replace("@TILESEL@", TILE_SEL)


def content(tid, t):
    ctok = tok(t).replace("\n  ", "\n    ")
    r_card = t["radius"]
    return f"""
/* ---------------- Тема: {t['name']} ---------------- */
{PREFIXES} {{
  :root {{
  {ctok}
    --color-accent-primary: var(--fm-accent) !important;
    --button-background-color-primary: var(--fm-accent) !important;
    --button-text-color-primary: var(--fm-on-accent) !important;
    --link-color: var(--fm-accent) !important;
    --focus-outline-color: var(--fm-accent) !important;
    --toggle-background-color-pressed: {t['toggle']} !important;
    --page-nav-button-background-color-selected: var(--fm-soft) !important;
    --page-nav-button-text-color-selected: var(--fm-accent) !important;
    --card-border-radius: {r_card} !important;
    --box-border-radius: {r_card} !important;
    --button-border-radius: {t['r_btn']} !important;
    --input-text-border-radius: {t['r_url']} !important;
    --select-border-radius: {t['r_btn']} !important;
    --page-nav-button-border-radius: {t['r_item']} !important;
  }}
  :is(setting-group, groupbox):not([hidden]), .card, .addon.card, moz-card {{ border-radius: {r_card} !important; }}
  button:not(.ghost-button):not([type="icon"]), select, menulist, input[type="search"], input[type="text"] {{ border-radius: {t['r_btn']} !important; }}
  .category, .page-nav-button {{ border-radius: {t['r_item']} !important; }}
}}

@-moz-document url-prefix("chrome://noraneko-settings/") {{
  :root, :root[data-theme], .floorp-standard-ui {{
  {ctok}
    --floorp-brand: var(--fm-accent) !important;
    --floorp-action: var(--fm-accent) !important;
    --floorp-focus: var(--fm-accent) !important;
    --floorp-switch-on: {t['toggle']} !important;
    --chakra-colors-purple-solid: var(--fm-accent) !important;
    --chakra-colors-purple-fg: var(--fm-accent) !important;
    --chakra-colors-purple-focus-ring: var(--fm-accent) !important;
    --chakra-colors-purple-subtle: var(--fm-soft) !important;
  }}
}}

{NEWTAB} {{
{t['newtab']}
}}
"""


def pdf(tid, t):
    return f"""
/* ---------------- Тема: {t['name']} ---------------- */
:root:has(#outerContainer #viewerContainer) {{
  & {{
    --x-accent: {t['accent']} !important;
    --x-on-accent: {t['on_accent']} !important;
    --x-ground: {t['frame']} !important;
    --x-rail: {t['frame']} !important;
    --x-bar: {t['pdf_bar']} !important;
    --x-well: {t['pdf_well']} !important;
    --x-field: {t['field']} !important;
    --x-line: {t['line']} !important;
    --x-ink: {t['ink']} !important;
    --x-muted: {t['muted']} !important;
    --x-radius: {'4px' if t['radius'] == '8px' else '10px'} !important;
  }}
  & #toolbarViewerLeft,
  & #toolbarViewerMiddle,
  & #editorModeButtons,
  & #toolbarViewerRight > .toolbarHorizontalGroup:not(#editorModeButtons) {{ border-radius: {t['r_btn'] if t['r_btn'] != '999px' else '999px'} !important; }}
  & .toolbarButton:not(.labeled) {{ border-radius: {t['r_btn']} !important; }}
}}
"""


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for tid, t in THEMES.items():
        for name, text in ((f"{tid}-chrome.css", chrome(tid, t)), (f"{tid}-content.css", content(tid, t)), (f"{tid}-pdf.css", pdf(tid, t))):
            assert text.count("{") == text.count("}"), name
            (out / name).write_text(text, encoding="utf-8")
    print("ok:", ", ".join(THEMES))
