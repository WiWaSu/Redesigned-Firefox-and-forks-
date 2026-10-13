#!/usr/bin/env python3
"""Redesigned Fox — дополнительные темы: Material You, Windows 11, macOS, Nothing,
Night Drive, Aero, Retro 98, Terminal, Paper, Cyberpunk.

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


# ------------------------------------------------------------------ Night Drive
# идея с Reddit: стекло iOS + тонкие часы One UI, размытые огни ночной дороги
# отодвинуты к краям, запотевшее окно машины
THEMES["nightdrive"] = dict(
    name="Night Drive",
    accent="var(--fm-user-accent, #FFB25B)", on_accent="#1a1205",
    frame="#07080d", bar="#151822", field="#1b1f2b", menu="rgb(21 24 33 / .94)",
    ink="#eef0f6", muted="#9aa0b4",
    line="rgb(255 255 255 / .08)", hover="rgb(255 255 255 / .07)", press="rgb(255 255 255 / .12)",
    soft="color-mix(in srgb, var(--fm-user-accent, #FFB25B) 18%, transparent)",
    radius="22px", r_menu="22px", r_item="12px", r_tab="12px", r_url="14px", r_btn="999px",
    font='"Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif',
    tile="rgb(255 255 255 / .1)", tile_radius="10px", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Night Drive: тёмное стекло, тёплый свет фар */
#urlbar-background, .urlbar-background {
  background-color: rgb(255 255 255 / .06) !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .08), 0 0 0 1px rgb(255 255 255 / .06) !important;
}
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: rgb(255 255 255 / .09) !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .12), 0 6px 18px rgb(0 0 0 / .35) !important;
}
.tabbrowser-tab[selected] .tab-label { color: #fff !important; }
menupopup::part(content), panel::part(content) {
  backdrop-filter: blur(24px) saturate(1.4) !important;
  border: 1px solid rgb(255 255 255 / .1) !important;
}
#tabbrowser-tabpanels .browserContainer { box-shadow: 0 0 0 1px rgb(255 255 255 / .05), 0 18px 50px rgb(0 0 0 / .6) !important; }
""",
    newtab=r"""
  html { background: #05060b !important; }
  /* размытые огни ночной дороги — только по краям, центр тёмный */
  #root::before {
    animation: none !important; inset: 0 !important;
    background:
      radial-gradient(9% 12% at 6% 78%, rgb(255 60 50 / .85), transparent 70%),
      radial-gradient(7% 9% at 15% 90%, rgb(255 40 40 / .7), transparent 70%),
      radial-gradient(11% 14% at 92% 72%, rgb(255 178 91 / .8), transparent 70%),
      radial-gradient(8% 11% at 83% 88%, rgb(255 210 140 / .65), transparent 70%),
      radial-gradient(10% 13% at 96% 18%, rgb(80 200 255 / .55), transparent 70%),
      radial-gradient(7% 9% at 4% 16%, rgb(255 150 60 / .55), transparent 70%),
      radial-gradient(6% 8% at 24% 8%, rgb(120 160 255 / .4), transparent 70%),
      radial-gradient(5% 7% at 74% 6%, rgb(255 120 80 / .4), transparent 70%),
      radial-gradient(70% 55% at 50% 50%, #0a0c14, #04050a 100%) !important;
  }
  /* запотевшее стекло: лёгкая дымка и мелкие капли */
  #root::after {
    content: "" !important; position: fixed !important; inset: 0 !important; z-index: -1 !important; pointer-events: none !important;
    background:
      radial-gradient(circle at 30% 40%, rgb(255 255 255 / .06) 0 1.2px, transparent 1.6px) 0 0 / 23px 29px,
      radial-gradient(circle at 70% 60%, rgb(255 255 255 / .05) 0 0.9px, transparent 1.3px) 0 0 / 17px 21px,
      linear-gradient(180deg, rgb(200 210 230 / .07), rgb(200 210 230 / .02) 60%, rgb(200 210 230 / .06)) !important;
  }
  /* часы One UI: тонкие и огромные */
  .absolute.top-4.right-4 .tabular-nums {
    font-family: "Segoe UI Variable Display", "Segoe UI", sans-serif !important;
    font-weight: 200 !important; font-size: clamp(110px, 13vw, 200px) !important; letter-spacing: .02em !important;
    color: rgb(255 255 255 / .92) !important; text-shadow: 0 0 40px rgb(255 178 91 / .25) !important;
  }
  .absolute.top-4.right-4 .flex-col.text-right > div { color: rgb(255 255 255 / .75) !important; }
  .group.cursor-pointer:has(input[readonly]) {
    background: rgb(255 255 255 / .07) !important; border: 1px solid rgb(255 255 255 / .12) !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .1), 0 20px 50px rgb(0 0 0 / .5) !important;
    backdrop-filter: blur(20px) !important;
  }
  .inline-block.backdrop-blur-sm.p-3 { background: rgb(255 255 255 / .06) !important; border-color: rgb(255 255 255 / .1) !important; }
""",
    pdf_bar="#151822", pdf_well="#1b1f2b",
)

