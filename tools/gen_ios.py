#!/usr/bin/env python3
"""Floorp Modern — тема iOS 26 «Liquid Glass».

Надстройка поверх базового оформления One UI: установщик вставляет эти блоки
прямо перед END-маркерами базовых блоков, поэтому удаление работает так же.
Пишет ios-chrome.css, ios-content.css, ios-pdf.css.

Стекло собирается из четырёх слоёв:
  1. обои-градиент под окном (их видно вокруг страницы и под панелями);
  2. полупрозрачная заливка + размытие того, что под ней (backdrop-filter);
  3. «блик» сверху — мягкий градиент от белого к прозрачному;
  4. светящийся кант по краю (inset-тени) и мягкая тень снизу.
Размытие стоит только на маленьких элементах: на больших слоях Firefox тормозит."""

import sys, pathlib

# системные цвета iOS (тёмные варианты)
BLUE, GREEN, ORANGE, RED, PURPLE, GRAY, TEAL, PINK, YELLOW, INDIGO = (
    "#0A84FF", "#30D158", "#FF9F0A", "#FF453A", "#BF5AF2", "#8E8E93", "#40C8E0", "#FF375F", "#FFCC00", "#5E5CE6")

TILES = {
    "#appMenu-new-tab-button2": BLUE,
    "#appMenu-new-window-button2, #appMenu-new-classic-window-button": TEAL,
    "#appMenu-new-private-window-button2": INDIGO,
    "#appMenu-history-button": ORANGE,
    "#appMenu-bookmarks-button": YELLOW,
    "#appMenu-downloads-button": GREEN,
    "#appMenu-passwords-button": GRAY,
    "#appMenu-extensions-themes-button, #appMenu-unified-extensions-button": PURPLE,
    "#appMenu-print-button2": GRAY,
    "#appMenu-save-file-button2": BLUE,
    "#appMenu-translate-button": TEAL,
    "#appMenu-find-button2": BLUE,
    "#appMenu-settings-button": GRAY,
    "#appMenu-more-button2": GRAY,
    "#appMenu-help-button2": BLUE,
    "#appMenu-profiles-button, #appMenu-create-profile-button": PINK,
    "#appMenu-tab-groups-button": TEAL,
    "#appMenu-quit-button2": RED,
    "#appMenu-fullscreen-button2": GRAY,
}
TILE_RULES = "\n".join(f"{sel} {{ --fm-tile: {c} !important; }}" for sel, c in TILES.items())
TILE_SEL = ", ".join(TILES.keys())

# ---------------------------------------------------------------- общие токены
GLASS_TOKENS = r"""
  --fm-accent: light-dark(var(--fm-user-accent, #007AFF), var(--fm-user-accent, #0A84FF)) !important;
  --fm-on-accent: #ffffff !important;
  --fm-frame: light-dark(#EEF1F8, #05060B) !important;
  --fm-bar: light-dark(#FFFFFF, #1C1C1E) !important;
  --fm-field: light-dark(rgb(255 255 255 / .7), rgb(255 255 255 / .1)) !important;
  --fm-menu: light-dark(rgb(250 250 253 / .94), rgb(30 30 34 / .93)) !important;
  --fm-ink: light-dark(#000000, #FFFFFF) !important;
  --fm-muted: light-dark(rgb(60 60 67 / .62), rgb(235 235 245 / .6)) !important;
  --fm-line: light-dark(rgb(60 60 67 / .14), rgb(255 255 255 / .1)) !important;
  --fm-hover: light-dark(rgb(0 0 0 / .05), rgb(255 255 255 / .1)) !important;
  --fm-press: light-dark(rgb(0 0 0 / .1), rgb(255 255 255 / .16)) !important;
  --fm-soft: light-dark(rgb(0 122 255 / .14), rgb(10 132 255 / .24)) !important;
  --fm-radius: 26px !important;
  --fm-font: "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;

  /* материал «жидкое стекло» */
  --lg-fill: light-dark(rgb(255 255 255 / .55), rgb(255 255 255 / .085));
  --lg-fill-strong: light-dark(rgb(255 255 255 / .82), rgb(255 255 255 / .17));
  --lg-sheen: linear-gradient(180deg, light-dark(rgb(255 255 255 / .7), rgb(255 255 255 / .13)) 0%, transparent 58%);
  --lg-rim: inset 0 1px 0 light-dark(rgb(255 255 255 / 1), rgb(255 255 255 / .34)),
            inset 0 -1px 0 light-dark(rgb(255 255 255 / .55), rgb(255 255 255 / .07)),
            inset 1px 0 0 light-dark(rgb(255 255 255 / .6), rgb(255 255 255 / .09)),
            inset -1px 0 0 light-dark(rgb(255 255 255 / .6), rgb(255 255 255 / .09));
  --lg-drop: 0 8px 24px light-dark(rgb(40 50 90 / .14), rgb(0 0 0 / .38)),
             0 1px 3px light-dark(rgb(40 50 90 / .1), rgb(0 0 0 / .35));
  --lg-blur: blur(22px) saturate(190%);
  --lg-wall:
    radial-gradient(55% 75% at 0% 0%, light-dark(rgb(122 170 255 / .55), rgb(10 132 255 / .34)), transparent 70%),
    radial-gradient(45% 70% at 100% 0%, light-dark(rgb(196 160 255 / .55), rgb(94 92 230 / .38)), transparent 70%),
    radial-gradient(55% 60% at 100% 100%, light-dark(rgb(255 172 200 / .5), rgb(255 55 95 / .2)), transparent 70%),
    radial-gradient(50% 60% at 0% 100%, light-dark(rgb(140 228 255 / .5), rgb(64 200 224 / .18)), transparent 70%),
    light-dark(#EEF1F8, #05060B);
"""

