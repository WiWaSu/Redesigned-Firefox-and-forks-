/* Redesigned Fox Studio — тонкая настройка оформления.
 *
 * Настройки лежат в pref "floorp.modern.studio" (JSON). Из них собирается
 * CSS и подключается как пользовательская таблица стилей ко всему браузеру
 * (окна, меню, новая вкладка) — изменения видны сразу, без перезапуска.
 *
 * Страница настроек: resource://pdftweaks/studio.html (импортирует SCHEMA
 * отсюда же, поэтому на верхнем уровне модуля нет обращений к Services).
 */

export const PREF = "floorp.modern.studio";
// версия Redesigned Fox — меняется вместе с VERSION (tools/build.sh проверяет)
export const APP_VERSION = "1.19.0";

/* Описание всех настроек: из него рисуется страница, проверяются значения
   и собирается CSS. null = «как в теме». */
export const SCHEMA = [
  { group: "colors", title: "Цвета", items: [
    { key: "accent", type: "color", label: "Акцент", hint: "Кнопки, выделение, ползунки" },
    { key: "frame", type: "color", label: "Фон окна", hint: "Вокруг страницы и под вкладками" },
    { key: "bar", type: "color", label: "Поля и адресная строка" },
    { key: "menuBg", type: "color", label: "Фон меню и панелей" },
    { key: "ink", type: "color", label: "Текст интерфейса" },
    { key: "menuAlpha", type: "range", label: "Прозрачность меню", min: 0, max: 60, step: 5, unit: "%" },
    { key: "menuBlur", type: "range", label: "Размытие под меню", min: 0, max: 40, step: 2, unit: "px" },
  ] },
  { group: "shape", title: "Форма", items: [
    { key: "square", type: "bool", label: "Без скруглений", hint: "Убирает все скругления: окно, вкладки, меню, кнопки, адресная строка, новая вкладка, PDF" },
    { key: "radius", type: "range", label: "Скругление страницы", min: 0, max: 36, step: 1, unit: "px" },
    { key: "gap", type: "range", label: "Отступ вокруг страницы", min: 0, max: 24, step: 1, unit: "px" },
    { key: "pageShadow", type: "range", label: "Тень под страницей", min: 0, max: 100, step: 5, unit: "%" },
    { key: "menuRadius", type: "range", label: "Скругление меню", min: 0, max: 32, step: 1, unit: "px" },
    { key: "buttonShape", type: "select", label: "Кнопки панели", options: [["round", "Круглые"], ["rounded", "Скруглённые"], ["square", "Квадратные"]] },
    { key: "density", type: "select", label: "Плотность", options: [["compact", "Компактно"], ["normal", "Обычно"], ["touch", "Крупно (сенсор)"]] },
  ] },
  { group: "tabs", title: "Вкладки", items: [
    { key: "tabShape", type: "select", label: "Форма вкладок", options: [["pill", "Таблетки"], ["rounded", "Скруглённые"], ["square", "Прямые"], ["underline", "Подчёркивание"], ["card", "Карточки"], ["chrome", "Как в Chrome"]] },
    { key: "tabSelected", type: "select", label: "Выбранная вкладка", options: [["soft", "Мягкий акцент"], ["accent", "Залита акцентом"], ["outline", "Обводка"], ["glass", "Стекло"], ["contrast", "Контрастная"], ["none", "Без подсветки"]] },
    { key: "tabHeight", type: "range", label: "Высота вкладок", min: 26, max: 48, step: 1, unit: "px" },
    { key: "tabMinWidth", type: "range", label: "Мин. ширина вкладки", min: 40, max: 260, step: 10, unit: "px" },
    { key: "tabClose", type: "select", label: "Крестик на вкладке", options: [["always", "Всегда"], ["hover", "При наведении"], ["never", "Скрыть"]] },
    { key: "tabWeight", type: "range", label: "Жирность названия", min: 300, max: 800, step: 100 },
    { key: "tabsHide", type: "select", label: "Скрыть вкладки", hint: "«У края» — вкладки спрятаны и выезжают, когда подводите мышь к краю окна. «Полностью» — их не видно совсем (Alt+Shift+T — показать / спрятать). Не компактный вид, а скрытие целиком", options: [["edge", "У края"], ["always", "Полностью"]] },
  ] },
  { group: "urlbar", title: "Адресная строка", items: [
    { key: "urlHeight", type: "range", label: "Высота", min: 28, max: 52, step: 1, unit: "px" },
    { key: "urlRadius", type: "range", label: "Скругление", min: 0, max: 26, step: 1, unit: "px" },
    { key: "urlAlign", type: "select", label: "Адрес", options: [["center", "По центру"], ["start", "Слева"]] },
    { key: "urlBorder", type: "select", label: "Рамка", options: [["glow", "Свечение"], ["line", "Тонкая линия"], ["none", "Без рамки"]] },
  ] },
  { group: "menus", title: "Меню правой кнопки", items: [
    { key: "menuStyle", type: "cards", label: "Стиль", options: [
      ["oneui", "One UI", "Крупные пункты-таблетки"],
      ["glass", "Стекло iOS", "Полупрозрачное, с размытием"],
      ["fluent", "Windows 11", "Компактное, полоска акцента"],
      ["macos", "macOS", "Синяя подсветка, плотное"],
      ["touch", "Сенсор", "Очень крупные пункты"],
      ["nothing", "Nothing", "Монохром и красная точка"],
      ["neon", "Неон", "Тёмное со свечением акцента"],
    ] },
    { key: "menuItemHeight", type: "range", label: "Высота пункта", min: 22, max: 52, step: 1, unit: "px" },
    { key: "menuFont", type: "range", label: "Размер текста", min: 11, max: 17, step: 0.5, unit: "px" },
    { key: "menuIcons", type: "bool", label: "Значки в меню" },
  ] },
  { group: "ctrltab", title: "Переключатель Ctrl+Tab", items: [
    { key: "ctrlTabPreview", type: "bool", label: "Показывать окно с превью", hint: "Ctrl+Tab переключает по недавно открытым и показывает миниатюры" },
    { key: "ctrlTabStyle", type: "cards", label: "Стиль", options: [
      ["ios", "iOS", "Большие карточки на размытом фоне"],
      ["windows", "Windows 11", "Как Alt+Tab: акрил и рамка"],
      ["list", "Список", "Только названия, без миниатюр"],
      ["neon", "Неон", "Тёмный, выбранная светится"],
    ] },
  ] },
  { group: "font", title: "Шрифт", items: [
    { key: "font", type: "select", label: "Шрифт интерфейса", options: [["segoe", "Segoe UI Variable"], ["inter", "Inter"], ["roboto", "Roboto"], ["system", "Системный"], ["arial", "Arial"], ["mono", "Моноширинный"], ["custom", "Свой…"]] },
    { key: "fontCustom", type: "text", label: "Свой шрифт", hint: "Название шрифта, установленного в Windows" },
    { key: "fontSize", type: "range", label: "Размер текста", min: 11, max: 17, step: 0.5, unit: "px" },
  ] },
  { group: "motion", title: "Анимации", items: [
    { key: "speed", type: "range", label: "Длительность", min: 0.3, max: 2, step: 0.1, unit: "×" },
    { key: "bounce", type: "select", label: "Пружинистость", options: [["none", "Без перелёта"], ["soft", "Мягкая"], ["ios", "Как в iOS"], ["strong", "Сильная"]] },
  ] },
  { group: "newtab", title: "Новая вкладка", items: [
    { key: "clockSize", type: "range", label: "Размер часов", min: 40, max: 220, step: 4, unit: "px" },
    { key: "clockWeight", type: "range", label: "Толщина цифр", min: 100, max: 900, step: 100 },
    { key: "clockFont", type: "select", label: "Шрифт часов", options: [["ui", "Как интерфейс"], ["serif", "С засечками"], ["mono", "Моноширинный"], ["rounded", "Округлый"]] },
    { key: "clockPos", type: "select", label: "Где часы", options: [["top", "Сверху"], ["center", "По центру"], ["hidden", "Скрыть"]] },
    { key: "showDate", type: "bool", label: "Дата под часами" },
    { key: "searchWidth", type: "range", label: "Ширина поиска", min: 30, max: 90, step: 5, unit: "%" },
    { key: "tiles", type: "bool", label: "Ярлыки сайтов" },
    { key: "wallBlur", type: "range", label: "Размытие обоев", min: 0, max: 40, step: 2, unit: "px" },
  ] },
  { group: "update", title: "Обновления", items: [
    { key: "checkUpdates", type: "bool", label: "Проверять обновления", hint: "Раз в сутки смотрит на github.com/WiWaSu/Redesigned-Firefox-and-forks- — есть ли новая версия. Ничего не скачивает сам" },
  ] },
  { group: "hide", title: "Показать / скрыть", items: [
    { key: "showBookmarks", type: "bool", label: "Панель закладок" },
    { key: "showSidebarButton", type: "bool", label: "Кнопка боковой панели" },
    { key: "showTabList", type: "bool", label: "Кнопка «Все вкладки»" },
    { key: "showNewTabButton", type: "bool", label: "Кнопка «Новая вкладка»" },
    { key: "showExtensions", type: "bool", label: "Кнопка расширений" },
    { key: "showNowBar", type: "bool", label: "Плашка Now Bar" },
    { key: "showCallBar", type: "bool", label: "Плашка звонка", hint: "Сверху по центру, когда в другой вкладке идёт звонок" },
    { key: "showProgress", type: "bool", label: "Полоска загрузки страницы" },
  ] },
];

