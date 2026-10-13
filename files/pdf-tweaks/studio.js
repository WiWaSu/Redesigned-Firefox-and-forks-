/* Redesigned Fox Studio — страница настроек.
 * Получает текущие настройки от браузера (событие fm-studio-config) и
 * отправляет изменения обратно (fm-studio-save). Применяет их сам браузер. */
import { SCHEMA, PRESETS, sanitize } from "./FloorpModernStudio.sys.mjs";
import { THEMES } from "./FloorpModernThemes.sys.mjs";

const $ = (sel, root = document) => root.querySelector(sel);
const mk = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
};
// значения по умолчанию для переключателей (null = как в теме)
const BOOL_DEFAULT = { ctrlTabPreview: false, square: false };

let cfg = {};
let connected = false;
const controls = new Map();

/* ---------- связь с браузером ----------
   Открыта как chrome://fmstudio/ — у страницы есть права браузера, пишем настройки сами.
   Открыта как resource:// — через события, их передаёт актор FloorpPdfTweaks. */
let direct = null;
let themesApi = null;
try {
  if (typeof ChromeUtils !== "undefined") {
    direct = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernStudio.sys.mjs");
    themesApi = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernThemes.sys.mjs");
  }
} catch {
  direct = null;
  themesApi = null;
}
let theme = "";
let saveTimer = 0;
function save(now = false) {
  clearTimeout(saveTimer);
  const send = () => {
    if (direct) {
      try {
        direct.save(sanitize(cfg));
        return;
      } catch (e) {
        console.error(e);
      }
    }
    window.dispatchEvent(new CustomEvent("fm-studio-save", { detail: JSON.stringify(sanitize(cfg)) }));
  };
  if (now) send();
  else saveTimer = setTimeout(send, 120);
}
window.addEventListener("fm-studio-config", e => {
  connected = true;
  try {
    const d = JSON.parse(e.detail || "{}");
    cfg = sanitize(d.config || {});
    if (d.version) $("#ver").textContent = "· версия " + d.version;
    if (d.theme) theme = d.theme;
    markTheme();
  } catch {
    cfg = {};
  }
  document.documentElement.toggleAttribute("connected", true);
  refreshAll();
});

function toast(text) {
  const t = $("#toast");
  t.textContent = text;
  t.hidden = false;
  t.classList.remove("out");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => {
    t.classList.add("out");
    setTimeout(() => (t.hidden = true), 300);
  }, 1800);
}

function set(key, value) {
  if (value === null || value === undefined || value === "") delete cfg[key];
  else cfg[key] = value;
  refresh(key);
  save();
}

/* ---------- элементы управления ---------- */
function row(it) {
  const r = mk("div", "row");
  r.dataset.key = it.key;
  const head = mk("div", "row-head");
  const lab = mk("div", "label", it.label);
  head.append(lab);
  const reset = mk("button", "reset", "↺");
  reset.title = "Как в теме";
  reset.addEventListener("click", () => set(it.key, null));
  head.append(reset);
  r.append(head);
  if (it.hint) r.append(mk("div", "hint", it.hint));
  return r;
}

// Firefox при восстановлении вкладки сам заполняет поля формы и шлёт события —
// принимаем изменения только от элементов, которых пользователь реально касался
function touchable(el) {
  el.setAttribute("autocomplete", "off");
  const mark = () => (el.dataset.touched = "1");
  el.addEventListener("pointerdown", mark);
  el.addEventListener("keydown", mark);
  return () => el.dataset.touched === "1";
}