# ================================================================ окно браузера
CHROME = r"""
/* ---------------- iOS 26 · Liquid Glass ---------------- */
:root, menupopup, panel, tooltip, #urlbar, .urlbarView {
@GLASS@
  --fm-ring: light-dark(rgb(0 122 255 / .34), rgb(10 132 255 / .42)) !important;
  --fm-ring-focus: light-dark(rgb(0 122 255 / .62), rgb(10 132 255 / .72)) !important;
  --fm-ring-glow: light-dark(rgb(0 122 255 / .1), rgb(10 132 255 / .16)) !important;
  --panel-background-color: var(--fm-menu) !important;
  --arrowpanel-background: var(--fm-menu) !important;
  --urlbarview-background-color-selected: light-dark(rgb(0 0 0 / .06), rgb(255 255 255 / .12)) !important;
}
/* рамка окна прозрачная: всё, что раньше было «чёрным фоном», теперь показывает обои */
:root {
  --fm-frame: transparent !important;
  --sidebar-background-color: transparent !important;
  --panel-sidebar-background-color: transparent !important;
  --toolbox-background-color: transparent !important;
  --toolbox-background-color-inactive: transparent !important;
  --toolbar-background-color: transparent !important;
  --toolbar-bgcolor: transparent !important;
}
:root:not([lwtheme]) :is(#sidebar-main, #sidebar-box, #panel-sidebar-select-box, #panel-sidebar-select-box > *, #sidebar-main > *, #vertical-tabs, #tabbrowser-tabs[orient="vertical"], .sidebar-panel-header, #sidebar-header) {
  background-color: transparent !important;
  background-image: none !important;
}

/* ---------- обои под окном: видны вокруг страницы и сквозь стекло ---------- */
:root:not([lwtheme]) :is(#navigator-toolbox, #nav-bar, #PersonalToolbar, #TabsToolbar, #browser, #sidebar-main, #sidebar-box, #panel-sidebar-select-box, #nora-statusbar) {
  background-color: transparent !important;
}
:root:not([lwtheme]) :is(#navigator-toolbox, #browser) {
  background: var(--lg-wall) !important;
  background-attachment: fixed !important;
}

/* страница — «плавающая» карточка с большим скруглением */
:root:not([inDOMFullscreen], [inFullscreen]) #tabbrowser-tabpanels .browserContainer {
  border-radius: 26px !important;
  box-shadow: 0 0 0 1px light-dark(rgb(255 255 255 / .7), rgb(255 255 255 / .08)),
              0 12px 40px light-dark(rgb(40 50 90 / .16), rgb(0 0 0 / .55)) !important;
}

/* ---------- панель навигации: парящая стеклянная капсула, как в Safari ---------- */
#nav-bar {
  margin: 6px 8px 6px !important;
  padding: 3px 6px !important;
  border-radius: 999px !important;
  background-color: var(--lg-fill) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim), var(--lg-drop) !important;
  /* без backdrop-filter: он сделал бы панель отдельным слоем, и выпадающие
     списки адресной строки могли бы уйти под страницу. Под панелью и так
     плавный градиент, размытие там незаметно */
}
:root[sizemode="maximized"] #nav-bar, :root[sizemode="normal"] #nav-bar { border-top: 0 !important; }

/* кнопки: без заливки, при наведении — маленькая стеклянная «капля» */
toolbar .toolbarbutton-1 {
  --toolbarbutton-hover-background: light-dark(rgb(255 255 255 / .7), rgb(255 255 255 / .14)) !important;
  --toolbarbutton-active-background: light-dark(rgb(255 255 255 / .95), rgb(255 255 255 / .22)) !important;
}
toolbar .toolbarbutton-1:not([disabled]):hover > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  box-shadow: var(--lg-rim) !important;
}
toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  transition: background-color .2s ease, scale .25s cubic-bezier(.3, 1.6, .5, 1) !important;
}
toolbar .toolbarbutton-1:not([disabled]):active > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) { scale: .88; }
toolbarbutton:is([open], [checked]) > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  background-color: var(--lg-fill-strong) !important;
  fill: var(--fm-accent) !important;
  box-shadow: var(--lg-rim) !important;
}

/* ---------- адресная строка: стеклянная капсула внутри капсулы ---------- */
#urlbar-background, .urlbar-background {
  background-color: light-dark(rgb(255 255 255 / .62), rgb(255 255 255 / .09)) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim) !important;
}
#urlbar > :is(#urlbar-background, .urlbar-background),
.urlbar > .urlbar-background {
  box-shadow: var(--lg-rim), 0 0 16px var(--fm-ring-glow) !important;
}
#urlbar:is([focused], [open], [popover-open], [breakout-extend], :focus-within) > :is(#urlbar-background, .urlbar-background),
.urlbar:is([focused], [open], [popover-open], :focus-within) > .urlbar-background {
  box-shadow: var(--lg-rim), 0 0 22px var(--fm-ring-glow) !important;
}
#urlbar[open] > :is(#urlbar-background, .urlbar-background) {
  background-color: var(--fm-menu) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim), 0 24px 60px light-dark(rgb(40 50 90 / .22), rgb(0 0 0 / .6)) !important;
  backdrop-filter: blur(30px) saturate(180%) !important;
  border: 0 !important;
  border-radius: 28px !important;
}
.urlbarView-row:not([selected]):hover > .urlbarView-row-inner { background: var(--fm-hover) !important; }
.urlbarView-row[selected] > .urlbarView-row-inner {
  background: light-dark(rgb(0 0 0 / .06), rgb(255 255 255 / .12)) !important;
  box-shadow: var(--lg-rim) !important;
}
.urlbarView-row[selected] :is(.urlbarView-title, .urlbarView-action, .urlbarView-url) { color: var(--fm-ink) !important; }
.urlbarView-row[selected] .urlbarView-action { color: var(--fm-accent) !important; }
.urlbarView-favicon {
  border-radius: 10px !important;
  background: var(--lg-fill-strong) !important;
  box-shadow: var(--lg-rim) !important;
}
.urlbarView-row[selected] .urlbarView-favicon { background: var(--fm-accent) !important; fill: #fff !important; }

/* ---------- вкладки: стеклянные капли ---------- */
.tabbrowser-tab > .tab-stack > .tab-background { border-radius: 999px !important; }
#tabbrowser-tabs[orient="vertical"] .tabbrowser-tab > .tab-stack > .tab-background { border-radius: 16px !important; }
.tabbrowser-tab:not([selected], [multiselected]):hover > .tab-stack > .tab-background {
  background: var(--lg-fill) !important;
  box-shadow: var(--lg-rim) !important;
}
.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background {
  background-color: var(--lg-fill-strong) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim), var(--lg-drop) !important;
}
.tabbrowser-tab[selected] .tab-label { color: var(--fm-ink) !important; font-weight: 600 !important; }
.tab-close-button:hover { background: var(--lg-fill-strong) !important; }
#tabs-newtab-button > .toolbarbutton-icon, #vertical-tabs-newtab-button {
  border-radius: 999px !important;
}

/* ---------- закладки: просто текст, как в Safari; при наведении — стекло ---------- */
#PlacesToolbarItems > .bookmark-item {
  background: transparent !important;
  box-shadow: none !important;
}
#PlacesToolbarItems > .bookmark-item:hover {
  background: var(--lg-fill) !important;
  box-shadow: var(--lg-rim) !important;
}
#PlacesToolbarItems > .bookmark-item[open] {
  background: var(--lg-fill-strong) !important;
  color: var(--fm-ink) !important;
  box-shadow: var(--lg-rim) !important;
}

/* ---------- боковые панели: стеклянные кнопки ----------
   На саму панель с сайтом никаких эффектов: внутри живая страница. */
.panel-sidebar-panel:hover, .panel-sidebar-actions:hover { background-color: var(--lg-fill) !important; }
.panel-sidebar-panel[data-checked="true"] {
  background-color: var(--lg-fill-strong) !important;
  box-shadow: var(--lg-rim) !important;
}
#sidebar-main .tools-and-extensions moz-button, #sidebar-main button-group moz-button { border-radius: 14px !important; }

/* ---------- меню и панели: матовое стекло с кантом ---------- */
menupopup::part(content), panel::part(content) {
  background-color: var(--fm-menu) !important;
  background-image: var(--lg-sheen) !important;
  border: 0 !important;
  border-radius: 26px !important;
  box-shadow: var(--lg-rim), 0 0 0 .5px light-dark(rgb(0 0 0 / .08), rgb(0 0 0 / .6)) !important;
}
menupopup::part(content) { border-radius: 20px !important; }
menupopup > :is(menuitem, menu) { border-radius: 12px !important; }
menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]) {
  background-color: light-dark(rgb(0 0 0 / .06), rgb(255 255 255 / .12)) !important;
  color: var(--fm-ink) !important;
}
.subviewbutton:not([disabled]):hover,
#appMenu-mainView .subviewbutton:not([disabled]):hover {
  background: light-dark(rgb(0 0 0 / .05), rgb(255 255 255 / .1)) !important;
}
tooltip {
  background-color: var(--fm-menu) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim) !important;
  border: 0 !important;
}

/* главное меню: иконки — объёмные квадраты, как значки iOS 26 */
@TILES@
#appMenu-mainView .subviewbutton:is(@TILESEL@) > .toolbarbutton-icon {
  border-radius: 9px !important;
  width: 30px !important; height: 30px !important; padding: 7px !important;
  background: linear-gradient(180deg, color-mix(in srgb, var(--fm-tile) 78%, white), var(--fm-tile) 70%) !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .45), inset 0 -1px 0 rgb(0 0 0 / .12),
              0 2px 6px color-mix(in srgb, var(--fm-tile) 35%, transparent) !important;
}
#appMenu-mainView .subviewbutton { border-radius: 14px !important; min-height: 44px !important; }
#appMenu-mainView .subviewbutton > .toolbarbutton-text { font-weight: 500 !important; font-size: 14px !important; }

/* загрузки, расширения, разрешения */
#downloadsListBox > richlistitem[selected] { background: var(--lg-fill-strong) !important; box-shadow: var(--lg-rim) !important; }
.protections-popup-section, .identity-popup-section { background: var(--lg-fill) !important; box-shadow: var(--lg-rim) !important; }
moz-toggle { --toggle-background-color-pressed: #34C759 !important; }
button.primary, .popup-notification-primary-button {
  background: linear-gradient(180deg, color-mix(in srgb, var(--fm-accent) 80%, white), var(--fm-accent) 65%) !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .4) !important;
}

/* ---------- функции Floorp Modern ---------- */
.fm-toast {
  background-color: light-dark(rgb(255 255 255 / .72), rgb(40 40 46 / .6)) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim), var(--lg-drop) !important;
  backdrop-filter: blur(26px) saturate(190%) !important;
  border: 0 !important;
}
.fm-toast[data-kind="ok"] .fm-toast-dot { background: #30D158 !important; }
.fm-nowbar {
  background-color: light-dark(rgb(255 255 255 / .72), rgb(40 40 46 / .6)) !important;
  background-image: var(--lg-sheen) !important;
  box-shadow: var(--lg-rim), var(--lg-drop) !important;
  backdrop-filter: blur(26px) saturate(190%) !important;
  border: 0 !important;
}
.fm-progress-fill { background: linear-gradient(90deg, #0A84FF, #5E5CE6, #FF375F) !important; box-shadow: 0 0 10px rgb(10 132 255 / .7) !important; }
findbar { background: transparent !important; }
/* ---------- плашка доступа к экрану: стеклянная капсула ---------- */
@-moz-document url("chrome://browser/content/webrtcIndicator.xhtml") {
  body {
    background: light-dark(rgb(250 250 253 / .96), rgb(34 34 40 / .96)) !important;
    background-image: linear-gradient(180deg, light-dark(rgb(255 255 255 / .8), rgb(255 255 255 / .12)), transparent 60%) !important;
    border: 0 !important;
    box-shadow: inset 0 1px 0 light-dark(#fff, rgb(255 255 255 / .3)), inset 0 0 0 1px light-dark(rgb(0 0 0 / .08), rgb(255 255 255 / .08)) !important;
  }
  .stop-button {
    background: linear-gradient(180deg, #3D9BFF, #0A84FF 65%) !important;
    color: #fff !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .4) !important;
  }
}

"""