/* Готовые наборы: меняют сразу много настроек */
export const PRESETS = [
  ["clean", "Чистый", { radius: 14, gap: 6, menuStyle: "fluent", tabShape: "rounded", tabSelected: "soft", bounce: "soft", menuAlpha: 0, urlBorder: "line" }],
  ["bubble", "Пузыри", { radius: 30, gap: 10, menuStyle: "oneui", tabShape: "pill", tabSelected: "accent", bounce: "strong", menuRadius: 28, urlRadius: 26, buttonShape: "round" }],
  ["glass", "Стекло", { radius: 26, gap: 10, menuStyle: "glass", tabShape: "pill", tabSelected: "glass", menuAlpha: 35, menuBlur: 24, bounce: "ios", ctrlTabStyle: "ios" }],
  ["sharp", "Острый", { radius: 0, gap: 0, menuRadius: 4, urlRadius: 4, buttonShape: "square", tabShape: "square", tabSelected: "contrast", menuStyle: "fluent", bounce: "none", speed: 0.7 }],
  ["neon", "Неон", { accent: "#00E5FF", frame: "#05060A", menuBg: "#0B0D14", menuStyle: "neon", tabShape: "underline", tabSelected: "outline", ctrlTabStyle: "neon", urlBorder: "glow" }],
  ["mac", "Как Mac", { menuStyle: "macos", tabShape: "card", tabSelected: "contrast", radius: 12, gap: 6, urlRadius: 8, buttonShape: "rounded", font: "system", ctrlTabStyle: "windows" }],
];

const COLOR = /^#[0-9a-fA-F]{6}$/;
const FONT_TEXT = /^[\p{L}\p{N} ._-]{1,60}$/u;

/* оставить только известные ключи с правильными значениями */
export function sanitize(raw) {
  const out = {};
  if (!raw || typeof raw !== "object") {
    return out;
  }
  for (const g of SCHEMA) {
    for (const it of g.items) {
      const v = raw[it.key];
      if (v === null || v === undefined || v === "") {
        continue;
      }
      if (it.type === "color" && typeof v === "string" && COLOR.test(v)) {
        out[it.key] = v.toUpperCase();
      } else if (it.type === "range" && typeof v === "number" && isFinite(v)) {
        out[it.key] = Math.min(it.max, Math.max(it.min, v));
      } else if ((it.type === "select" || it.type === "cards") && it.options.some(o => o[0] === v)) {
        out[it.key] = v;
      } else if (it.type === "bool" && typeof v === "boolean") {
        out[it.key] = v;
      } else if (it.type === "text" && typeof v === "string" && FONT_TEXT.test(v.trim())) {
        out[it.key] = v.trim();
      }
    }
  }
  return out;
}

