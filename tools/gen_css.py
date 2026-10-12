#!/usr/bin/env python3
"""Generates the PDF viewer theme block for Floorp's userContent.css."""

def svg(body, fill=False):
    attrs = ("fill='black'" if fill else
             "fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'")
    return ("url(\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' "
            + attrs + ">" + body + "</svg>\")")

P = lambda d: f"<path d='{d}'/>"

ICONS = {
    # main toolbar
    "--toolbarButton-viewsManagerToggle-icon": svg("<rect x='3' y='4' width='18' height='16' rx='3'/>" + P("M9.5 4v16")),
    "--toolbarButton-search-icon": svg("<circle cx='11' cy='11' r='6.5'/>" + P("M20 20l-4.2-4.2")),
    "--toolbarButton-pageUp-icon": svg(P("M6 15l6-6 6 6")),
    "--toolbarButton-pageDown-icon": svg(P("M6 9l6 6 6-6")),
    "--toolbarButton-zoomOut-icon": svg(P("M5 12h14")),
    "--toolbarButton-zoomIn-icon": svg(P("M12 5v14M5 12h14")),
    "--toolbarButton-editorComment-icon": svg(P("M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-6 4z")),
    "--toolbarButton-editorSignature-icon": svg(P("M3 16c2.5 0 3.5-8 6-8s1 7.5 3 7.5 2-3.5 4-3.5 2 2 5 2") + P("M3 20.5h18")),
    "--toolbarButton-editorHighlight-icon": svg(P("M9.5 10.5l5-5.5 4.5 4.5-5.5 5z") + P("M9.5 10.5L6 14l4 4 3.5-3.5") + P("M6 14l-2 4h4") + P("M14 20.5h7")),
    "--toolbarButton-editorFreeText-icon": svg(P("M5 7V4.5h14V7") + P("M12 4.5v15") + P("M9 19.5h6")),
    "--toolbarButton-editorInk-icon": svg(P("M4 20l1.2-4.4L15.8 5a2.2 2.2 0 0 1 3.2 3.2L8.4 18.8z") + P("M13.8 7l3.2 3.2")),
    "--toolbarButton-editorStamp-icon": svg("<rect x='3' y='4.5' width='18' height='15' rx='3'/><circle cx='9' cy='10' r='1.8'/>" + P("M21 16l-4.5-4.5L7 19.5")),
    "--toolbarButton-print-icon": svg(P("M7 9V3.5h10V9") + "<rect x='3.5' y='9' width='17' height='8' rx='2.5'/>" + P("M7 14h10v6.5H7z")),
    "--toolbarButton-download-icon": svg(P("M12 3.5v11") + P("M7 10l5 5 5-5") + P("M4.5 20h15")),
    "--toolbarButton-secondaryToolbarToggle-icon": svg("<circle cx='5.5' cy='12' r='1.7'/><circle cx='12' cy='12' r='1.7'/><circle cx='18.5' cy='12' r='1.7'/>", fill=True),
    "--toolbarButton-menuArrow-icon": svg(P("M7 10l5 5 5-5")),
    "--toolbarButton-presentationMode-icon": svg("<rect x='3' y='4' width='18' height='12' rx='2.5'/>" + P("M12 16v4.5M8 20.5h8")),
    "--toolbarButton-bookmark-icon": svg(P("M7 3.5h10v17l-5-4-5 4z")),
    "--toolbarButton-viewThumbnail-icon": svg("<rect x='4' y='3.5' width='7' height='9' rx='1.5'/><rect x='13' y='3.5' width='7' height='9' rx='1.5'/><rect x='4' y='14.5' width='7' height='6' rx='1.5'/><rect x='13' y='14.5' width='7' height='6' rx='1.5'/>"),
    "--toolbarButton-viewOutline-icon": svg(P("M9 6h11M9 12h11M9 18h11") + "<circle cx='4.5' cy='6' r='.8'/><circle cx='4.5' cy='12' r='.8'/><circle cx='4.5' cy='18' r='.8'/>"),
    "--toolbarButton-viewAttachments-icon": svg(P("M20 11.5l-8 8a5 5 0 0 1-7-7l8.5-8.5a3.3 3.3 0 0 1 4.7 4.7L9.7 17a1.7 1.7 0 0 1-2.4-2.4L15 7")),
    "--findbarButton-previous-icon": svg(P("M6 15l6-6 6 6")),
    "--findbarButton-next-icon": svg(P("M6 9l6 6 6-6")),
    # secondary menu
    "--secondaryToolbarButton-firstPage-icon": svg(P("M6 5v14") + P("M18 6l-7 6 7 6")),
    "--secondaryToolbarButton-lastPage-icon": svg(P("M18 5v14") + P("M6 6l7 6-7 6")),
    "--secondaryToolbarButton-rotateCw-icon": svg(P("M19.5 12a7.5 7.5 0 1 1-2.2-5.3") + P("M19.5 4v5h-5")),
    "--secondaryToolbarButton-rotateCcw-icon": svg(P("M4.5 12a7.5 7.5 0 1 0 2.2-5.3") + P("M4.5 4v5h5")),
    "--secondaryToolbarButton-selectTool-icon": svg(P("M5 3.5l13.5 7-6 1.8-2.2 6.2z")),
    "--secondaryToolbarButton-handTool-icon": svg(P("M8 12V6a1.5 1.5 0 0 1 3 0v5M11 11V4.5a1.5 1.5 0 0 1 3 0V11M14 11V6a1.5 1.5 0 0 1 3 0v6c0 5-2.5 8.5-6.5 8.5-3 0-4.5-2-6-5l-1.2-2.4a1.4 1.4 0 0 1 2.4-1.4L8 13.5")),
    "--secondaryToolbarButton-scrollVertical-icon": svg("<rect x='6' y='3' width='12' height='8' rx='1.5'/><rect x='6' y='13' width='12' height='8' rx='1.5'/>"),
    "--secondaryToolbarButton-scrollHorizontal-icon": svg("<rect x='3' y='6' width='8' height='12' rx='1.5'/><rect x='13' y='6' width='8' height='12' rx='1.5'/>"),
    "--secondaryToolbarButton-scrollWrapped-icon": svg("<rect x='3.5' y='3.5' width='7' height='7' rx='1.5'/><rect x='13.5' y='3.5' width='7' height='7' rx='1.5'/><rect x='3.5' y='13.5' width='7' height='7' rx='1.5'/>"),
    "--secondaryToolbarButton-scrollPage-icon": svg("<rect x='6' y='3' width='12' height='18' rx='2'/>"),
    "--secondaryToolbarButton-spreadNone-icon": svg("<rect x='7' y='4' width='10' height='16' rx='1.5'/>"),
    "--secondaryToolbarButton-spreadOdd-icon": svg("<rect x='2.5' y='5' width='8.5' height='14' rx='1.5'/><rect x='13' y='5' width='8.5' height='14' rx='1.5'/>" + P("M6.75 10v4")),
    "--secondaryToolbarButton-spreadEven-icon": svg("<rect x='2.5' y='5' width='8.5' height='14' rx='1.5'/><rect x='13' y='5' width='8.5' height='14' rx='1.5'/>" + P("M15.5 10.5h3.5M15.5 13.5h3.5")),
    "--secondaryToolbarButton-documentProperties-icon": svg("<circle cx='12' cy='12' r='8.5'/>" + P("M12 11v5.5") + "<circle cx='12' cy='7.8' r='.6'/>"),
    # our theme button
    "--x-theme-auto-icon": svg("<circle cx='12' cy='12' r='8'/>" + P("M12 4a8 8 0 0 1 0 16z").replace("/>", " fill='black'/>")),
    "--x-theme-light-icon": svg("<circle cx='12' cy='12' r='4'/>" + P("M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4")),
    "--x-theme-dark-icon": svg(P("M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z")),
    # закладки страниц
    "--x-bookmark-icon": svg(P("M7 3.5h10a1 1 0 0 1 1 1v16l-6-4-6 4v-16a1 1 0 0 1 1-1z")),
    "--x-bookmark-on-icon": svg(P("M7 3.5h10a1 1 0 0 1 1 1v16l-6-4-6 4v-16a1 1 0 0 1 1-1z").replace("/>", " fill='black'/>")),
}