# ------------------------------------------------------------------ Aero (Windows 7)
THEMES["aero"] = dict(
    name="Aero",
    accent="var(--fm-user-accent, #2B7CD3)", on_accent="#ffffff",
    frame="light-dark(#bcd3ee, #14223a)", bar="light-dark(rgb(255 255 255 / .75), rgb(30 50 85 / .8))",
    field="light-dark(#ffffff, #1b2b48)", menu="light-dark(#f2f6fb, #1a2944)",
    ink="light-dark(#0b1a2e, #eaf2ff)", muted="light-dark(#4a5f7a, #9fb4d4)",
    line="light-dark(rgb(30 60 110 / .25), rgb(160 200 255 / .2))",
    hover="light-dark(rgb(43 124 211 / .12), rgb(120 180 255 / .14))",
    press="light-dark(rgb(43 124 211 / .22), rgb(120 180 255 / .22))",
    soft="light-dark(rgb(43 124 211 / .18), rgb(120 180 255 / .2))",
    radius="8px", r_menu="6px", r_item="3px", r_tab="6px", r_url="4px", r_btn="4px",
    font='"Segoe UI", Tahoma, sans-serif',
    tile="linear-gradient(180deg, #5aa2ec, #1f62b5)", tile_radius="5px", tile_mono=False,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Aero: стеклянная голубая рамка с бликом, глянцевые кнопки */
#navigator-toolbox {
  background-image: linear-gradient(180deg, rgb(255 255 255 / .55), rgb(255 255 255 / .1) 45%, transparent 46%),
                    linear-gradient(180deg, light-dark(#9fc2ea, #23406e), light-dark(#c9dcf2, #14223a)) !important;
}
toolbar .toolbarbutton-1:not([disabled]):hover > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  background: linear-gradient(180deg, rgb(255 255 255 / .85), rgb(200 225 250 / .7) 50%, rgb(160 205 245 / .7) 51%, rgb(200 230 255 / .8)) !important;
  box-shadow: inset 0 0 0 1px rgb(60 120 190 / .6) !important;
}
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: linear-gradient(180deg, rgb(255 255 255 / .95), light-dark(#e3eefb, #2a4774)) !important;
  box-shadow: inset 0 0 0 1px rgb(60 120 190 / .55), 0 1px 3px rgb(0 0 0 / .2) !important;
}
.tabbrowser-tab[selected] .tab-label { color: light-dark(#0b1a2e, #ffffff) !important; }
#urlbar-background, .urlbar-background { box-shadow: inset 0 1px 2px rgb(0 0 0 / .2), 0 0 0 1px rgb(60 110 170 / .5) !important; }
menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) {
  background: linear-gradient(180deg, rgb(230 242 255), rgb(200 225 250)) !important; color: #0b1a2e !important;
  box-shadow: inset 0 0 0 1px rgb(120 170 230) !important;
}
""",
    newtab=r"""
  html { background: #0b3a7a !important; }
  /* как обои Windows 7: синее небо и светлые ленты */
  #root::before {
    animation: none !important; inset: 0 !important;
    background:
      radial-gradient(60% 40% at 30% 70%, rgb(140 220 255 / .55), transparent 70%),
      linear-gradient(160deg, transparent 40%, rgb(255 255 255 / .18) 50%, transparent 60%),
      linear-gradient(170deg, transparent 55%, rgb(160 230 120 / .35) 62%, transparent 70%),
      linear-gradient(180deg, #0b4fa8, #0a2f6b) !important;
  }
  .absolute.top-4.right-4 .tabular-nums {
    font-family: "Segoe UI", sans-serif !important; font-weight: 300 !important;
    font-size: clamp(100px, 12vw, 170px) !important; color: #fff !important;
    text-shadow: 0 0 18px rgb(255 255 255 / .55), 0 2px 6px rgb(0 0 0 / .4) !important;
  }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 6px !important; border: 1px solid rgb(255 255 255 / .6) !important;
    background: linear-gradient(180deg, rgb(255 255 255 / .55), rgb(255 255 255 / .3)) !important;
    box-shadow: inset 0 1px 0 #fff, 0 10px 30px rgb(0 0 0 / .3) !important; backdrop-filter: blur(12px) !important;
  }
  .group.cursor-pointer:has(input[readonly]) input, .group.cursor-pointer:has(input[readonly]) input::placeholder { color: #0b1a2e !important; }
  .group.cursor-pointer:has(input[readonly]) svg { color: #0b1a2e !important; }
  .inline-block.backdrop-blur-sm.p-3 { border-radius: 8px !important; background: rgb(10 40 90 / .45) !important; border-color: rgb(255 255 255 / .55) !important; backdrop-filter: blur(12px) !important; }
  .inline-block.backdrop-blur-sm.p-3 * { color: #fff !important; text-shadow: 0 1px 2px rgb(0 0 0 / .5); }
""",
    pdf_bar="light-dark(#e8f0fa, #1a2944)", pdf_well="light-dark(#ffffff, #1b2b48)",
)

# ------------------------------------------------------------------ Retro 98
THEMES["retro"] = dict(
    name="Retro 98",
    accent="var(--fm-user-accent, #000080)", on_accent="#ffffff",
    frame="#c0c0c0", bar="#ffffff", field="#ffffff", menu="#c0c0c0",
    ink="#000000", muted="#404040",
    line="#808080", hover="rgb(0 0 128 / .12)", press="rgb(0 0 128 / .22)",
    soft="rgb(0 0 128 / .14)",
    radius="0px", r_menu="0px", r_item="0px", r_tab="0px", r_url="0px", r_btn="0px",
    font='Tahoma, "MS Sans Serif", "Segoe UI", sans-serif',
    tile="#c0c0c0", tile_radius="0px", tile_mono=False,
    toggle="#000080",
    chrome_extra=r"""
/* Retro 98: серые «выпуклые» кнопки, синие заголовки, никаких скруглений */
:root { color-scheme: light !important; }
#navigator-toolbox, #nav-bar, #TabsToolbar, #PersonalToolbar { color: #000 !important; }
toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  background: #c0c0c0 !important;
  box-shadow: inset -1px -1px #404040, inset 1px 1px #ffffff, inset -2px -2px #808080, inset 2px 2px #dfdfdf !important;
  fill: #000 !important;
}
toolbar .toolbarbutton-1:not([disabled]):active > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  box-shadow: inset 1px 1px #404040, inset -1px -1px #ffffff, inset 2px 2px #808080 !important;
}
.tabbrowser-tab > .tab-stack > .tab-background {
  background: #c0c0c0 !important;
  box-shadow: inset -1px 0 #404040, inset 1px 1px #ffffff, inset -2px 0 #808080 !important;
}
.tabbrowser-tab[selected] > .tab-stack > .tab-background { background: #d4d0c8 !important; }
.tabbrowser-tab[selected] .tab-label { color: #000 !important; font-weight: 700 !important; }
#urlbar-background, .urlbar-background {
  background: #fff !important;
  box-shadow: inset 1px 1px #808080, inset -1px -1px #ffffff, inset 2px 2px #404040 !important; outline: none !important;
}
#urlbar-input, .urlbar-input { color: #000 !important; }
menupopup::part(content), panel::part(content) {
  border: 0 !important; box-shadow: inset -1px -1px #404040, inset 1px 1px #ffffff, 2px 2px 0 rgb(0 0 0 / .35) !important;
}
menupopup > :is(menuitem, menu) { color: #000 !important; }
menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]),
.subviewbutton:not([disabled]):hover { background: #000080 !important; color: #fff !important; }
#tabbrowser-tabpanels .browserContainer { box-shadow: inset 0 0 0 2px #808080 !important; }
.fm-toast, .fm-nowbar { border-radius: 0 !important; background: #c0c0c0 !important; color: #000 !important;
  box-shadow: inset -1px -1px #404040, inset 1px 1px #fff, 3px 3px 0 rgb(0 0 0 / .3) !important; }
""",
    newtab=r"""
  html { background: #008080 !important; }
  #root::before { animation: none !important; inset: 0 !important; background: #008080 !important; }
  #root::after { display: none !important; }
  /* часы в «окне» Windows 98 */
  .absolute.top-4.right-4 > div {
    background: #c0c0c0 !important; padding: 34px 26px 18px !important; position: relative;
    box-shadow: inset -1px -1px #000, inset 1px 1px #dfdfdf, inset -2px -2px #808080, inset 2px 2px #fff, 4px 4px 0 rgb(0 0 0 / .35) !important;
    border-radius: 0 !important; backdrop-filter: none !important; border: 0 !important;
  }
  .absolute.top-4.right-4 > div::before {
    content: "Clock"; position: absolute; left: 3px; right: 3px; top: 3px; height: 20px; line-height: 20px; padding-left: 6px;
    background: linear-gradient(90deg, #000080, #1084d0); color: #fff; font: 700 12px Tahoma, sans-serif; text-align: left;
  }
  .absolute.top-4.right-4 .tabular-nums {
    font-family: "Courier New", Consolas, monospace !important; font-weight: 700 !important;
    font-size: clamp(70px, 8vw, 110px) !important; color: #000 !important; text-shadow: none !important;
    background: #fff; padding: 4px 14px; box-shadow: inset 1px 1px #808080, inset 2px 2px #404040;
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div { color: #000 !important; font: 12px Tahoma, sans-serif !important; }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 0 !important; background: #fff !important; border: 0 !important;
    box-shadow: inset 1px 1px #808080, inset -1px -1px #fff, inset 2px 2px #404040, 3px 3px 0 rgb(0 0 0 / .3) !important;
  }
  .group.cursor-pointer:has(input[readonly]) input, .group.cursor-pointer:has(input[readonly]) input::placeholder { color: #000 !important; font-family: Tahoma, sans-serif !important; }
  .group.cursor-pointer:has(input[readonly]) svg { color: #000 !important; }
  .inline-block.backdrop-blur-sm.p-3 { border-radius: 0 !important; background: #c0c0c0 !important; border: 0 !important;
    box-shadow: inset -1px -1px #404040, inset 1px 1px #fff, 3px 3px 0 rgb(0 0 0 / .3) !important; }
  .inline-block.backdrop-blur-sm.p-3 * { color: #000 !important; }
  a.group .overflow-hidden.bg-gray-700 { border-radius: 0 !important; }
""",
    pdf_bar="#c0c0c0", pdf_well="#ffffff",
)

# ------------------------------------------------------------------ Terminal
THEMES["terminal"] = dict(
    name="Terminal",
    accent="var(--fm-user-accent, #33FF66)", on_accent="#000000",
    frame="#030603", bar="#081108", field="#000000", menu="#061006",
    ink="#5CFF85", muted="#2BA84C",
    line="rgb(51 255 102 / .28)", hover="rgb(51 255 102 / .1)", press="rgb(51 255 102 / .18)",
    soft="rgb(51 255 102 / .14)",
    radius="2px", r_menu="2px", r_item="2px", r_tab="2px", r_url="2px", r_btn="2px",
    font='"Cascadia Mono", "Cascadia Code", Consolas, ui-monospace, monospace',
    tile="transparent", tile_radius="2px", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Terminal: зелёный фосфор, моноширинный шрифт, всё прямоугольное */
:root { color-scheme: dark !important; }
#navigator-toolbox, menupopup, panel { text-shadow: 0 0 6px rgb(51 255 102 / .45); }
toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) { fill: var(--fm-ink) !important; }
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: transparent !important; box-shadow: inset 0 0 0 1px var(--fm-accent), 0 0 12px rgb(51 255 102 / .25) !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-accent) !important; }
#urlbar-background, .urlbar-background { background: #000 !important; box-shadow: inset 0 0 0 1px var(--fm-line) !important; }
#urlbar:is([focused], [open]) > :is(#urlbar-background, .urlbar-background) { box-shadow: inset 0 0 0 1px var(--fm-accent), 0 0 14px rgb(51 255 102 / .3) !important; }
menupopup::part(content), panel::part(content) { border: 1px solid var(--fm-line) !important; }
menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) { background: var(--fm-accent) !important; color: #000 !important; text-shadow: none; }
""",
    newtab=r"""
  html { background: #010301 !important; }
  /* экран старого монитора: строки развёртки и свечение */
  #root::before {
    animation: none !important; inset: 0 !important;
    background:
      repeating-linear-gradient(180deg, rgb(0 0 0 / .35) 0 1px, transparent 1px 3px),
      radial-gradient(80% 70% at 50% 45%, rgb(20 80 35 / .55), transparent 75%),
      #010301 !important;
  }
  #root::after { content: "" !important; position: fixed !important; inset: 0 !important; z-index: -1 !important; pointer-events: none !important;
    background: radial-gradient(120% 100% at 50% 50%, transparent 60%, rgb(0 0 0 / .8)) !important; }
  .absolute.top-4.right-4 .tabular-nums {
    font-family: "Cascadia Mono", Consolas, monospace !important; font-weight: 400 !important;
    font-size: clamp(90px, 11vw, 160px) !important; color: #5CFF85 !important;
    text-shadow: 0 0 10px rgb(51 255 102 / .8), 0 0 40px rgb(51 255 102 / .35) !important;
  }
  .absolute.top-4.right-4 .tabular-nums::after { content: "_"; animation: fm-blink 1.1s steps(1) infinite; }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div { font-family: "Cascadia Mono", Consolas, monospace !important; color: #2BA84C !important; text-transform: uppercase; letter-spacing: .15em; }
  .absolute.top-4.right-4 .flex-col.text-right > div:first-child::before { content: "> "; }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 0 !important; background: #000 !important; border: 1px solid rgb(51 255 102 / .5) !important;
    box-shadow: 0 0 18px rgb(51 255 102 / .2) !important;
  }
  .group.cursor-pointer:has(input[readonly]) input { font-family: "Cascadia Mono", Consolas, monospace !important; color: #5CFF85 !important; }
  .group.cursor-pointer:has(input[readonly]) input::placeholder { color: #2BA84C !important; }
  .group.cursor-pointer:has(input[readonly]) svg { color: #5CFF85 !important; }
  .inline-block.backdrop-blur-sm.p-3 { border-radius: 0 !important; background: #000 !important; border: 1px solid rgb(51 255 102 / .35) !important; }
  .inline-block.backdrop-blur-sm.p-3 * { color: #5CFF85 !important; font-family: "Cascadia Mono", Consolas, monospace !important; }
""",
    pdf_bar="#081108", pdf_well="#000000",
)

# ------------------------------------------------------------------ Paper
THEMES["paper"] = dict(
    name="Paper",
    accent="var(--fm-user-accent, #B4532A)", on_accent="#ffffff",
    frame="#efe9de", bar="#f8f4ec", field="#fffdf8", menu="#faf6ee",
    ink="#2b2622", muted="#7a7066",
    line="rgb(43 38 34 / .16)", hover="rgb(43 38 34 / .06)", press="rgb(43 38 34 / .11)",
    soft="color-mix(in srgb, var(--fm-user-accent, #B4532A) 14%, transparent)",
    radius="6px", r_menu="6px", r_item="3px", r_tab="4px", r_url="4px", r_btn="4px",
    font='Georgia, Cambria, "Times New Roman", serif',
    tile="transparent", tile_radius="3px", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Paper: тёплая бумага, засечки, плоско — только тонкие линии */
:root { color-scheme: light !important; }
#navigator-toolbox, #nav-bar, #TabsToolbar { color: var(--fm-ink) !important; }
toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) { fill: var(--fm-ink) !important; }
.tabbrowser-tab[selected] > .tab-stack > .tab-background {
  background: var(--fm-bar) !important; box-shadow: inset 0 -2px 0 var(--fm-accent), 0 0 0 1px var(--fm-line) !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-ink) !important; font-style: italic; }
#urlbar-background, .urlbar-background { background: var(--fm-field) !important; box-shadow: 0 0 0 1px var(--fm-line) !important; }
#tabbrowser-tabpanels .browserContainer { box-shadow: 0 0 0 1px var(--fm-line), 0 2px 8px rgb(60 40 20 / .08) !important; }
menupopup::part(content), panel::part(content) { box-shadow: 0 0 0 1px var(--fm-line), 0 8px 24px rgb(60 40 20 / .12) !important; }
""",
    newtab=r"""
  html { background: #f1ebdf !important; }
  /* бумага: тёплый тон, лёгкие волокна и линейка */
  #root::before {
    animation: none !important; inset: 0 !important;
    background:
      repeating-linear-gradient(180deg, transparent 0 35px, rgb(120 90 60 / .06) 35px 36px),
      radial-gradient(90% 70% at 50% 40%, #fbf7ef, #ece4d5) !important;
  }
  #root::after { display: none !important; }
  .absolute.top-4.right-4 .tabular-nums {
    font-family: Georgia, "Times New Roman", serif !important; font-weight: 400 !important;
    font-size: clamp(100px, 12vw, 170px) !important; color: #2b2622 !important; text-shadow: none !important;
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div { font-family: Georgia, serif !important; font-style: italic; color: #7a7066 !important; }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 0 !important; background: transparent !important; border: 0 !important;
    box-shadow: inset 0 -2px 0 #2b2622 !important; backdrop-filter: none !important;
  }
  .group.cursor-pointer:has(input[readonly]) input { font-family: Georgia, serif !important; color: #2b2622 !important; }
  .group.cursor-pointer:has(input[readonly]) input::placeholder { color: #8a7f74 !important; font-style: italic; }
  .group.cursor-pointer:has(input[readonly]) svg { color: #2b2622 !important; }
  .inline-block.backdrop-blur-sm.p-3 { border-radius: 4px !important; background: #faf6ee !important; border: 1px solid rgb(43 38 34 / .15) !important; box-shadow: none !important; }
  .inline-block.backdrop-blur-sm.p-3 * { color: #2b2622 !important; }
  button.fixed.bottom-4.right-4 { background: #faf6ee !important; color: #2b2622 !important; border-color: rgb(43 38 34 / .2) !important; }
""",
    pdf_bar="#f8f4ec", pdf_well="#fffdf8",
)

# ------------------------------------------------------------------ Cyberpunk
THEMES["cyber"] = dict(
    name="Cyberpunk",
    accent="var(--fm-user-accent, #FCEE0A)", on_accent="#000000",
    frame="#0b0912", bar="#15111f", field="#1a1526", menu="#120e1b",
    ink="#f3f0ff", muted="#a497cc",
    line="rgb(255 0 170 / .32)", hover="rgb(0 240 255 / .1)", press="rgb(0 240 255 / .18)",
    soft="rgb(252 238 10 / .14)",
    radius="4px", r_menu="2px", r_item="0px", r_tab="0px", r_url="0px", r_btn="2px",
    font='Bahnschrift, "Segoe UI", system-ui, sans-serif',
    tile="transparent", tile_radius="0px", tile_mono=True,
    toggle="var(--fm-accent)",
    chrome_extra=r"""
/* Cyberpunk: срезанные углы, жёлтый акцент, неон розовый и голубой */
:root { color-scheme: dark !important; }
.tabbrowser-tab > .tab-stack > .tab-background { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }
.tabbrowser-tab[selected] > .tab-stack > .tab-background { background: var(--fm-accent) !important; box-shadow: none !important; }
.tabbrowser-tab[selected] :is(.tab-label, .tab-close-button) { color: #000 !important; fill: #000 !important; font-weight: 700 !important; }
#urlbar-background, .urlbar-background {
  clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px);
  background: #1a1526 !important; box-shadow: inset 0 0 0 1px rgb(0 240 255 / .5) !important;
}
#urlbar:is([focused], [open]) > :is(#urlbar-background, .urlbar-background) { box-shadow: inset 0 0 0 2px var(--fm-accent) !important; clip-path: none; }
menupopup::part(content), panel::part(content) {
  border: 1px solid rgb(255 0 170 / .55) !important; box-shadow: 0 0 22px rgb(255 0 170 / .25) !important;
}
menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) { background: var(--fm-accent) !important; color: #000 !important; }
#tabbrowser-tabpanels .browserContainer { box-shadow: 0 0 0 1px rgb(0 240 255 / .35), 0 0 30px rgb(255 0 170 / .15) !important; }
""",
    newtab=r"""
  html { background: #07050d !important; }
  /* неоновый город: сетка-пол уходит в даль, розовое и голубое свечение */
  #root::before {
    animation: none !important; inset: 0 !important;
    background:
      linear-gradient(180deg, transparent 58%, rgb(255 0 170 / .0) 58%),
      repeating-linear-gradient(90deg, rgb(0 240 255 / .18) 0 1px, transparent 1px 80px) 0 62% / 100% 38% no-repeat,
      repeating-linear-gradient(180deg, rgb(255 0 170 / .2) 0 1px, transparent 1px 34px) 0 100% / 100% 38% no-repeat,
      radial-gradient(60% 30% at 50% 62%, rgb(255 0 170 / .45), transparent 70%),
      radial-gradient(40% 40% at 85% 15%, rgb(0 240 255 / .3), transparent 70%),
      linear-gradient(180deg, #0a0614, #1a0b2e 60%, #07050d) !important;
  }
  #root::after { display: none !important; }
  .absolute.top-4.right-4 .tabular-nums {
    font-family: Bahnschrift, "Segoe UI", sans-serif !important; font-weight: 700 !important;
    font-size: clamp(100px, 12vw, 170px) !important; color: #FCEE0A !important; letter-spacing: .04em !important;
    text-shadow: -3px 0 rgb(255 0 170 / .85), 3px 0 rgb(0 240 255 / .85), 0 0 30px rgb(252 238 10 / .35) !important;
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div { font-family: Bahnschrift, sans-serif !important; text-transform: uppercase; letter-spacing: .25em; color: #00f0ff !important; }
  .group.cursor-pointer:has(input[readonly]) {
    border-radius: 0 !important; background: rgb(10 6 20 / .85) !important; border: 1px solid #FCEE0A !important;
    clip-path: polygon(18px 0, 100% 0, 100% calc(100% - 18px), calc(100% - 18px) 100%, 0 100%, 0 18px);
    box-shadow: none !important;
  }
  .group.cursor-pointer:has(input[readonly]) input { font-family: Bahnschrift, sans-serif !important; color: #f3f0ff !important; }
  .inline-block.backdrop-blur-sm.p-3 { border-radius: 0 !important; background: rgb(10 6 20 / .8) !important; border: 1px solid rgb(255 0 170 / .5) !important;
    clip-path: polygon(16px 0, 100% 0, 100% calc(100% - 16px), calc(100% - 16px) 100%, 0 100%, 0 16px); }
""",
    pdf_bar="#15111f", pdf_well="#1a1526",
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