const SPRINGS = {
  none: ["cubic-bezier(.2, .8, .2, 1)", "cubic-bezier(.2, .8, .2, 1)"],
  soft: ["cubic-bezier(.2, .9, .25, 1.08)", "cubic-bezier(.2, .8, .2, 1)"],
  ios: [
    "linear(0, 0.0385, 0.135, 0.2646, 0.4078, 0.5501, 0.6814, 0.7955, 0.8894, 0.9626, 1.016, 1.0519, 1.073, 1.0823, 1.0828, 1.0772, 1.0676, 1.0561, 1.0441, 1.0325, 1.0222, 1.0134, 1.0063, 1.0009, 0.9972, 0.9948, 0.9935, 0.9931, 0.9934, 0.9941, 0.995, 0.9961, 0.9971, 0.998, 0.9987, 0.9993, 0.9997, 1)",
    "linear(0, 0.0661, 0.2032, 0.3554, 0.4963, 0.6161, 0.7127, 0.7881, 0.8454, 0.8883, 0.9199, 0.9429, 0.9596, 0.9715, 0.98, 0.986, 0.9902, 0.9932, 0.9953, 0.9967, 0.9978, 0.9985, 0.9989, 0.9993, 1)",
  ],
  strong: [
    "linear(0, 0.06, 0.21, 0.4, 0.6, 0.79, 0.95, 1.07, 1.15, 1.18, 1.17, 1.13, 1.08, 1.03, 0.99, 0.96, 0.95, 0.95, 0.96, 0.98, 0.99, 1.005, 1.01, 1.01, 1.005, 1)",
    "linear(0, 0.0661, 0.2032, 0.3554, 0.4963, 0.6161, 0.7127, 0.7881, 0.8454, 0.8883, 0.9199, 0.9429, 0.9596, 0.9715, 0.98, 0.986, 0.9902, 0.9932, 0.9953, 0.9967, 0.9978, 0.9985, 0.9989, 0.9993, 1)",
  ],
};
const FONTS = {
  segoe: '"Segoe UI Variable Display", "Segoe UI Variable Text", "Segoe UI", sans-serif',
  inter: '"Inter", "Inter Variable", "Segoe UI", sans-serif',
  roboto: '"Roboto", "Roboto Flex", "Segoe UI", sans-serif',
  system: "system-ui, sans-serif",
  arial: "Arial, Helvetica, sans-serif",
  mono: '"Cascadia Code", "Cascadia Mono", Consolas, monospace',
};
const CLOCK_FONTS = {
  serif: '"Georgia", "Times New Roman", serif',
  mono: '"Cascadia Code", "Cascadia Mono", Consolas, monospace',
  rounded: '"Nunito", "Varela Round", "Segoe UI Variable Display", sans-serif',
};

/* меню правой кнопки: стили */
const MENU_STYLES = {
  oneui: `
    menupopup::part(content) { border-radius: 26px !important; padding: 8px !important; }
    menupopup > :is(menuitem, menu) { border-radius: 16px !important; padding-inline: 14px !important; }`,
  glass: `
    menupopup::part(content) {
      background-color: color-mix(in srgb, var(--fm-menu, #1c1d20) 62%, transparent) !important;
      backdrop-filter: blur(26px) saturate(1.8) !important;
      border: 1px solid light-dark(rgb(255 255 255 / .6), rgb(255 255 255 / .14)) !important;
      box-shadow: inset 0 1px 0 light-dark(rgb(255 255 255 / .8), rgb(255 255 255 / .12)), 0 18px 50px rgb(0 0 0 / .35) !important;
      border-radius: 24px !important;
    }
    menupopup > :is(menuitem, menu) { border-radius: 12px !important; }
    menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]) {
      background-color: light-dark(rgb(0 0 0 / .07), rgb(255 255 255 / .12)) !important;
    }`,
  fluent: `
    menupopup::part(content) { border-radius: 8px !important; padding: 4px !important; }
    menupopup > :is(menuitem, menu) {
      border-radius: 4px !important; min-height: 30px !important; padding-block: 3px !important;
      margin-inline: 0 !important; position: relative;
    }
    menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled])::before {
      content: ""; position: absolute; inset-inline-start: 0; top: 25%; height: 50%; width: 3px;
      border-radius: 3px; background: var(--fm-accent);
    }
    menupopup > menuseparator { margin-inline: 0 !important; }`,
  macos: `
    menupopup::part(content) { border-radius: 10px !important; padding: 5px !important; }
    menupopup > :is(menuitem, menu) {
      border-radius: 5px !important; min-height: 24px !important; padding-block: 2px !important;
      margin-inline: 0 !important; font-size: 13px !important;
    }
    menupopup > :is(menuitem, menu):is([_moz-menuactive], :hover):not([disabled]) {
      background-color: var(--fm-accent) !important; color: var(--fm-on-accent, #fff) !important;
    }
    menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) :is(.menu-accel, .menu-icon) { color: inherit !important; fill: currentColor !important; }`,
  touch: `
    menupopup::part(content) { border-radius: 30px !important; padding: 10px !important; }
    menupopup > :is(menuitem, menu) {
      border-radius: 20px !important; min-height: 48px !important; padding-inline: 18px !important; font-size: 15px !important;
    }
    menupopup > :is(menuitem, menu) > .menu-icon { width: 20px !important; height: 20px !important; }`,
  nothing: `
    menupopup::part(content) {
      border-radius: 18px !important; padding: 6px !important;
      background-color: light-dark(#f4f4f4, #0c0c0c) !important; border: 1px solid light-dark(#d6d6d6, #2a2a2a) !important;
    }
    menupopup > :is(menuitem, menu) {
      border-radius: 10px !important; font-family: "Cascadia Mono", Consolas, monospace !important;
      font-size: 12.5px !important; letter-spacing: .02em; text-transform: uppercase; position: relative;
    }
    menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) {
      background-color: light-dark(#e8e8e8, #1c1c1c) !important; color: inherit !important;
    }
    menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled])::after {
      content: ""; position: absolute; inset-inline-end: 12px; top: calc(50% - 3px);
      width: 6px; height: 6px; border-radius: 50%; background: #ff2d2d;
    }`,
  neon: `
    menupopup::part(content) {
      border-radius: 18px !important; padding: 6px !important;
      background-color: #0b0d14 !important; color: #e8f6ff !important;
      border: 1px solid color-mix(in srgb, var(--fm-accent) 55%, transparent) !important;
      box-shadow: 0 0 0 1px color-mix(in srgb, var(--fm-accent) 20%, transparent), 0 0 28px color-mix(in srgb, var(--fm-accent) 35%, transparent), 0 18px 50px rgb(0 0 0 / .6) !important;
    }
    menupopup > :is(menuitem, menu) { border-radius: 10px !important; color: #e8f6ff !important; }
    menupopup > :is(menuitem, menu):is([_moz-menuactive]):not([disabled]) {
      background-color: color-mix(in srgb, var(--fm-accent) 18%, transparent) !important;
      color: #fff !important; text-shadow: 0 0 8px var(--fm-accent);
      box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--fm-accent) 50%, transparent);
    }
    menupopup > menuseparator { border-color: color-mix(in srgb, var(--fm-accent) 30%, transparent) !important; }`,
};