# ================================================================ страницы about:, настройки, новая вкладка
CONTENT_PREFIXES = '@-moz-document url-prefix("about:"), url-prefix("chrome://browser/content/"), url-prefix("chrome://mozapps/"), url-prefix("chrome://global/content/")'

CONTENT = r"""
/* ---------------- iOS 26 · Liquid Glass ---------------- */
@PREFIXES@ {
  :root {
@GLASS@
    --background-color-canvas: transparent !important;
    --background-color-box: var(--lg-fill) !important;
    --card-background-color: var(--lg-fill) !important;
    --in-content-page-background: transparent !important;
    --in-content-box-background: var(--lg-fill) !important;
    --color-accent-primary: var(--fm-accent) !important;
    --button-background-color-primary: var(--fm-accent) !important;
    --link-color: var(--fm-accent) !important;
    --focus-outline-color: var(--fm-accent) !important;
    --button-background-color: var(--lg-fill-strong) !important;
    --button-background-color-hover: light-dark(rgb(255 255 255 / .95), rgb(255 255 255 / .22)) !important;
    --input-text-background-color: var(--lg-fill-strong) !important;
    --select-background-color: var(--lg-fill-strong) !important;
    /* переключатели iPhone: зелёные */
    --toggle-background-color-pressed: #34C759 !important;
    --toggle-background-color-pressed-hover: #30B350 !important;
    --toggle-height: 24px !important;
    --toggle-width: 42px !important;
    --page-nav-button-background-color-selected: var(--lg-fill-strong) !important;
    --page-nav-button-text-color-selected: var(--fm-accent) !important;
    --card-border-radius: 26px !important;
    --box-border-radius: 26px !important;
  }
  /* обои — неподвижные, без анимации, чтобы страница не тормозила */
  :root:not(:has(#outerContainer #viewerContainer)) {
    background: var(--lg-wall) !important;
    background-attachment: fixed !important;
  }
  body { background: transparent !important; }

  /* группы настроек и карточки — стеклянные плитки */
  :is(setting-group, groupbox):not([hidden]), .card, .addon.card, moz-card {
    background-color: var(--lg-fill) !important;
    background-image: var(--lg-sheen) !important;
    box-shadow: var(--lg-rim), 0 6px 20px light-dark(rgb(40 50 90 / .08), rgb(0 0 0 / .25)) !important;
    border-radius: 26px !important;
    border: 0 !important;
  }
  .card:hover, .addon.card:hover { background-color: var(--lg-fill-strong) !important; }

  /* меню слева: выбранный пункт — стеклянная капля */
  .category[selected], .page-nav-button[selected], moz-page-nav-button[selected] {
    background: var(--lg-fill-strong) !important;
    color: var(--fm-accent) !important;
    box-shadow: var(--lg-rim) !important;
  }
  button.primary, moz-button[type="primary"]::part(button) {
    background-image: linear-gradient(180deg, rgb(255 255 255 / .22), transparent 65%) !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .35) !important;
  }
  input[type="search"], input[type="text"], select, menulist {
    box-shadow: var(--lg-rim) !important;
  }
}

/* ---------- настройки Floorp ---------- */
@-moz-document url-prefix("chrome://noraneko-settings/") {
  :root {
@GLASS@
  }
  :root, :root[data-theme], .floorp-standard-ui {
    --floorp-brand: #0A84FF !important;
    --floorp-brand-hover: #2A95FF !important;
    --floorp-action: #0A84FF !important;
    --floorp-focus: #0A84FF !important;
    --floorp-switch-on: #34C759 !important;
    --floorp-canvas: transparent !important;
    --floorp-surface: var(--lg-fill) !important;
    --floorp-subtle: var(--lg-fill) !important;
    --chakra-colors-purple-solid: #0A84FF !important;
    --chakra-colors-purple-fg: #0A84FF !important;
    --chakra-colors-purple-focus-ring: #0A84FF !important;
    --chakra-colors-purple-subtle: rgb(10 132 255 / .16) !important;
    --chakra-colors-bg-panel: var(--lg-fill) !important;
    --chakra-colors-bg-muted: var(--lg-fill) !important;
  }
  html {
    background: var(--lg-wall) !important;
    background-attachment: fixed !important;
  }
  body, #root { background: transparent !important; }
}

/* ---------- новая вкладка: экран блокировки iOS 26 ---------- */
@-moz-document url-prefix("chrome://noraneko-newtab/"), url("about:newtab"), url("about:home") {
  html { background: #050611 !important; }
  /* обои iOS 26: глубокий синий, фиолетовый и тёплый всполох. Неподвижные: стекло
     поверх движущегося фона пришлось бы перерисовывать каждый кадр */
  #root::before {
    animation: none !important;
    inset: 0 !important;
    background:
      radial-gradient(60% 55% at 18% 18%, rgb(64 156 255 / .95), transparent 62%),
      radial-gradient(55% 60% at 88% 12%, rgb(120 86 255 / .9), transparent 64%),
      radial-gradient(70% 55% at 75% 95%, rgb(255 92 140 / .75), transparent 62%),
      radial-gradient(45% 45% at 8% 92%, rgb(255 170 90 / .55), transparent 66%),
      radial-gradient(45% 40% at 50% 58%, rgb(70 80 220 / .55), transparent 70%),
      #070a24 !important;
  }
  #root::after { background: radial-gradient(130% 100% at 50% 35%, transparent 60%, rgb(0 0 0 / .45)) !important; }

  /* дата сверху, под ней огромные стеклянные часы */
  .absolute.top-4.right-4 > div > .flex { flex-direction: column-reverse !important; gap: 0 !important; }
  .absolute.top-4.right-4 .flex-col.text-right > div {
    font-size: 21px !important;
    font-weight: 600 !important;
    color: rgb(255 255 255 / .9) !important;
  }
  .absolute.top-4.right-4 .tabular-nums {
    font-size: clamp(96px, 13vw, 200px) !important;
    font-weight: 700 !important;
    letter-spacing: -0.035em !important;
    line-height: .92 !important;
    color: transparent !important;
    background: linear-gradient(180deg, rgb(255 255 255 / .97) 0%, rgb(255 255 255 / .78) 45%, rgb(225 232 255 / .55) 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-stroke: 1px rgb(255 255 255 / .35);
    text-shadow: none !important;
    filter: drop-shadow(0 2px 1px rgb(255 255 255 / .18)) drop-shadow(0 10px 30px rgb(10 20 80 / .45));
  }
  .absolute.top-4.right-4 .tabular-nums > .animate-pulse { animation: none !important; opacity: 1 !important; }

  /* поиск: настоящее жидкое стекло — размывает обои под собой */
  .group.cursor-pointer:has(input[readonly]) {
    min-height: 58px !important;
    border-radius: 999px !important;
    background-color: rgb(255 255 255 / .13) !important;
    background-image: linear-gradient(180deg, rgb(255 255 255 / .2), rgb(255 255 255 / 0) 60%) !important;
    border: 0 !important;
    backdrop-filter: blur(26px) saturate(190%) !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .55), inset 0 -1px 0 rgb(255 255 255 / .12),
                inset 1px 0 0 rgb(255 255 255 / .16), inset -1px 0 0 rgb(255 255 255 / .16),
                0 18px 50px rgb(5 10 40 / .35) !important;
  }
  .group.cursor-pointer:has(input[readonly]):hover {
    background-color: rgb(255 255 255 / .2) !important;
    transform: scale(1.015);
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .65), inset 0 -1px 0 rgb(255 255 255 / .16),
                inset 1px 0 0 rgb(255 255 255 / .2), inset -1px 0 0 rgb(255 255 255 / .2),
                0 22px 60px rgb(5 10 40 / .4) !important;
  }
  .group.cursor-pointer:has(input[readonly]) input::placeholder { color: rgb(255 255 255 / .78) !important; }
  .group.cursor-pointer:has(input[readonly]) :is(input, input:focus, input:hover) {
    appearance: none !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    border-radius: 0 !important;
    min-height: 0 !important;
    color: #fff !important;
  }

  /* док с ярлыками: стеклянная полка, иконки — квадраты iOS */
  .inline-block.backdrop-blur-sm.p-3 {
    border-radius: 34px !important;
    background-color: rgb(255 255 255 / .12) !important;
    background-image: linear-gradient(180deg, rgb(255 255 255 / .18), rgb(255 255 255 / 0) 55%) !important;
    border: 0 !important;
    backdrop-filter: blur(26px) saturate(190%) !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .5), inset 0 -1px 0 rgb(255 255 255 / .1),
                inset 1px 0 0 rgb(255 255 255 / .14), inset -1px 0 0 rgb(255 255 255 / .14),
                0 20px 50px rgb(5 10 40 / .3) !important;
  }
  a.group .overflow-hidden.bg-gray-700 {
    border-radius: 14px !important;
    background: linear-gradient(180deg, #ffffff, #e9ecf5) !important;
    box-shadow: inset 0 1px 0 #fff, 0 6px 16px rgb(0 0 0 / .28) !important;
  }
  a.group.flex.flex-col.items-center:hover { background: rgb(255 255 255 / .12) !important; }
  html body button.fixed.bottom-4.right-4,
  html body button.fixed.bottom-4.right-4:hover {
    background: rgb(255 255 255 / .14) !important;
    appearance: none !important;
    color: #fff !important;
    border-radius: 999px !important;
    width: 44px !important; height: 44px !important;
    min-height: 0 !important; padding: 0 !important;
    display: grid !important; place-items: center !important;
    backdrop-filter: blur(20px) saturate(190%) !important;
    border: 0 !important;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / .5), 0 8px 24px rgb(0 0 0 / .3) !important;
  }
  html body button.fixed.bottom-4.right-4:hover { background: rgb(255 255 255 / .24) !important; }
  html body button.fixed.bottom-4.right-4 svg { color: #fff !important; stroke: currentColor; opacity: .95; }
}
/* ---------- скриншот страницы: стеклянная панель, как в iOS ---------- */
#screenshots-component { --fm-shot-accent: #0A84FF; }
#screenshots-component #buttons-container,
#screenshots-component #selection-size {
  background: rgb(40 40 46 / .55) !important;
  background-image: linear-gradient(180deg, rgb(255 255 255 / .16), transparent 60%) !important;
  backdrop-filter: blur(24px) saturate(190%) !important;
  border: 0 !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .35), inset 0 0 0 1px rgb(255 255 255 / .08), 0 14px 40px rgb(0 0 0 / .4) !important;
}
#screenshots-component .screenshots-button { background: rgb(255 255 255 / .1) !important; }
#screenshots-component #download {
  background: linear-gradient(180deg, #3D9BFF, #0A84FF 65%) !important;
  color: #fff !important;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .4) !important;
}
#screenshots-component .highlight { border-radius: 14px !important; }
#screenshots-component .mover { box-shadow: 0 0 0 2px #0A84FF, 0 2px 8px rgb(0 0 0 / .45) !important; }

"""