icon_vars = "\n".join(f"    {k}: {v} !important;" for k, v in ICONS.items())

CSS = r"""
/* ======================= PDF-TWEAKS BEGIN ======================= */
/* Новый вид встроенного просмотрщика PDF (Floorp).
   Этот блок ставит и убирает установщик «Floorp PDF». Правки внутри
   блока пропадут при переустановке. */

/* срабатывает только в просмотрщике PDF (любой адрес, в т.ч. file:///) */
:root:has(#outerContainer #viewerContainer) {

  /* ---------- НАСТРОЙКИ: меняйте тут ---------- */
  & {
    /* Цвет акцента (активный инструмент, выделение, текущая страница) */
    --x-accent: light-dark(AccentColor, color-mix(in srgb, AccentColor 62%, white)) !important;
    --x-on-accent: light-dark(AccentColorText, color-mix(in srgb, AccentColor 22%, black)) !important;
    /* Скругление страниц и отступ между ними */
    --x-radius: 10px;
    --x-gap: 18px;
  }
  /* -------------------------------------------- */

  & {
    --x-ground:  light-dark(#f2f3f5, #000000);
    --x-bar:     light-dark(#ffffff, #17181a);
    --x-well:    light-dark(#eef0f3, #242528);
    --x-rail:    light-dark(#f2f3f5, #000000);
    --x-line:    light-dark(rgb(0 0 0 / .08), rgb(255 255 255 / .08));
    --x-ink:     light-dark(#111214, #f2f2f3);
    --x-muted:   light-dark(#6b6f76, #9a9da3);
    --x-field:   light-dark(#ffffff, #2a2b2e);
    --x-hover:   light-dark(rgb(28 33 48 / .08), rgb(228 231 239 / .09));
    --x-press:   light-dark(rgb(28 33 48 / .14), rgb(228 231 239 / .15));
    --x-soft:    color-mix(in srgb, var(--x-accent) 16%, transparent);
    --x-shadow:  0 1px 2px light-dark(rgb(20 30 60 / .12), rgb(0 0 0 / .5)),
                 0 7px 26px light-dark(rgb(20 30 60 / .10), rgb(0 0 0 / .35));
    --x-pop:     0 2px 4px light-dark(rgb(20 30 60 / .10), rgb(0 0 0 / .4)),
                 0 14px 40px light-dark(rgb(20 30 60 / .16), rgb(0 0 0 / .5));

    /* тон страниц: без скрипта — «ночь» в тёмной теме;
       со скриптом управляется кнопкой темы (атрибут data-x-page) */
    --x-page-filter: none;

    --toolbar-height: 52px !important;
    --toolbar-vertical-padding: 6px !important;
    --toolbar-horizontal-padding: 10px !important;
    --icon-size: 18px !important;

    --main-color: var(--x-ink) !important;
    --text-color: var(--x-ink) !important;
    --body-bg-color: var(--x-ground) !important;
    --toolbar-bg-color: var(--x-bar) !important;
    --toolbar-border-color: var(--x-line) !important;
    --toolbar-border-bottom: 1px solid var(--x-line) !important;
    --toolbar-box-shadow: none !important;
    --toolbarSidebar-box-shadow: none !important;
    --toolbarSidebar-border-bottom: 1px solid var(--x-line) !important;
    --sidebar-toolbar-bg-color: var(--x-rail) !important;
    --sidebar-narrow-bg-color: var(--x-rail) !important;
    --toolbar-icon-bg-color: var(--x-ink) !important;
    --toolbar-icon-hover-bg-color: var(--x-ink) !important;
    --toolbar-icon-opacity: .9 !important;
    --doorhanger-icon-opacity: .9 !important;
    --button-hover-color: var(--x-hover) !important;
    --toggled-btn-color: var(--x-on-accent) !important;
    --toggled-btn-bg-color: var(--x-accent) !important;
    --toggled-hover-active-btn-color: var(--x-accent) !important;
    --toggled-hover-btn-outline: none !important;
    --field-color: var(--x-ink) !important;
    --field-bg-color: var(--x-field) !important;
    --field-border-color: var(--x-line) !important;
    --toolbar-field-color: var(--x-ink) !important;
    --toolbar-field-bg-color: var(--x-field) !important;
    --toolbar-field-border-color: var(--x-line) !important;
    --dropdown-btn-bg-color: transparent !important;
    --dropdown-btn-border: none !important;
    --separator-color: var(--x-line) !important;
    --doorhanger-bg-color: var(--x-bar) !important;
    --doorhanger-border-color: var(--x-line) !important;
    --doorhanger-hover-color: var(--x-ink) !important;
    --doorhanger-hover-bg-color: var(--x-hover) !important;
    --doorhanger-separator-color: var(--x-line) !important;
    --treeitem-color: var(--x-ink) !important;
    --treeitem-hover-color: var(--x-ink) !important;
    --treeitem-bg-color: var(--x-hover) !important;
    --treeitem-selected-color: var(--x-accent) !important;
    --treeitem-selected-bg-color: var(--x-soft) !important;
    --thumbnail-hover-color: var(--x-hover) !important;
    --thumbnail-selected-color: var(--x-soft) !important;
    --image-outline: none !important;
    --image-shadow: var(--x-shadow) !important;
    --image-current-border-color: var(--x-accent) !important;
    --image-page-number-bg: var(--x-bar) !important;
    --image-page-number-fg: var(--x-muted) !important;
    --image-page-number-border-color: var(--x-line) !important;
    --image-current-page-number-bg: var(--x-accent) !important;
    --image-current-page-number-fg: var(--x-on-accent) !important;
    --indicator-color: var(--x-accent) !important;
    --progressBar-color: var(--x-accent) !important;
    --progressBar-bg-color: transparent !important;
    --scrollbar-color: var(--x-line) !important;
    --scrollbar-bg-color: transparent !important;
    --dialog-button-bg-color: var(--x-field) !important;
    --dialog-button-hover-bg-color: var(--x-hover) !important;
    --highlight-bg-color: rgb(255 176 32 / .45) !important;
    --highlight-selected-bg-color: rgb(255 120 0 / .6) !important;
    --page-border: 0 !important;
    --page-margin: 0 auto var(--x-gap) !important;
    --spreadHorizontalWrapped-margin-LR: 0 !important;

    /* иконки */
@ICONS@
  }

  @media (prefers-color-scheme: dark) {
    &:not([data-x-page]) { --x-page-filter: invert(.88) hue-rotate(180deg) contrast(.9); --x-page-bg: #25262a; }
  }
  &[data-x-page="sepia"] { --x-page-filter: sepia(.45) brightness(.96) contrast(.95); --x-page-bg: #f4eddc; }
  &[data-x-page="night"] { --x-page-filter: invert(.88) hue-rotate(180deg) contrast(.9); --x-page-bg: #25262a; }

  &, & body, & button, & input, & select, & menu {
    font-family: "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;
  }

  /* ================= ПАНЕЛЬ ИНСТРУМЕНТОВ ================= */
  & #toolbarContainer {
    background: var(--x-bar) !important;
    border-bottom: 1px solid var(--x-line) !important;
    box-shadow: none !important;
  }
  & #toolbarViewer { gap: 10px !important; }
  & #toolbarViewerLeft { margin-inline-start: 0 !important; }
  & #toolbarViewerLeft, & #toolbarViewerMiddle, & #toolbarViewerRight { gap: 8px !important; }

  /* «таблетки» — группы кнопок */
  & #toolbarViewerLeft,
  & #toolbarViewerMiddle,
  & #editorModeButtons,
  & #toolbarViewerRight > .toolbarHorizontalGroup:not(#editorModeButtons) {
    background: var(--x-well) !important;
    border: 1px solid var(--x-line) !important;
    border-radius: 999px !important;
    box-shadow: inset 0 1px 0 light-dark(rgb(255 255 255 / .9), rgb(255 255 255 / .06)), 0 1px 3px light-dark(rgb(0 0 0 / .06), rgb(0 0 0 / .5)) !important;
    padding: 0 3px !important;
    gap: 2px !important;
    height: 40px !important;
    width: auto !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    flex: none !important;
  }
  & #toolbarViewerRight {
    background: none !important; border: 0 !important; padding: 0 !important;
    display: flex !important; align-items: center !important; gap: 10px !important;
  }
  & #toolbarViewer { align-items: center !important; }
  & .toolbarButtonSpacer { width: 4px !important; }
  & :is(.verticalToolbarSeparator, .splitToolbarButtonSeparator, #editorModeSeparator) {
    display: none !important;
  }

  /* кнопки */
  /* фиксированные размеры: в Firefox проценты высоты у вложенных
     контейнеров не срабатывают, и кнопки вылезали за свои группы */
  & #toolbarViewer :is(.toolbarHorizontalGroup, .toolbarButtonWithContainer) {
    flex: none !important;
    margin: 0 !important;
    min-width: 0 !important;
  }
  & #toolbarViewer .toolbarButtonWithContainer:not([hidden], #editorComment) {
    height: auto !important;
    display: flex !important;
    align-items: center !important;
  }
  & .toolbarButton:not(.labeled):not(:is(.doorHanger, .doorHangerRight, .menu) *) {
    width: 32px !important;
    min-width: 32px !important;
    height: 32px !important;
    aspect-ratio: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    flex: none !important;
    border-radius: 999px !important;
    transition: background-color .12s ease, transform .08s ease !important;
  }
  & .toolbarButton:hover { background-color: var(--x-hover) !important; }
  & .toolbarButton:active { background-color: var(--x-press) !important; transform: scale(.94); }
  & .toolbarButton:focus-visible { outline: 2px solid var(--x-accent) !important; outline-offset: -2px !important; }
  & .toolbarButton:is(.toggled, [aria-pressed="true"]) {
    background-color: var(--x-accent) !important;
    box-shadow: 0 1px 3px color-mix(in srgb, var(--x-accent) 45%, transparent) !important;
  }
  & .toolbarButton:is(.toggled, [aria-pressed="true"])::before { background-color: var(--x-on-accent) !important; }
  & .toolbarButton[aria-expanded="true"]:not(.toggled) { background-color: var(--x-soft) !important; }
  & .toolbarButton[aria-expanded="true"]:not(.toggled)::before { background-color: var(--x-accent) !important; }
  & .toolbarButton:disabled { opacity: .35 !important; background: none !important; transform: none !important; }

  /* номер страницы и масштаб */
  & #pageNumber {
    width: 44px !important;
    height: 30px !important;
    box-sizing: border-box !important;
    text-align: center !important;
    border-radius: 8px !important;
    border: 1px solid var(--x-line) !important;
    background: var(--x-field) !important;
    color: var(--x-ink) !important;
    font-variant-numeric: tabular-nums !important;
    font-weight: 600 !important;
    border-radius: 999px !important;
  }
  & #numPages { color: var(--x-muted) !important; font-variant-numeric: tabular-nums !important; padding-inline: 4px 8px !important; }
  & #scaleSelectContainer { height: 32px !important; border-radius: 999px !important; display: flex !important; align-items: center !important; }
  & #scaleSelectContainer:hover { background: var(--x-hover) !important; }
  & #scaleSelect {
    height: 32px !important;
    border: 0 !important;
    background-color: transparent !important;
    color: var(--x-ink) !important;
    font-weight: 500 !important;
    border-radius: 999px !important;
    padding-inline: 10px 26px !important;
  }
  & :is(.toolbarField, #findInput, #scaleSelect, #pageNumber):focus {
    outline: 2px solid var(--x-accent) !important;
    outline-offset: -2px !important;
  }

  /* ================= ВСПЛЫВАЮЩИЕ ПАНЕЛИ ================= */
  & :is(.doorHanger, .doorHangerRight, #findbar, #secondaryToolbar, .editorParamsToolbar:not(#editorCommentParamsToolbar), .popupMenu, #xThemeMenu, #xBookMenu) {
    background: var(--x-bar) !important;
    border: 1px solid var(--x-line) !important;
    border-radius: 24px !important;
    box-shadow: var(--x-pop) !important;
  }
  & :is(.doorHanger, .doorHangerRight)::before,
  & :is(.doorHanger, .doorHangerRight)::after { display: none !important; }
  & :is(#secondaryToolbar, .popupMenu) { padding: 6px !important; }
  & :is(#secondaryToolbarButtonContainer, .popupMenu) :is(button, .toolbarButton) {
    border-radius: 14px !important;
    min-height: 36px !important;
  }
  & :is(#secondaryToolbarButtonContainer, .popupMenu) :is(button, .toolbarButton):hover {
    background: var(--x-hover) !important;
  }
  & #findbar { padding: 6px !important; gap: 6px !important; }
  & #findInput {
    border-radius: 999px !important;
    border: 1px solid var(--x-line) !important;
    background: var(--x-field) !important;
    padding-inline: 10px !important;
  }
  & .toggleButton.toolbarLabel { border-radius: 999px !important; }
  & .toggleButton.toolbarLabel:hover { background: var(--x-hover) !important; }
  & #findResultsCount, & #findMsg { color: var(--x-muted) !important; }

  /* панель параметров рисования (цвет / толщина / прозрачность) */
  & .editorParamsToolbar:not(#editorCommentParamsToolbar) { padding: 10px !important; }
  & .editorParamsToolbar input[type="range"] { accent-color: var(--x-accent) !important; }
  & .editorParamsToolbar input[type="color"] {
    border-radius: 8px !important; border: 1px solid var(--x-line) !important;
    background: var(--x-field) !important; overflow: hidden !important;
  }
  & .editorParamsLabel { color: var(--x-muted) !important; }

  /* плавающая панель у выделенной аннотации */
  & .editToolbar {
    background: var(--x-bar) !important;
    border: 1px solid var(--x-line) !important;
    border-radius: 999px !important;
    box-shadow: var(--x-pop) !important;
    padding: 3px !important;
  }
  & .editToolbar button { border-radius: 999px !important; }
  & .editToolbar button:hover { background: var(--x-hover) !important; }

  /* диалоги */
  & dialog {
    border-radius: 26px !important;
    border: 1px solid var(--x-line) !important;
    background: var(--x-bar) !important;
    color: var(--x-ink) !important;
    box-shadow: var(--x-pop) !important;
  }
  & dialog button { border-radius: 999px !important; }
  & dialog button.primaryButton, & dialog #primaryButton {
    background: var(--x-accent) !important; color: var(--x-on-accent) !important; border-color: transparent !important;
  }

  /* ================= БОКОВАЯ ПАНЕЛЬ ================= */
  & #viewsManager {
    background: var(--x-rail) !important;
    border-inline-end: 1px solid var(--x-line) !important;
    box-shadow: none !important;
  }
  & .thumbnailImageContainer {
    border-radius: 4px !important;
    overflow: hidden !important;
  }
  & .thumbnailImageContainer img { filter: var(--x-page-filter) !important; }
  & .thumbnail:has([aria-current="page"]) > .thumbnailImageContainer {
    outline: 2px solid var(--x-accent) !important;
    outline-offset: 3px !important;
  }
  & .treeItem > a { border-radius: 6px !important; }

  /* ================= СТРАНИЦЫ ================= */
  & #viewerContainer { background: var(--x-ground) !important; }
  & .pdfViewer { padding-block: 24px 48px !important; }
  & .pdfViewer .page {
    border: 0 !important;
    border-image: none !important;
    border-radius: var(--x-radius) !important;
    box-shadow: var(--x-shadow) !important;
    overflow: hidden !important;
    /* фон страницы того же цвета, что и сама страница после фильтра:
       пока страница рисуется, нет белых уголков и белых вспышек */
    background-color: var(--x-page-bg, #ffffff) !important;
  }
  & .pdfViewer .page .canvasWrapper { border-radius: inherit !important; overflow: hidden !important; }
  & .pdfViewer .page .canvasWrapper { filter: var(--x-page-filter) !important; }
  & .pdfViewer:is(.scrollHorizontal, .scrollWrapped) .page,
  & .pdfViewer .spread .page { margin: 0 calc(var(--x-gap) / 2) var(--x-gap) !important; }

  & .textLayer ::selection { background: color-mix(in srgb, var(--x-accent) 35%, transparent) !important; }
  & .textLayer .highlight { border-radius: 3px !important; }

  /* рисунки: никакой рамки. Схватить рисунок можно только за сами линии
     (скрипт помечает рисунок под курсором классом x-hot), пустое место
     вокруг не выделяется и по нему можно рисовать. */
  & .annotationEditorLayer .inkEditor {
    pointer-events: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
  }
  & .annotationEditorLayer .inkEditor::before { display: none !important; }
  & .annotationEditorLayer .inkEditor > .resizers { display: none !important; }
  & [hidden] { display: none !important; }
  & .annotationEditorLayer .inkEditor.x-hot {
    pointer-events: auto !important;
    cursor: move !important;
  }
  & .annotationEditorLayer .inkEditor.x-hot:not(.selectedEditor) { cursor: pointer !important; }
  & .canvasWrapper svg.draw.x-hover {
    filter: drop-shadow(0 0 1.5px var(--x-accent)) drop-shadow(0 0 1.5px var(--x-accent));
  }
  & .canvasWrapper svg.draw.x-sel {
    filter: drop-shadow(0 0 1px var(--x-accent)) drop-shadow(0 0 3px var(--x-accent));
  }

  /* выделенная аннотация (текст, картинка, подпись) */
  & .annotationEditorLayer :is(.freeTextEditor, .stampEditor, .signatureEditor).selectedEditor {
    outline: 2px solid var(--x-accent) !important;
    outline-offset: 2px !important;
    border-radius: 4px !important;
  }

  /* ================= КНОПКА ТЕМЫ ================= */
  & #xThemeButton::before { mask-image: var(--x-theme-auto-icon) !important; }
  &[data-x-ui="light"] #xThemeButton::before { mask-image: var(--x-theme-light-icon) !important; }
  &[data-x-ui="dark"] #xThemeButton::before { mask-image: var(--x-theme-dark-icon) !important; }
  & #xThemeWrap { position: relative; display: flex; align-items: center; }

  /* ================= ЗАКЛАДКИ СТРАНИЦ ================= */
  & #xBookButton::before { mask-image: var(--x-bookmark-icon) !important; }
  & #xBookButton[data-on]::before { mask-image: var(--x-bookmark-on-icon) !important; background-color: var(--x-accent) !important; }
  & #xBookWrap { position: relative; display: flex; align-items: center; }
  & #xBookMenu {
    position: absolute !important; top: calc(100% + 10px) !important; inset-inline-end: -4px !important; z-index: 30000 !important;
    width: 300px !important; max-width: calc(100vw - 16px) !important; box-sizing: border-box !important;
    max-height: min(70vh, 520px) !important; overflow: hidden auto !important; padding: 8px !important;
    display: flex !important; flex-direction: column !important; gap: 2px !important;
    color: var(--x-ink) !important; font: 500 13px "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;
    white-space: normal !important;
  }
  & #xBookMenu[hidden] { display: none !important; }
  & #xBookMenu [role="button"] { cursor: pointer !important; user-select: none !important; outline: none !important; }
  & #xBookMenu [role="button"]:focus-visible { box-shadow: 0 0 0 2px var(--x-accent) !important; }
  & #xBookMenu .x-head {
    display: flex !important; align-items: center !important; justify-content: space-between !important;
    gap: 8px !important; padding: 4px 4px 8px 10px !important; min-width: 0 !important;
  }
  & #xBookMenu .x-title { font-weight: 700 !important; font-size: 15px !important; flex: 1 1 auto !important; }
  & #xBookMenu .x-add {
    flex: none !important; padding: 6px 12px !important; border-radius: 999px !important;
    background: var(--x-accent) !important; color: var(--x-on-accent) !important;
    font-weight: 600 !important; white-space: nowrap !important;
  }
  & #xBookMenu .x-add:hover { filter: brightness(1.08); }
  & #xBookMenu .x-add[data-on] { background: var(--x-hover) !important; color: var(--x-ink) !important; }
  & #xBookMenu .x-item {
    display: flex !important; align-items: center !important; gap: 6px !important; min-width: 0 !important;
    border-radius: 12px !important; padding: 4px 4px 4px 8px !important;
  }
  & #xBookMenu .x-item:hover { background: var(--x-hover) !important; }
  & #xBookMenu .x-item[data-current] { background: var(--x-soft) !important; }
  & #xBookMenu .x-go {
    flex: 1 1 auto !important; min-width: 0 !important; overflow: hidden !important;
    display: flex !important; align-items: center !important; gap: 10px !important; padding: 4px 0 !important;
  }
  & #xBookMenu .x-num {
    flex: none !important; min-width: 34px !important; height: 26px !important; padding: 0 6px !important; box-sizing: border-box !important;
    display: grid !important; place-items: center !important; border-radius: 8px !important;
    background: var(--x-accent) !important; color: var(--x-on-accent) !important; font-weight: 700 !important; font-size: 12px !important;
  }
  & #xBookMenu .x-note {
    flex: 1 1 auto !important; min-width: 0 !important;
    overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; color: var(--x-muted) !important;
  }
  & #xBookMenu .x-del {
    flex: none !important; width: 28px !important; height: 28px !important; border-radius: 50% !important;
    display: grid !important; place-items: center !important; color: var(--x-muted) !important; font-size: 17px !important; line-height: 1 !important;
  }
  & #xBookMenu .x-del:hover { background: var(--x-press) !important; color: var(--x-ink) !important; }
  & #xBookMenu .x-empty { padding: 10px 10px 12px !important; color: var(--x-muted) !important; line-height: 1.45 !important; }
  /* ленточка на странице с закладкой */
  /* ::after у страницы занят значком загрузки PDF.js, поэтому ленточка — на ::before */
  & .pdfViewer .page.x-bookmarked::before {
    content: "" !important; display: block !important; position: absolute !important; top: -3px; inset-inline-end: 28px; z-index: 6 !important;
    width: 18px; height: 30px; background: var(--x-accent);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 74%, 0 100%);
    filter: drop-shadow(0 2px 3px rgb(0 0 0 / .3)); pointer-events: none;
  }
  & #xThemeMenu {
    position: absolute; top: calc(100% + 10px); inset-inline-end: -4px; z-index: 30000;
    min-width: 210px; padding: 8px; display: grid; gap: 4px;
    color: var(--x-ink); font-size: 13px;
  }
  & #xThemeMenu .x-h {
    font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
    color: var(--x-muted); padding: 6px 8px 2px;
  }
  & #xThemeMenu .x-seg {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px;
    background: var(--x-well); border: 1px solid var(--x-line); border-radius: 999px; padding: 3px;
  }
  & #xThemeMenu .x-seg.x-4 { grid-template-columns: repeat(2, 1fr); }
  & #xThemeMenu button {
    font: inherit; color: var(--x-ink); background: none; border: 0; border-radius: 999px;
    height: 30px; padding: 0 8px; cursor: pointer; white-space: nowrap;
    display: flex; align-items: center; justify-content: center; gap: 6px;
  }
  & #xThemeMenu button:hover { background: var(--x-hover); }
  & #xThemeMenu button[aria-pressed="true"] { background: var(--x-accent); color: var(--x-on-accent); }
  & #xThemeMenu .x-refresh { margin-top: 6px; border-top: 1px solid var(--x-line) !important; border-radius: 12px; height: 34px; color: var(--x-muted); }
  & #xThemeMenu .x-refresh:hover { color: var(--x-ink); }
  & #xThemeMenu .x-sw { width: 11px; height: 11px; border-radius: 50%; border: 1px solid var(--x-line); flex: none; }
  /* своя палитра вместо системного окна «Цвет»: всё с !important,
     иначе общие правила для кнопок просмотрщика перекрашивают кружки */
  & #xColorPop {
    position: fixed !important; z-index: 100000 !important;
    width: 234px !important; box-sizing: border-box !important;
    padding: 12px !important; border-radius: 22px !important;
    background: var(--x-bar) !important; color: var(--x-ink) !important;
    border: 1px solid var(--x-line) !important;
    box-shadow: var(--x-pop) !important;
    animation: x-pop calc(.3s * var(--fm-k, 1)) var(--fm-spring, cubic-bezier(.2, .9, .3, 1.15)) both;
  }
  /* Firefox рисует кнопки системным стилем Windows (appearance: auto), и стили
     пользователя его не отключают — отсюда серые квадраты. Выключаем явно. */
  & #xColorPop :is(button, input) { appearance: none !important; -moz-appearance: none !important; }
  & #xColorPop .x-grid { display: grid !important; grid-template-columns: repeat(5, 34px) !important; gap: 8px !important; justify-content: space-between !important; }
  & #xColorPop .x-recent { margin-top: 10px !important; padding-top: 10px !important; border-top: 1px solid var(--x-line) !important; }
  & #xColorPop button.x-dot {
    width: 34px !important; height: 34px !important; min-width: 0 !important;
    padding: 0 !important; margin: 0 !important; border: 0 !important;
    border-radius: 50% !important; cursor: pointer !important;
    background: var(--c) !important; background-image: none !important;
    box-shadow: inset 0 0 0 1px rgb(128 128 128 / .4) !important;
    outline: none !important;
    transition: transform .15s ease !important;
  }
  & #xColorPop button.x-dot:hover { transform: scale(1.12) !important; background: var(--c) !important; }
  & #xColorPop button.x-dot[aria-pressed="true"] {
    box-shadow: inset 0 0 0 1px rgb(128 128 128 / .4), 0 0 0 2px var(--x-bar), 0 0 0 4px var(--x-accent) !important;
  }
  & #xColorPop button.x-more, & #xColorPop button.x-ok {
    display: block !important; width: 100% !important; height: auto !important; min-width: 0 !important;
    margin: 10px 0 0 !important; padding: 9px 12px !important;
    border: 0 !important; border-radius: 999px !important; cursor: pointer !important;
    background: var(--x-hover) !important; color: var(--x-ink) !important;
    font: 500 13px "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;
  }
  & #xColorPop button.x-more:hover { background: var(--x-press) !important; }
  & #xColorPop .x-custom { margin-top: 12px !important; display: flex !important; flex-direction: column !important; gap: 10px !important; }
  & #xColorPop .x-sv {
    position: relative !important; height: 130px !important; border-radius: 14px !important;
    background: linear-gradient(to top, #000, transparent), linear-gradient(to right, #fff, transparent), var(--h, #f00) !important;
    cursor: crosshair !important; touch-action: none !important;
  }
  & #xColorPop .x-hue {
    position: relative !important; height: 14px !important; border-radius: 999px !important;
    background: linear-gradient(to right, #f00, #ff0 17%, #0f0 33%, #0ff 50%, #00f 67%, #f0f 83%, #f00) !important;
    cursor: pointer !important; touch-action: none !important;
  }
  & #xColorPop .x-knob {
    position: absolute !important; width: 18px !important; height: 18px !important;
    border-radius: 50% !important; translate: -50% -50% !important; pointer-events: none !important;
    background: var(--c) !important;
    box-shadow: 0 0 0 3px #fff, 0 1px 6px rgb(0 0 0 / .5) !important;
  }
  & #xColorPop .x-hue .x-knob { top: 50% !important; }
  & #xColorPop .x-row { display: flex !important; align-items: center !important; gap: 8px !important; }
  & #xColorPop .x-preview {
    flex: none !important; width: 32px !important; height: 32px !important; border-radius: 50% !important;
    background: var(--c) !important; box-shadow: inset 0 0 0 1px rgb(128 128 128 / .4) !important;
  }
  & #xColorPop input.x-hex {
    flex: 1 !important; min-width: 0 !important; height: 32px !important; box-sizing: border-box !important;
    padding: 0 12px !important; border-radius: 999px !important; border: 1px solid var(--x-line) !important;
    background: var(--x-field) !important; color: var(--x-ink) !important;
    font: 600 13px ui-monospace, "Cascadia Mono", Consolas, monospace !important; text-transform: uppercase !important;
  }
  & #xColorPop button.x-ok {
    flex: none !important; width: auto !important; margin: 0 !important; padding: 7px 14px !important;
    background: var(--x-accent) !important; color: var(--x-on-accent) !important; font-weight: 600 !important;
  }
  /* уведомление «Открыто на стр. N» */
  & #xNotice {
    position: fixed !important; left: 50% !important; bottom: 24px !important; z-index: 100000 !important;
    translate: -50% 0 !important;
    display: flex !important; align-items: center !important; gap: 12px !important;
    padding: 8px 8px 8px 18px !important; border-radius: 999px !important;
    background: var(--x-bar) !important; color: var(--x-ink) !important;
    border: 1px solid var(--x-line) !important; box-shadow: var(--x-pop) !important;
    font: 500 13.5px "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;
    animation: x-pop calc(.38s * var(--fm-k, 1)) var(--fm-spring, cubic-bezier(.2, .9, .3, 1.15)) both;
    transition: opacity .3s ease, translate .3s ease !important;
  }
  & #xNotice.x-out { opacity: 0 !important; translate: -50% 10px !important; }
  & #xNotice button {
    appearance: none !important; border: 0 !important; cursor: pointer !important;
    padding: 6px 14px !important; border-radius: 999px !important;
    background: var(--x-accent) !important; color: var(--x-on-accent) !important;
    font: 600 13px "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif !important;
  }
  @keyframes x-pop { from { opacity: 0; transform: translateY(-8px) scale(.9); } }

  /* ---- плавность ---- */
  /* первые страницы документа проявляются мягко при открытии */
  & .pdfViewer > .page:nth-child(-n+4) { animation: x-page calc(.6s * var(--fm-k, 1)) var(--fm-ease, cubic-bezier(.2, .8, .2, 1)) both; }
  & .pdfViewer > .page:nth-child(2) { animation-delay: .06s; }
  & .pdfViewer > .page:nth-child(3) { animation-delay: .12s; }
  & .pdfViewer > .page:nth-child(4) { animation-delay: .18s; }
  @keyframes x-page { from { opacity: 0; translate: 0 18px; scale: .98; } }
  /* всплывающие меню PDF.js (поиск, режимы, рисование) — пружинкой */
  & :is(.doorHanger, .doorHangerRight, #findbar, #secondaryToolbar, .editorParamsToolbar):not(.hidden) {
    animation: x-pop calc(.34s * var(--fm-k, 1)) var(--fm-spring, cubic-bezier(.2, .9, .3, 1.15)) both;
  }
  @media (prefers-reduced-motion: reduce) {
    & :is(.page, .doorHanger, .doorHangerRight, #findbar, #secondaryToolbar, .editorParamsToolbar, #xNotice, #xBookMenu, #xColorPop, #xThemeMenu) { animation: none !important; }
  }

  /* полосы прокрутки */
  & :is(#viewerContainer, #viewsManagerContent, #outlinesView, #thumbnailsView) {
    scrollbar-width: thin !important;
    scrollbar-color: var(--x-line) transparent !important;
  }
}
/* ======================= PDF-TWEAKS END ======================= */
""".replace("@ICONS@", icon_vars)

if __name__ == "__main__":
    import sys
    import re as _re
    _css = CSS.replace("AccentColorText", "var(--fm-user-on-accent, AccentColorText)")
    _css = _re.sub(r"\bAccentColor\b(?!Text)", "var(--fm-user-accent, AccentColor)", _css)
    sys.stdout.write(_css)