/* Ctrl+Tab: стили */
const CTRLTAB_BASE = `
  #ctrlTab-panel { --panel-padding: 22px 18px 18px !important; font-weight: 600 !important; }
  #ctrlTab-panel::part(content) { animation: fm-ct-in calc(.42s * var(--fm-k, 1)) var(--fm-spring, ease) both; }
  @keyframes fm-ct-in { from { opacity: 0; scale: .92; } }
  .ctrlTab-preview, #ctrlTab-showAll { text-shadow: none !important; }
  .ctrlTab-preview-inner { transition: scale calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease), background-color .2s ease, border-color .2s ease !important; }
  .ctrlTab-preview:focus > .ctrlTab-preview-inner { scale: 1.06; }
  .ctrlTab-canvas { box-shadow: 0 6px 18px rgb(0 0 0 / .35) !important; }
  .ctrlTab-favicon[src] { border-radius: 12px !important; border: 0 !important; box-shadow: 0 4px 12px rgb(0 0 0 / .35); }`;
const CTRLTAB_STYLES = {
  ios: `
    #ctrlTab-panel::part(content) {
      background-color: rgb(20 20 24 / .55) !important; backdrop-filter: blur(30px) saturate(1.8) !important;
      border: 1px solid rgb(255 255 255 / .14) !important; border-radius: 34px !important; color: #fff !important;
    }
    .ctrlTab-preview-inner { border-radius: 24px !important; border: 0 !important; padding: 10px !important; }
    .ctrlTab-canvas, .ctrlTab-canvas > :is(img, canvas) { border-radius: 18px !important; overflow: hidden; }
    .ctrlTab-preview:focus > .ctrlTab-preview-inner { background-color: rgb(255 255 255 / .16) !important; }
    #ctrlTab-showAll { border-radius: 999px !important; border: 0 !important; background: rgb(255 255 255 / .14) !important; }`,
  windows: `
    #ctrlTab-panel::part(content) {
      background-color: light-dark(rgb(243 243 243 / .82), rgb(32 32 32 / .82)) !important; backdrop-filter: blur(40px) saturate(1.4) !important;
      border: 1px solid light-dark(rgb(0 0 0 / .1), rgb(255 255 255 / .1)) !important; border-radius: 12px !important;
      color: light-dark(#1b1b1b, #fff) !important;
    }
    .ctrlTab-preview-inner { border-radius: 8px !important; border: 2px solid transparent !important; }
    .ctrlTab-canvas, .ctrlTab-canvas > :is(img, canvas) { border-radius: 6px !important; }
    .ctrlTab-preview:focus > .ctrlTab-preview-inner { background: transparent !important; border-color: light-dark(#1b1b1b, #fff) !important; scale: 1 !important; }
    .ctrlTab-preview-inner { flex-direction: column-reverse !important; }
    .ctrlTab-label { text-align: start !important; font-weight: 500 !important; margin-bottom: 6px; }
    #ctrlTab-showAll { border-radius: 6px !important; border: 0 !important; }`,
  list: `
    #ctrlTab-panel::part(content) {
      background-color: var(--fm-menu, #1c1d20) !important; border: 1px solid var(--fm-line, rgb(255 255 255 / .1)) !important;
      border-radius: 22px !important; color: var(--fm-ink, #fff) !important;
    }
    #ctrlTab-previews { grid-template-columns: 1fr !important; row-gap: 4px !important; min-width: 340px; }
    .ctrlTab-canvas, .ctrlTab-placeholder { display: none !important; }
    .ctrlTab-favicon-container { order: -1; }
    .ctrlTab-favicon[src] { width: 22px !important; height: 22px !important; margin: 0 10px 0 0 !important; padding: 2px !important; box-shadow: none; }
    .ctrlTab-preview-inner { flex-direction: row !important; align-items: center !important; margin: 0 !important; padding: 8px 14px !important; border: 0 !important; border-radius: 14px !important; }
    .ctrlTab-label { text-align: start !important; font-weight: 500 !important; }
    .ctrlTab-preview:focus > .ctrlTab-preview-inner { background-color: var(--fm-soft, rgb(255 255 255 / .12)) !important; scale: 1 !important; }`,
  neon: `
    #ctrlTab-panel::part(content) {
      background-color: rgb(6 8 14 / .9) !important; border: 1px solid color-mix(in srgb, var(--fm-accent) 50%, transparent) !important;
      border-radius: 22px !important; color: #e8f6ff !important;
      box-shadow: 0 0 40px color-mix(in srgb, var(--fm-accent) 35%, transparent) !important;
    }
    .ctrlTab-preview-inner { border-radius: 14px !important; border: 1px solid transparent !important; }
    .ctrlTab-canvas, .ctrlTab-canvas > :is(img, canvas) { border-radius: 10px !important; }
    .ctrlTab-preview:focus > .ctrlTab-preview-inner {
      background: color-mix(in srgb, var(--fm-accent) 14%, transparent) !important;
      border-color: var(--fm-accent) !important; box-shadow: 0 0 22px color-mix(in srgb, var(--fm-accent) 55%, transparent);
    }
    .ctrlTab-preview:focus .ctrlTab-label { text-shadow: 0 0 10px var(--fm-accent) !important; }`,
};

