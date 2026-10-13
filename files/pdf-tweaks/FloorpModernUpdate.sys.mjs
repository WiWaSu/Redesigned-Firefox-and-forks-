/* Redesigned Fox — проверка обновлений.
 *
 * Репозиторий релизов: github.com/WiWaSu/Redesigned-Firefox-and-forks-
 * Где ищем новую версию (по порядку, до первого ответа):
 *  1. latest.json в корне репозитория (ветки main, master):
 *     { "version": "1.19.0", "zip": "v1.19.0.zip", "notes": "notes/v1.19.0.md" }
 *  2. список файлов репозитория: самый новый vX.Y.Z.zip;
 *  3. GitHub Releases (последний релиз).
 * Проверка — не чаще раза в сутки (и по кнопке «Проверить»). Сеть делает окно браузера
 * (его fetch и таймеры), модуль хранит результат и общий для всех окон статус.
 */
import { APP_VERSION } from "resource://pdftweaks/FloorpModernStudio.sys.mjs";

export const REPO = "WiWaSu/Redesigned-Firefox-and-forks-";
export const PAGE = `https://github.com/${REPO}`;
const P = "floorp.modern.update.";
const DAY = 24 * 3600;

/* сравнить версии «1.18.0» и «1.19.2» */
export function cmp(a, b) {
  const pa = String(a).replace(/^v/, "").split(".").map(n => parseInt(n, 10) || 0);
  const pb = String(b).replace(/^v/, "").split(".").map(n => parseInt(n, 10) || 0);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const d = (pa[i] || 0) - (pb[i] || 0);
    if (d) {
      return d > 0 ? 1 : -1;
    }
  }
  return 0;
}
const VER = /^v?(\d{1,3}\.\d{1,3}\.\d{1,3})$/;

export function enabled() {
  try {
    const cfg = JSON.parse(Services.prefs.getStringPref("floorp.modern.studio", "{}"));
    return cfg.checkUpdates !== false;
  } catch (e) {
    return true;
  }
}

/* последний известный результат: { version, zip, notes, page } или null */
export function known() {
  try {
    const r = JSON.parse(Services.prefs.getStringPref(P + "latest", ""));
    if (r && VER.test(r.version) && cmp(r.version, APP_VERSION) > 0) {
      return r;
    }
  } catch (e) {}
  return null;
}

async function getJSON(win, url) {
  const ctrl = new win.AbortController();
  const t = win.setTimeout(() => ctrl.abort(), 8000);
  try {
    const r = await win.fetch(url, { signal: ctrl.signal, cache: "no-store", credentials: "omit", headers: { Accept: "application/json" } });
    if (!r.ok) {
      return null;
    }
    return await r.json();
  } catch (e) {
    return null;
  } finally {
    win.clearTimeout(t);
  }
}

const raw = (branch, path) => `https://raw.githubusercontent.com/${REPO}/${branch}/${path}`;
const blob = (branch, path) => `https://github.com/${REPO}/blob/${branch}/${path}`;

async function lookup(win) {
  // 1) latest.json
  for (const branch of ["main", "master"]) {
    const j = await getJSON(win, raw(branch, "latest.json"));
    if (j && VER.test(String(j.version || ""))) {
      const v = String(j.version).replace(/^v/, "");
      return {
        version: v,
        zip: /^https:\/\//.test(j.zip || "") ? j.zip : `https://github.com/${REPO}/raw/${branch}/${j.zip || `v${v}.zip`}`,
        notes: /^https:\/\//.test(j.notes || "") ? j.notes : blob(branch, j.notes || `notes/v${v}.md`),
        page: PAGE,
        source: "latest.json",
      };
    }
  }
  // 2) самый новый vX.Y.Z.zip в корне
  const list = await getJSON(win, `https://api.github.com/repos/${REPO}/contents/`);
  if (Array.isArray(list)) {
    let best = null;
    for (const f of list) {
      const m = /^v(\d{1,3}\.\d{1,3}\.\d{1,3})\.zip$/.exec(String(f?.name || ""));
      if (m && (!best || cmp(m[1], best.v) > 0)) {
        best = { v: m[1], url: String(f.download_url || "") };
      }
    }
    if (best) {
      return {
        version: best.v,
        zip: /^https:\/\//.test(best.url) ? best.url : PAGE,
        notes: `${PAGE}/blob/HEAD/notes/v${best.v}.md`,
        page: PAGE,
        source: "files",
      };
    }
  }
  // 3) GitHub Releases
  const rel = await getJSON(win, `https://api.github.com/repos/${REPO}/releases/latest`);
  if (rel && VER.test(String(rel.tag_name || ""))) {
    const v = String(rel.tag_name).replace(/^v/, "");
    const asset = (rel.assets || []).find(a => /\.zip$/i.test(a?.name || ""));
    return {
      version: v,
      zip: asset?.browser_download_url || rel.html_url || PAGE,
      notes: rel.html_url || PAGE,
      page: PAGE,
      source: "releases",
    };
  }
  return null;
}

let running = null;
/* проверить. force — без учёта «раз в сутки». Возвращает { latest, newer, error } */
export function check(win, { force = false } = {}) {
  if (running) {
    return running;
  }
  const now = Math.floor(Date.now() / 1000);
  if (!force) {
    if (!enabled()) {
      return Promise.resolve({ latest: null, newer: false, skipped: true });
    }
    let last = 0;
    try {
      last = Services.prefs.getIntPref(P + "lastCheck", 0);
    } catch (e) {}
    if (now - last < DAY) {
      const k = known();
      return Promise.resolve({ latest: k, newer: !!k, cached: true });
    }
  }
  running = (async () => {
    try {
      const r = await lookup(win);
      Services.prefs.setIntPref(P + "lastCheck", now);
      if (!r) {
        return { latest: null, newer: false, error: "нет ответа от GitHub" };
      }
      Services.prefs.setStringPref(P + "latest", JSON.stringify(r));
      return { latest: r, newer: cmp(r.version, APP_VERSION) > 0 };
    } catch (e) {
      return { latest: null, newer: false, error: String(e) };
    } finally {
      running = null;
    }
  })();
  return running;
}

/* «не напоминать об этой версии» */
export function skip(version) {
  Services.prefs.setStringPref(P + "skip", String(version));
}
export function skipped(version) {
  try {
    return Services.prefs.getStringPref(P + "skip", "") === String(version);
  } catch (e) {
    return false;
  }
}

export { APP_VERSION };