function buildControl(it) {
  const r = row(it);
  let update;
  if (it.type === "color") {
    const wrap = mk("div", "color");
    const input = mk("input");
    input.type = "color";
    const hex = mk("input", "hex");
    hex.maxLength = 7;
    hex.spellcheck = false;
    const theme = mk("span", "badge", "тема");
    const tColor = touchable(input);
    const tHex = touchable(hex);
    input.addEventListener("input", () => tColor() && set(it.key, input.value.toUpperCase()));
    hex.addEventListener("change", () => {
      if (tHex() && /^#[0-9a-fA-F]{6}$/.test(hex.value)) set(it.key, hex.value.toUpperCase());
    });
    wrap.append(input, hex, theme);
    r.append(wrap);
    update = v => {
      input.value = v || "#808080";
      hex.value = v || "";
      hex.placeholder = "#RRGGBB";
      theme.hidden = !!v;
    };
  } else if (it.type === "range") {
    const wrap = mk("div", "range");
    const input = mk("input");
    input.type = "range";
    input.min = it.min;
    input.max = it.max;
    input.step = it.step;
    const out = mk("output");
    const tRange = touchable(input);
    input.addEventListener("input", () => {
      if (!tRange()) return;
      out.textContent = input.value + (it.unit || "");
      set(it.key, Number(input.value));
    });
    wrap.append(input, out);
    r.append(wrap);
    update = v => {
      input.value = v ?? (it.min + it.max) / 2;
      input.toggleAttribute("unset", v === undefined);
      out.textContent = v === undefined ? "тема" : v + (it.unit || "");
    };
  } else if (it.type === "select") {
    const seg = mk("div", "seg");
    for (const [val, name] of it.options) {
      const b = mk("button", "", name);
      b.dataset.v = val;
      b.addEventListener("click", () => set(it.key, cfg[it.key] === val ? null : val));
      seg.append(b);
    }
    r.append(seg);
    update = v => {
      for (const b of seg.children) b.toggleAttribute("on", b.dataset.v === v);
    };
  } else if (it.type === "cards") {
    const grid = mk("div", "cards");
    for (const [val, name, desc] of it.options) {
      const c = mk("button", "card");
      c.dataset.v = val;
      const pv = mk("div", `pv pv-${it.key} pv-${val}`);
      // мини-превью: меню с тремя пунктами или три карточки вкладок
      for (let i = 0; i < 3; i++) pv.append(mk("i", i === 1 ? "sel" : ""));
      c.append(pv, mk("b", "", name), mk("small", "", desc));
      c.addEventListener("click", () => set(it.key, cfg[it.key] === val ? null : val));
      grid.append(c);
    }
    r.append(grid);
    update = v => {
      for (const b of grid.children) b.toggleAttribute("on", b.dataset.v === v);
    };
  } else if (it.type === "bool") {
    const sw = mk("button", "switch");
    sw.setAttribute("role", "switch");
    sw.addEventListener("click", () => {
      const cur = cfg[it.key] ?? BOOL_DEFAULT[it.key] ?? true;
      set(it.key, !cur);
    });
    r.querySelector(".row-head").insertBefore(sw, r.querySelector(".reset"));
    r.classList.add("row-bool");
    update = v => {
      const on = v ?? BOOL_DEFAULT[it.key] ?? true;
      sw.setAttribute("aria-checked", String(on));
      sw.toggleAttribute("unset", v === undefined);
    };
  } else if (it.type === "text") {
    const input = mk("input", "text");
    input.placeholder = "например, JetBrains Mono";
    const tText = touchable(input);
    input.addEventListener("change", () => tText() && set(it.key, input.value.trim() || null));
    r.append(input);
    update = v => {
      input.value = v || "";
    };
  }
  controls.set(it.key, { row: r, update });
  return r;
}

function refresh(key) {
  const c = controls.get(key);
  if (c) {
    c.update(cfg[key]);
    c.row.toggleAttribute("changed", cfg[key] !== undefined);
  }
  // свой шрифт виден только при выборе «Свой…»
  const fc = controls.get("fontCustom");
  if (fc) fc.row.hidden = cfg.font !== "custom";
}
function refreshAll() {
  for (const k of controls.keys()) refresh(k);
}

/* ---------- страница ---------- */
const nav = $("#nav");
const groups = $("#groups");
for (const g of SCHEMA) {
  const sec = mk("section", "group");
  sec.id = "g-" + g.group;
  sec.append(mk("h2", "", g.title));
  const box = mk("div", "box");
  for (const it of g.items) box.append(buildControl(it));
  sec.append(box);
  groups.append(sec);
  const a = mk("a", "", g.title);
  a.href = "#g-" + g.group;
  nav.append(a);
}
// подсветка раздела в меню слева
const io = new IntersectionObserver(entries => {
  for (const en of entries) {
    if (en.isIntersecting) {
      for (const a of nav.children) a.toggleAttribute("on", a.getAttribute("href") === "#" + en.target.id);
    }
  }
}, { rootMargin: "-40% 0px -55% 0px" });
for (const s of groups.children) io.observe(s);

/* ---------- тема: меняется сразу во всём браузере ---------- */
const themeRow = $("#themes");
function markTheme() {
  for (const b of themeRow.children) b.toggleAttribute("on", b.dataset.id === theme);
}
for (const [id, name, sw] of THEMES) {
  const b = mk("button", "theme");
  b.dataset.id = id;
  const pv = mk("span", "theme-pv");
  pv.style.setProperty("--a", sw[0]);
  pv.style.setProperty("--b", sw[1]);
  pv.style.setProperty("--c", sw[2]);
  pv.style.setProperty("--d", sw[3]);
  pv.append(mk("i"), mk("i"), mk("i"));
  b.append(pv, mk("span", "theme-name", name));
  b.addEventListener("click", async () => {
    theme = id;
    markTheme();
    try {
      if (themesApi) await themesApi.setTheme(id);
      else window.dispatchEvent(new CustomEvent("fm-theme-set", { detail: id }));
      toast(`Тема «${name}»`);
    } catch (e) {
      console.error(e);
      toast("Не получилось сменить тему");
    }
  });
  themeRow.append(b);
}

const presetRow = $("#presets");
for (const [id, name, values] of PRESETS) {
  const b = mk("button", `preset preset-${id}`);
  b.append(mk("span", "dot"), mk("span", "", name));
  b.addEventListener("click", () => {
    cfg = sanitize({ ...cfg, ...values });
    refreshAll();
    save(true);
    toast(`Набор «${name}» применён`);
  });
  presetRow.append(b);
}

$("#reset").addEventListener("click", () => {
  cfg = {};
  refreshAll();
  save(true);
  toast("Всё как в теме");
});
$("#export").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(sanitize(cfg), null, 2)], { type: "application/json" });
  const a = mk("a");
  a.href = URL.createObjectURL(blob);
  a.download = "floorp-modern-studio.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
});
$("#import").addEventListener("click", () => {
  const input = mk("input");
  input.type = "file";
  input.accept = ".json,application/json";
  input.addEventListener("change", async () => {
    try {
      const text = await input.files[0].text();
      cfg = sanitize(JSON.parse(text));
      refreshAll();
      save(true);
      toast("Настройки загружены");
    } catch {
      toast("Не получилось прочитать файл");
    }
  });
  input.click();
});

refreshAll();
if (direct) {
  connected = true;
  cfg = sanitize(direct.readConfig());
  try {
    theme = themesApi.current();
  } catch {}
  markTheme();
  try {
    $("#ver").textContent = "· версия " + direct.version();
    const up = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernUpdate.sys.mjs");
    const k = up.known();
    if (k) {
      const a = mk("a", "upd", ` · доступна ${k.version}`);
      a.href = k.notes;
      a.target = "_blank";
      $("#ver").append(a);
    }
  } catch {}
  document.documentElement.toggleAttribute("connected", true);
  refreshAll();
}
setTimeout(() => {
  if (!connected) document.documentElement.toggleAttribute("offline", true);
}, 1500);