/* вкладки: форма */
const TAB_SHAPES = {
  pill: ".tabbrowser-tab > .tab-stack > .tab-background { border-radius: 999px !important; }",
  rounded: ".tabbrowser-tab > .tab-stack > .tab-background { border-radius: 10px !important; }",
  square: ".tabbrowser-tab > .tab-stack > .tab-background { border-radius: 2px !important; }",
  underline: `
    .tabbrowser-tab > .tab-stack > .tab-background { border-radius: 0 !important; background: transparent !important; box-shadow: none !important; outline: none !important; }
    .tabbrowser-tab > .tab-stack > .tab-background::after {
      content: ""; position: absolute; inset: auto 22% 2px; height: 3px; border-radius: 3px;
      background: var(--fm-accent); scale: 0 1; transition: scale calc(.35s * var(--fm-k, 1)) var(--fm-spring, ease);
    }
    .tabbrowser-tab > .tab-stack > .tab-background { position: relative; }
    .tabbrowser-tab[selected] > .tab-stack > .tab-background::after { scale: 1 1; }
    /* вертикальные вкладки: полоска слева */
    #tabbrowser-tabs[orient="vertical"] .tabbrowser-tab > .tab-stack > .tab-background::after { inset: 22% auto 22% 3px; width: 3px; height: auto; scale: 1 0; }
    #tabbrowser-tabs[orient="vertical"] .tabbrowser-tab[selected] > .tab-stack > .tab-background::after { scale: 1 1; }`,
  card: `
    .tabbrowser-tab > .tab-stack > .tab-background { border-radius: 10px 10px 0 0 !important; margin-bottom: 0 !important; }`,
  chrome: `
    .tabbrowser-tab > .tab-stack > .tab-background { border-radius: 12px 12px 0 0 !important; margin-block: 4px 0 !important; }
    .tabbrowser-tab[selected] > .tab-stack > .tab-background { background: var(--fm-bar, #2a2b2f) !important; }`,
};
const TAB_SELECTED = {
  soft: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background { background: var(--fm-soft) !important; box-shadow: none !important; }
         .tabbrowser-tab[selected] .tab-label { color: var(--fm-accent) !important; }`,
  accent: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background { background: var(--fm-accent) !important; box-shadow: 0 4px 14px color-mix(in srgb, var(--fm-accent) 40%, transparent) !important; }
           .tabbrowser-tab[selected] :is(.tab-label, .tab-close-button) { color: var(--fm-on-accent, #fff) !important; fill: currentColor !important; }`,
  outline: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background { background: transparent !important; outline: 1.5px solid var(--fm-accent) !important; outline-offset: -1.5px !important; box-shadow: none !important; }
            .tabbrowser-tab[selected] .tab-label { color: var(--fm-accent) !important; }`,
  glass: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background {
            background: light-dark(rgb(255 255 255 / .7), rgb(255 255 255 / .1)) !important;
            box-shadow: inset 0 1px 0 light-dark(#fff, rgb(255 255 255 / .2)), 0 4px 14px rgb(0 0 0 / .18) !important;
            backdrop-filter: blur(12px); }
          .tabbrowser-tab[selected] .tab-label { color: inherit !important; }`,
  none: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background { background: transparent !important; box-shadow: none !important; outline: none !important; }
         .tabbrowser-tab > .tab-stack > .tab-background::before { display: none !important; }
         .tabbrowser-tab[selected] .tab-label { color: inherit !important; }`,
  contrast: `.tabbrowser-tab:is([selected], [multiselected]) > .tab-stack > .tab-background { background: var(--fm-ink) !important; box-shadow: none !important; }
             .tabbrowser-tab[selected] :is(.tab-label, .tab-close-button) { color: var(--fm-frame, #000) !important; fill: currentColor !important; }`,
};

/* «Без скруглений»: тот же CSS, что в square-chrome.css / square-content.css
   (обновляется командой python3 tools/pack_themes.py) */
// SQUARE-CSS BEGIN
const SQUARE_CHROME = "/* Redesigned Fox: «Без скруглений» — окна браузера (LAYER заменяется на имя слоя) */\n@-moz-document url-prefix(\"chrome://\") {\n@layer LAYER {\n:root, menupopup, panel, tooltip, #urlbar, .urlbarView {\n  --fm-radius: 0px !important; --panel-border-radius: 0px !important; --arrowpanel-border-radius: 0px !important;\n  --menuitem-border-radius: 0px !important; --arrowpanel-menuitem-border-radius: 0px !important;\n  --urlbarview-border-radius: 0px !important; --urlbar-border-radius: 0px !important;\n  --toolbarbutton-border-radius: 0px !important; --tab-border-radius: 0px !important;\n  --border-radius-small: 0px !important; --border-radius-medium: 0px !important;\n  --border-radius-large: 0px !important; --border-radius-xlarge: 0px !important; --button-border-radius: 0px !important;\n}\n:not(#fm-q1#fm-q2#fm-q3):not(radio, checkbox, .radio-check, .checkbox-check, input[type=\"radio\"], input[type=\"checkbox\"], .toggle-button, moz-toggle),\n:not(#fm-q1#fm-q2#fm-q3)::before, :not(#fm-q1#fm-q2#fm-q3)::after { border-radius: 0 !important; }\n:not(#fm-q1#fm-q2#fm-q3):is(menupopup, panel, tooltip)::part(content) { border-radius: 0 !important; }\n}\n}\n";
const SQUARE_CONTENT = "/* Redesigned Fox: «Без скруглений» — страницы браузера, новая вкладка, PDF (LAYER заменяется на имя слоя) */\n@-moz-document url-prefix(\"about:\"), url-prefix(\"chrome://\"), url-prefix(\"resource://\") {\n@layer LAYER {\n:root {\n  --fm-radius: 0px !important; --x-radius: 0px !important; --card-border-radius: 0px !important;\n  --box-border-radius: 0px !important; --button-border-radius: 0px !important; --input-text-border-radius: 0px !important;\n  --select-border-radius: 0px !important; --page-nav-button-border-radius: 0px !important;\n  --border-radius-small: 0px !important; --border-radius-medium: 0px !important;\n  --border-radius-large: 0px !important; --border-radius-xlarge: 0px !important;\n}\n:not(#fm-q1#fm-q2#fm-q3):not(input[type=\"radio\"], input[type=\"checkbox\"], .toggle-button),\n:not(#fm-q1#fm-q2#fm-q3)::before, :not(#fm-q1#fm-q2#fm-q3)::after { border-radius: 0 !important; }\n}\n}\n@layer LAYER {\n:root:has(#outerContainer #viewerContainer) { --x-radius: 0px !important; }\n:root:has(#outerContainer #viewerContainer) :not(#fm-q1#fm-q2#fm-q3),\n:root:has(#outerContainer #viewerContainer) :not(#fm-q1#fm-q2#fm-q3)::before,\n:root:has(#outerContainer #viewerContainer) :not(#fm-q1#fm-q2#fm-q3)::after { border-radius: 0 !important; }\n}\n";
// SQUARE-CSS END

const px = n => `${n}px`;

/* собрать CSS из настроек */
export function buildCss(cfgRaw) {
  const c = sanitize(cfgRaw);
  const has = k => c[k] !== undefined;
  const root = [];
  const chrome = [];
  const newtab = [];

  // ---- цвета и общие переменные (действуют и в окне, и на новой вкладке)
  if (has("accent")) {
    const r = parseInt(c.accent.slice(1, 3), 16), g = parseInt(c.accent.slice(3, 5), 16), b = parseInt(c.accent.slice(5, 7), 16);
    const on = 0.299 * r + 0.587 * g + 0.114 * b > 160 ? "#000000" : "#ffffff";
    root.push(`--fm-user-accent: ${c.accent} !important; --fm-user-on-accent: ${on} !important;`);
  }
  if (has("speed")) {
    root.push(`--fm-k: ${c.speed} !important;`);
  }
  if (has("bounce")) {
    root.push(`--fm-spring: ${SPRINGS[c.bounce][0]} !important; --fm-ease: ${SPRINGS[c.bounce][1]} !important;`);
  }
  let fontStack = null;
  if (has("font")) {
    fontStack = c.font === "custom" ? (has("fontCustom") ? `"${c.fontCustom}", "Segoe UI", sans-serif` : null) : FONTS[c.font];
  }

  // ---- окно браузера
  const v = [];
  if (has("frame")) {
    v.push(`--fm-frame: ${c.frame} !important; --toolbox-background-color: ${c.frame} !important; --toolbox-background-color-inactive: ${c.frame} !important; --toolbar-background-color: ${c.frame} !important; --toolbar-bgcolor: ${c.frame} !important; --sidebar-background-color: ${c.frame} !important;`);
    chrome.push(`:is(#navigator-toolbox, #nav-bar, #PersonalToolbar, #TabsToolbar, #browser, #sidebar-main, #sidebar-box, #panel-sidebar-select-box) { background-color: ${c.frame} !important; }`);
    chrome.push(`body, #navigator-toolbox { background-image: none !important; }`);
  }
  if (has("bar")) {
    v.push(`--fm-bar: ${c.bar} !important; --fm-field: ${c.bar} !important; --toolbar-field-background-color: ${c.bar} !important; --urlbar-background-color: ${c.bar} !important;`);
  }
  if (has("ink")) {
    v.push(`--fm-ink: ${c.ink} !important; --toolbar-color: ${c.ink} !important; --toolbox-text-color: ${c.ink} !important; --toolbarbutton-icon-fill: ${c.ink} !important;`);
    chrome.push(`:is(#navigator-toolbox, #sidebar-main) { color: ${c.ink} !important; }`);
  }
  if (has("radius")) {
    v.push(`--fm-radius: ${px(c.radius)} !important;`);
    chrome.push(`#tabbrowser-tabpanels .browserContainer { border-radius: ${px(c.radius)} !important; }`);
  }
  if (has("gap")) {
    v.push(`--fm-gap: ${px(c.gap)} !important;`);
    chrome.push(`:root:not([inDOMFullscreen], [inFullscreen]) #tabbrowser-tabbox { padding: 0 ${px(c.gap)} ${px(c.gap)} !important; }`);
  }
  if (has("pageShadow")) {
    const a = c.pageShadow / 100;
    chrome.push(`#tabbrowser-tabpanels .browserContainer { box-shadow: 0 1px 3px rgb(0 0 0 / ${(a * 0.4).toFixed(2)}), 0 12px 34px rgb(0 0 0 / ${(a * 0.45).toFixed(2)}) !important; }`);
  }
  if (v.length) {
    chrome.push(`:root, menupopup, panel, tooltip, #urlbar, .urlbarView { ${v.join(" ")} }`);
  }

  // меню и панели
  const menuVars = [];
  if (has("menuBg")) {
    menuVars.push(`--fm-menu: ${c.menuBg} !important; --panel-background: ${c.menuBg} !important; --arrowpanel-background: ${c.menuBg} !important; --panel-background-color: ${c.menuBg} !important; --menu-background-color: ${c.menuBg} !important;`);
  }
  if (menuVars.length) {
    chrome.push(`:root, menupopup, panel, tooltip { ${menuVars.join(" ")} }`);
  }
  if (has("menuStyle")) {
    chrome.push(MENU_STYLES[c.menuStyle]);
  }
  if (has("menuAlpha") && c.menuAlpha > 0) {
    chrome.push(`:is(menupopup, panel[type="arrow"])::part(content) { background-color: color-mix(in srgb, var(--fm-menu, #1c1d20) ${100 - c.menuAlpha}%, transparent) !important; }`);
  }
  if (has("menuBlur") && c.menuBlur > 0) {
    chrome.push(`:is(menupopup, panel[type="arrow"])::part(content) { backdrop-filter: blur(${px(c.menuBlur)}) saturate(1.6) !important; }`);
  }
  if (has("menuRadius")) {
    chrome.push(`:is(menupopup, panel)::part(content) { border-radius: ${px(c.menuRadius)} !important; }`);
    chrome.push(`menupopup > :is(menuitem, menu), .subviewbutton { border-radius: ${px(Math.max(0, Math.round(c.menuRadius * 0.6)))} !important; }`);
  }
  if (has("menuItemHeight")) {
    chrome.push(`menupopup > :is(menuitem, menu) { min-height: ${px(c.menuItemHeight)} !important; padding-block: 0 !important; }`);
  }
  if (has("menuFont")) {
    chrome.push(`menupopup > :is(menuitem, menu) { font-size: ${px(c.menuFont)} !important; }`);
  }
  if (c.menuIcons === false) {
    chrome.push(`menupopup > :is(menuitem, menu) > .menu-icon { display: none !important; }`);
  }

  // Ctrl+Tab
  if (has("ctrlTabStyle")) {
    chrome.push(CTRLTAB_BASE, CTRLTAB_STYLES[c.ctrlTabStyle]);
  }

  // кнопки
  if (has("buttonShape")) {
    const r = { round: "999px", rounded: "10px", square: "3px" }[c.buttonShape];
    v.push(`--toolbarbutton-border-radius: ${r} !important;`);
    chrome.push(`:root { --toolbarbutton-border-radius: ${r} !important; }`);
    chrome.push(`toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack, .toolbarbutton-text) { border-radius: ${r} !important; }`);
  }
  if (has("density")) {
    const pad = { compact: "6px", normal: "8px", touch: "11px" }[c.density];
    chrome.push(`:root { --toolbarbutton-inner-padding: ${pad} !important; --toolbarbutton-padding-inner: ${pad} !important; }`);
    chrome.push(`toolbar .toolbarbutton-1 > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) { padding: ${pad} !important; }`);
    chrome.push(`#nav-bar { padding-block: ${c.density === "compact" ? "1px" : c.density === "touch" ? "7px" : "4px"} !important; }`);
  }

  // вкладки
  if (has("tabShape")) {
    chrome.push(TAB_SHAPES[c.tabShape]);
  }
  if (has("tabSelected")) {
    chrome.push(TAB_SELECTED[c.tabSelected]);
  }
  if (has("tabHeight")) {
    chrome.push(`:root { --tab-min-height: ${px(c.tabHeight)} !important; }`);
    chrome.push(`.tabbrowser-tab { min-height: ${px(c.tabHeight)} !important; } .tab-content { min-height: ${px(c.tabHeight)} !important; }`);
  }
  if (has("tabMinWidth")) {
    chrome.push(`:root { --tab-min-width: ${px(c.tabMinWidth)} !important; } .tabbrowser-tab:not([pinned]) { min-width: ${px(c.tabMinWidth)} !important; }`);
  }
  if (has("tabClose")) {
    if (c.tabClose === "never") {
      chrome.push(`.tabbrowser-tab:not([pinned]) .tab-close-button { display: none !important; }`);
    } else if (c.tabClose === "hover") {
      chrome.push(`.tabbrowser-tab:not([pinned]):not(:hover) .tab-close-button { display: none !important; }`);
    } else {
      chrome.push(`.tabbrowser-tab:not([pinned]) .tab-close-button { display: flex !important; }`);
    }
  }
  if (has("tabWeight")) {
    chrome.push(`.tabbrowser-tab .tab-label, .tabbrowser-tab[selected] .tab-label { font-weight: ${c.tabWeight} !important; }`);
  }

  // вкладки спрятаны: боковая панель вкладок становится «шторкой» поверх страницы,
  // верхний ряд вкладок сворачивается и появляется при наведении на панель
  if (has("tabsHide")) {
    const V = '#browser > :has(#tabbrowser-tabs[orient="vertical"])';
    const edge = c.tabsHide === "edge";
    chrome.push(`#browser { position: relative !important; }`);
    chrome.push(`:root:not([customizing]) ${V} {
      position: absolute !important; inset-block: 0 !important; inset-inline-start: 0 !important; z-index: 30 !important;
      translate: ${edge ? "calc(-100% + 8px)" : "-100%"} 0; opacity: 0;
      ${edge ? "" : "visibility: hidden;"}
      background-color: var(--fm-frame, var(--toolbox-background-color, Canvas)) !important;
      box-shadow: 10px 0 34px rgb(0 0 0 / .32) !important;
      transition: translate calc(.38s * var(--fm-k, 1)) var(--fm-spring, ease), opacity .2s ease, visibility 0s .38s !important; }`);
    chrome.push(`:root:not([customizing]) ${V}:is(:hover, :focus-within, [fm-open]), :root[fm-tabs-peek] ${V} {
      translate: 0 0; opacity: 1; visibility: visible; transition: translate calc(.38s * var(--fm-k, 1)) var(--fm-spring, ease), opacity .15s ease !important; }`);
    chrome.push(`:root:not([customizing]) #sidebar-launcher-splitter { display: none !important; }`);
    chrome.push(`:root:not([customizing]):not([fm-tabs-peek]) #navigator-toolbox:not(:hover, :focus-within) #TabsToolbar:has(#tabbrowser-tabs:not([orient="vertical"])) { visibility: collapse !important; }`);
  }

  // адресная строка
  if (has("urlHeight")) {
    chrome.push(`#urlbar { --urlbar-min-height: ${px(c.urlHeight)} !important; --urlbar-height: ${px(c.urlHeight)} !important; }`);
    chrome.push(`#urlbar-container { --urlbar-container-height: ${px(c.urlHeight + 8)} !important; }`);
  }
  if (has("urlRadius")) {
    chrome.push(`#urlbar { --urlbar-border-radius: ${px(c.urlRadius)} !important; --toolbarbutton-border-radius: ${px(c.urlRadius)}; }`);
    chrome.push(`#urlbar > :is(#urlbar-background, .urlbar-background), .urlbar > .urlbar-background { border-radius: ${px(c.urlRadius)} !important; }`);
  }
  if (has("urlAlign")) {
    chrome.push(`#urlbar:not([focused], [open]) #urlbar-input, moz-urlbar:not([focused], [open]) .urlbar-input { text-align: ${c.urlAlign} !important; }`);
  }
  if (has("urlBorder")) {
    if (c.urlBorder === "none") {
      chrome.push(`#urlbar > :is(#urlbar-background, .urlbar-background), .urlbar > .urlbar-background { outline: none !important; box-shadow: none !important; }`);
    } else if (c.urlBorder === "line") {
      chrome.push(`#urlbar > :is(#urlbar-background, .urlbar-background), .urlbar > .urlbar-background { outline: 1px solid var(--fm-line, rgb(128 128 128 / .3)) !important; outline-offset: -1px !important; box-shadow: none !important; }`);
      chrome.push(`#urlbar:is([focused], [open]) > :is(#urlbar-background, .urlbar-background) { outline: 1.5px solid var(--fm-accent) !important; }`);
    } else {
      chrome.push(`#urlbar > :is(#urlbar-background, .urlbar-background) { box-shadow: 0 0 18px color-mix(in srgb, var(--fm-accent) 30%, transparent) !important; }`);
    }
  }

  // шрифт
  if (fontStack) {
    chrome.push(`#navigator-toolbox, #sidebar-main, #panel-sidebar-select-box, menupopup, panel, tooltip, .tabbrowser-tab, #urlbar { font-family: ${fontStack} !important; }`);
  }
  if (has("fontSize")) {
    chrome.push(`#navigator-toolbox, menupopup, panel, #sidebar-main { font-size: ${px(c.fontSize)} !important; } .tabbrowser-tab .tab-label, #urlbar-input, .urlbar-input { font-size: ${px(c.fontSize)} !important; }`);
  }

  // показать / скрыть
  const hide = (key, sel) => {
    if (c[key] === false) {
      chrome.push(`${sel} { display: none !important; }`);
    }
  };
  hide("showBookmarks", "#PersonalToolbar");
  hide("showSidebarButton", "#sidebar-button");
  hide("showTabList", "#alltabs-button");
  hide("showNewTabButton", ":is(#new-tab-button, #tabs-newtab-button, #vertical-tabs-newtab-button)");
  hide("showExtensions", "#unified-extensions-button");
  hide("showNowBar", ".fm-nowbar");
  hide("showCallBar", ".fm-callbar");
  hide("showProgress", ".fm-progress");
  if (c.showBookmarks === true) {
    chrome.push(`#PersonalToolbar[collapsed] { visibility: visible !important; }`);
  }

  // ---- новая вкладка
  const CLOCK = ".absolute.top-4.right-4";
  if (has("clockSize")) {
    newtab.push(`${CLOCK} .tabular-nums { font-size: ${px(c.clockSize)} !important; line-height: 1 !important; }`);
  }
  if (has("clockWeight")) {
    newtab.push(`${CLOCK} .tabular-nums { font-weight: ${c.clockWeight} !important; }`);
  }
  if (has("clockFont")) {
    const f = c.clockFont === "ui" ? (fontStack || FONTS.segoe) : CLOCK_FONTS[c.clockFont];
    newtab.push(`${CLOCK}, ${CLOCK} .tabular-nums { font-family: ${f} !important; }`);
  }
  if (has("clockPos")) {
    if (c.clockPos === "hidden") {
      newtab.push(`${CLOCK} { display: none !important; } :root:has(#fm-clock) .outer-wrapper { padding-top: revert !important; }`);
    } else if (c.clockPos === "center") {
      newtab.push(`${CLOCK} { top: 26vh !important; }`);
      newtab.push(`.w-full.min-h-screen.flex.flex-col.justify-center.items-center { padding-top: 40vh !important; } :root:has(#fm-clock) .outer-wrapper { padding-top: 50vh !important; }`);
    } else {
      newtab.push(`${CLOCK} { top: 8vh !important; }`);
    }
  }
  if (c.showDate === false) {
    newtab.push(`${CLOCK} .flex-col.text-right { display: none !important; }`);
  }
  if (has("searchWidth")) {
    newtab.push(`:is(.group.cursor-pointer:has(input[readonly]), .search-wrapper .search-inner-wrapper) { width: ${c.searchWidth}vw !important; max-width: ${c.searchWidth}vw !important; }`);
    newtab.push(`.search-wrapper { width: auto !important; max-width: none !important; }`);
  }
  if (c.tiles === false) {
    newtab.push(`:is(.inline-block.backdrop-blur-sm.p-3, .top-sites, .top-sites-list) { display: none !important; }`);
  }
  if (has("wallBlur") && c.wallBlur > 0) {
    newtab.push(`#fm-wall { filter: blur(${px(c.wallBlur)}); inset: -${px(c.wallBlur * 2)} !important; }`);
  }

  // Всё в слое @layer: у слоя пометки !important сильнее, чем у обычных
  // стилей userChrome.css / userContent.css, поэтому настройки всегда побеждают тему.
  const L = body => `@layer fm-studio {\n${body}\n}`;
  // порядок слоёв: Studio сильнее настроек установщика
  const out = ["/* Redesigned Fox Studio — собрано автоматически */", "@layer fm-studio, fm-settings;"];
  const R = root.length ? `:root { ${root.join(" ")} }` : "";
  // метка: окно браузера проверяет её и понимает, что стили Studio дошли
  out.push(`@-moz-document url("chrome://browser/content/browser.xhtml") {\n${L(R + "\n:root { --fm-studio-ok: 1 !important; }\n" + chrome.join("\n"))}\n}`);
  out.push(`@-moz-document url("about:newtab"), url("about:home"), url-prefix("chrome://noraneko-newtab/") {\n${L(R + "\n" + newtab.join("\n"))}\n}`);
  if (R) {
    // PDF и встроенные страницы тоже берут акцент и скорость анимаций
    out.push(`@-moz-document url-prefix("resource://pdf.js/"), url-prefix("about:"), url-prefix("resource://pdftweaks/"), url-prefix("chrome://fmstudio/") {\n${L(R)}\n}`);
  }
  if (c.square === true) {
    out.push(SQUARE_CHROME.replaceAll("@layer LAYER", "@layer fm-studio"));
    out.push(SQUARE_CONTENT.replaceAll("@layer LAYER", "@layer fm-studio"));
  }
  return out.join("\n\n");
}

/* ---------------- подключение к браузеру ---------------- */
let registered = null;
let started = false;

function sss() {
  return Cc["@mozilla.org/content/style-sheet-service;1"].getService(Ci.nsIStyleSheetService);
}

export function version() {
  // раньше брали из настройки, которую пишет только установщик, — после обновления файлов
  // без переустановки там оставалась старая версия (например, 1.13.0)
  return APP_VERSION;
}

export function readConfig() {
  try {
    return sanitize(JSON.parse(Services.prefs.getStringPref(PREF, "{}")));
  } catch (e) {
    return {};
  }
}

let lastCss = "";
export function currentSheet() {
  return registered ? registered.spec : "";
}
export function hasConfig() {
  return Object.keys(readConfig()).length > 0;
}

function apply() {
  const s = sss();
  if (registered && s.sheetRegistered(registered, s.USER_SHEET)) {
    s.unregisterSheet(registered, s.USER_SHEET);
  }
  registered = null;
  const cfg = readConfig();
  lastCss = Object.keys(cfg).length ? buildCss(cfg) : "";
  // копия собранного CSS — для проверки, что именно применилось
  try {
    const dir = PathUtils.join(Services.dirsvc.get("UChrm", Ci.nsIFile).path, "pdf-tweaks");
    IOUtils.writeUTF8(PathUtils.join(dir, "fm-studio.css"), lastCss || "/* Studio: всё как в теме */").catch(() => {});
  } catch (e) {}
  if (!lastCss) {
    return;
  }
  registered = Services.io.newURI("data:text/css;charset=utf-8," + encodeURIComponent(lastCss));
  s.loadAndRegisterSheet(registered, s.USER_SHEET);
}

/* сохранить настройки (вызывает родительский актор) */
export function save(raw) {
  const cfg = sanitize(raw);
  Services.prefs.setStringPref(PREF, JSON.stringify(cfg));
  // Ctrl+Tab с превью — это настройка самого браузера
  if (cfg.ctrlTabPreview !== undefined) {
    Services.prefs.setBoolPref("browser.ctrlTab.sortByRecentlyUsed", cfg.ctrlTabPreview);
  }
  if (cfg.density !== undefined) {
    Services.prefs.setIntPref("browser.uidensity", { normal: 0, compact: 1, touch: 2 }[cfg.density]);
  }
  if (cfg.showBookmarks !== undefined) {
    Services.prefs.setStringPref("browser.toolbars.bookmarks.visibility", cfg.showBookmarks ? "always" : "never");
  }
  return cfg;
}

export function init() {
  if (started) {
    return;
  }
  started = true;
  // настоящая версия — в настройку (её читают страница Studio и журналы)
  try {
    Services.prefs.setStringPref("floorp.modern.version", APP_VERSION);
  } catch (e) {}
  // 1.13.0–1.13.3: браузер при восстановлении вкладки Studio заполнял все поля
  // значениями по умолчанию (серый #808080, ползунки посередине) — такие настройки сбрасываем
  try {
    const c = readConfig();
    if (c.accent === "#808080" && c.frame === "#808080" && c.ink === "#808080") {
      Services.prefs.setStringPref(PREF, "{}");
    }
  } catch (e) {}
  try {
    apply();
  } catch (e) {
    console.error("[floorp-modern] studio:", e);
  }
  Services.prefs.addObserver(PREF, () => {
    try {
      apply();
    } catch (e) {
      console.error("[floorp-modern] studio:", e);
    }
  });
}