# ================================================================ просмотрщик PDF
PDF = r"""
/* ---------------- iOS 26 · Liquid Glass ---------------- */
:root:has(#outerContainer #viewerContainer) {
  & {
    --x-accent: light-dark(var(--fm-user-accent, #007AFF), var(--fm-user-accent, #0A84FF)) !important;
    --x-on-accent: #ffffff !important;
    --x-ground: light-dark(#ECEFF6, #07080E) !important;
    --x-bar: transparent !important;
    --x-well: light-dark(rgb(255 255 255 / .66), rgb(36 36 44 / .68)) !important;
    --x-field: light-dark(rgb(255 255 255 / .8), rgb(255 255 255 / .1)) !important;
    --x-rim: inset 0 1px 0 light-dark(#fff, rgb(255 255 255 / .32)),
             inset 0 -1px 0 light-dark(rgb(255 255 255 / .5), rgb(255 255 255 / .07)),
             inset 1px 0 0 light-dark(rgb(255 255 255 / .55), rgb(255 255 255 / .08)),
             inset -1px 0 0 light-dark(rgb(255 255 255 / .55), rgb(255 255 255 / .08));
    --x-sheen: linear-gradient(180deg, light-dark(rgb(255 255 255 / .6), rgb(255 255 255 / .12)), transparent 60%);
  }
  /* страницы уходят под панель, а панель — стеклянные капсулы поверх них */
  & #viewerContainer {
    inset-block-start: 0 !important;
    background:
      radial-gradient(60% 50% at 0% 0%, light-dark(rgb(122 170 255 / .35), rgb(10 132 255 / .16)), transparent 70%),
      radial-gradient(50% 50% at 100% 100%, light-dark(rgb(255 172 200 / .3), rgb(255 55 95 / .1)), transparent 70%),
      var(--x-ground) !important;
    background-attachment: local, local, scroll !important;
  }
  & .pdfViewer { padding-block-start: 68px !important; }
  & #loadingBar { border-bottom: 0 !important; background-color: transparent !important; }
  & #toolbarContainer {
    position: relative !important;
    z-index: 30 !important;
    background: transparent !important;
    border-bottom: 0 !important;
  }
  & #toolbarViewerLeft,
  & #toolbarViewerMiddle,
  & #editorModeButtons,
  & #toolbarViewerRight > .toolbarHorizontalGroup:not(#editorModeButtons) {
    background-color: var(--x-well) !important;
    background-image: var(--x-sheen) !important;
    border: 0 !important;
    box-shadow: var(--x-rim), 0 6px 18px light-dark(rgb(40 50 90 / .14), rgb(0 0 0 / .4)) !important;
    backdrop-filter: blur(18px) saturate(190%) !important;
  }
  & :is(.doorHanger, .doorHangerRight, #findbar, #secondaryToolbar, .editorParamsToolbar:not(#editorCommentParamsToolbar), .popupMenu, #xThemeMenu, #xColorPop, #xNotice, #xBookMenu) {
    background-color: light-dark(rgb(250 250 253 / .78), rgb(34 34 40 / .7)) !important;
    background-image: var(--x-sheen) !important;
    border: 0 !important;
    box-shadow: var(--x-rim), 0 20px 50px light-dark(rgb(40 50 90 / .2), rgb(0 0 0 / .55)) !important;
    backdrop-filter: blur(28px) saturate(190%) !important;
  }
}
"""


def build(t):
    return (t.replace("@GLASS@", GLASS_TOKENS)
             .replace("@TILES@", TILE_RULES)
             .replace("@TILESEL@", TILE_SEL)
             .replace("@PREFIXES@", CONTENT_PREFIXES))


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, text in (("ios-chrome.css", CHROME), ("ios-content.css", CONTENT), ("ios-pdf.css", PDF)):
        css = build(text)
        assert css.count("{") == css.count("}"), name
        (out / name).write_text(css, encoding="utf-8")
    print("ok")
