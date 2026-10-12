/* Floorp PDF tweaks — родительская часть.
 *  1. Сохраняет тему, выбранную в просмотрщике PDF.
 *  2. Запасной загрузчик: подключает floorp-modern.uc.js во все окна браузера
 *     (если основной загрузчик этого не сделал) и пишет журнал fm-boot.json.
 */

const ALLOWED = {
  ui: ["auto", "light", "dark"],
  page: ["auto", "paper", "sepia", "night"],
};

let booted = false;
const bootLog = [];

function logDir() {
  try {
    return PathUtils.join(Services.dirsvc.get("UChrm", Ci.nsIFile).path, "pdf-tweaks");
  } catch (e) {
    return null;
  }
}

function writeLog() {
  const dir = logDir();
  if (dir) {
    IOUtils.writeJSON(PathUtils.join(dir, "fm-boot.json"), bootLog).catch(() => {});
  }
}

function loadInto(win) {
  try {
    if (!win || win.closed || win.location?.href !== "chrome://browser/content/browser.xhtml") {
      return;
    }
    if (win.__floorpModern) {
      bootLog.push({ t: new Date().toISOString(), msg: "окно уже со скриптом (основной загрузчик сработал)" });
      return;
    }
    Services.scriptloader.loadSubScriptWithOptions("resource://pdftweaks/floorp-modern.uc.js", {
      target: win,
      ignoreCache: true,
    });
    bootLog.push({ t: new Date().toISOString(), msg: "скрипт подключён запасным загрузчиком" });
  } catch (e) {
    bootLog.push({ t: new Date().toISOString(), msg: "ОШИБКА: " + e, stack: String(e?.stack || "") });
  }
  writeLog();
}

export function boot() {
  if (booted) {
    return;
  }
  booted = true;
  bootLog.push({ t: new Date().toISOString(), msg: "запасной загрузчик запущен" });
  try {
    for (const win of Services.wm.getEnumerator("navigator:browser")) {
      if (win.gBrowserInit?.delayedStartupFinished) {
        loadInto(win);
      }
    }
    Services.obs.addObserver(subject => loadInto(subject), "browser-delayed-startup-finished");
  } catch (e) {
    bootLog.push({ t: new Date().toISOString(), msg: "ОШИБКА запуска: " + e });
  }
  writeLog();
}

export const STUDIO_URL = "chrome://fmstudio/content/studio.html";
const STUDIO_FALLBACK = "resource://pdftweaks/studio.html";
function studioRegistered() {
  try {
    Cc["@mozilla.org/chrome/chrome-registry;1"].getService(Ci.nsIChromeRegistry)
      .convertChromeURL(Services.io.newURI(STUDIO_URL));
    return true;
  } catch (e) {
    return false;
  }
}
export function openStudio(win) {
  if (!win) {
    return;
  }
  const url = studioRegistered() ? STUDIO_URL : STUDIO_FALLBACK;
  const principal = Services.scriptSecurityManager.getSystemPrincipal();
  // уже открыта — переключаемся и открываем заново (вдруг там была ошибка)
  for (const tab of win.gBrowser.tabs) {
    const spec = tab.linkedBrowser?.currentURI?.spec || "";
    if (spec.startsWith(STUDIO_URL) || spec.startsWith(STUDIO_FALLBACK)) {
      win.gBrowser.selectedTab = tab;
      tab.linkedBrowser.loadURI(Services.io.newURI(url), { triggeringPrincipal: principal });
      return;
    }
  }
  const tab = win.gBrowser.addTrustedTab(url, { triggeringPrincipal: principal });
  win.gBrowser.selectedTab = tab;
}

const WALL_IDS = ["theme", "custom", "aurora", "iris", "sunset", "ocean", "forest", "night", "rose", "graphite", "bloom", "dune"];
const WALL_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif", "image/avif", "image/bmp"];

export class FloorpPdfTweaksParent extends JSWindowActorParent {
  // обои разрешено менять только со страницы новой вкладки
  #fromNewtab() {
    try {
      const spec = this.manager.documentURI?.spec || "";
      return /^(about:(newtab|home)|chrome:\/\/noraneko-newtab\/)/.test(spec);
    } catch (e) {
      return false;
    }
  }

  async #wallpaper(msg) {
    if (!this.#fromNewtab()) {
      return null;
    }
    const dir = logDir();
    if (!dir) {
      return null;
    }
    const file = PathUtils.join(dir, "fm-wallpaper.img");
    if (msg.name === "PdfTweaks:wall-get") {
      try {
        const bytes = await IOUtils.read(file);
        const type = Services.prefs.getStringPref("floorp.modern.wallpaper.type", "image/jpeg");
        return { type: WALL_TYPES.includes(type) ? type : "image/jpeg", bytes };
      } catch (e) {
        return null;
      }
    }
    const d = msg.data || {};
    if (typeof d.dim === "number" && d.dim >= 0 && d.dim <= 70) {
      Services.prefs.setIntPref("floorp.modern.wallpaper.dim", Math.round(d.dim));
    }
    if (d.id === "custom") {
      const bytes = d.bytes;
      if (!(bytes instanceof Uint8Array) || !bytes.length || bytes.length > 15 * 1024 * 1024) {
        return null;
      }
      await IOUtils.write(file, bytes);
      Services.prefs.setStringPref("floorp.modern.wallpaper.type", WALL_TYPES.includes(d.type) ? d.type : "image/jpeg");
      Services.prefs.setIntPref("floorp.modern.wallpaper.rev", Services.prefs.getIntPref("floorp.modern.wallpaper.rev", 0) + 1);
      Services.prefs.setStringPref("floorp.modern.wallpaper", "custom");
    } else if (WALL_IDS.includes(d.id)) {
      Services.prefs.setStringPref("floorp.modern.wallpaper", d.id);
    }
    return null;
  }

  receiveMessage(msg) {
    if (msg.name === "PdfTweaks:boot") {
      boot();
      return;
    }
    if (msg.name === "PdfTweaks:studio-save") {
      // принимаем только со страницы Studio
      const spec = this.manager.documentURI?.spec || "";
      if (!/^(resource:\/\/pdftweaks\/|chrome:\/\/fmstudio\/content\/)studio\.html/.test(spec)) {
        return null;
      }
      try {
        const studio = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernStudio.sys.mjs");
        studio.save(JSON.parse(String(msg.data || "{}")));
      } catch (e) {
        bootLog.push({ t: new Date().toISOString(), msg: "Studio: ОШИБКА " + e });
        writeLog();
      }
      return null;
    }
    if (msg.name === "PdfTweaks:studio-open") {
      if (this.#fromNewtab()) {
        openStudio(this.browsingContext.topChromeWindow);
      }
      return null;
    }
    if (msg.name === "PdfTweaks:wall-get" || msg.name === "PdfTweaks:wall-set") {
      return this.#wallpaper(msg);
    }
    if (msg.name === "PdfTweaks:note") {
      // короткие заметки от страниц (например, «часы на новой вкладке поставлены»)
      const text = String(msg.data || "").slice(0, 200);
      if (text && bootLog.length < 60) {
        bootLog.push({ t: new Date().toISOString(), msg: text });
        writeLog();
      }
      return;
    }
    if (msg.name === "PdfTweaks:bookmarks") {
      // закладки страниц: { url: [{p, note, t}] }, не больше 150 файлов и 300 закладок в файле
      const { url, list } = msg.data || {};
      if (typeof url !== "string" || !url || url.length > 2000 || !Array.isArray(list)) {
        return;
      }
      let map = {};
      try {
        map = JSON.parse(Services.prefs.getStringPref("floorp.pdftweaks.bookmarks", "{}")) || {};
      } catch (e) {}
      const clean = list
        .filter(b => b && Number(b.p) > 0)
        .slice(0, 300)
        .map(b => ({ p: Math.floor(Number(b.p)), note: String(b.note || "").slice(0, 80), t: Number(b.t) || Date.now() }));
      if (clean.length) {
        map[url] = clean;
      } else {
        delete map[url];
      }
      const keys = Object.keys(map);
      if (keys.length > 150) {
        const last = k => Math.max(0, ...map[k].map(b => b.t || 0));
        keys.sort((a, b) => last(a) - last(b));
        for (const k of keys.slice(0, keys.length - 150)) {
          delete map[k];
        }
      }
      Services.prefs.setStringPref("floorp.pdftweaks.bookmarks", JSON.stringify(map));
      return;
    }
    if (msg.name === "PdfTweaks:page") {
      // запоминаем страницу для файла (последние 150 файлов)
      const { url, page } = msg.data || {};
      if (typeof url !== "string" || !url || url.length > 2000 || !(page > 0)) {
        return;
      }
      let map = {};
      try {
        map = JSON.parse(Services.prefs.getStringPref("floorp.pdftweaks.pages", "{}")) || {};
      } catch (e) {}
      map[url] = { p: Math.floor(page), t: Date.now() };
      const keys = Object.keys(map);
      if (keys.length > 150) {
        keys.sort((a, b) => (map[a].t || 0) - (map[b].t || 0));
        for (const k of keys.slice(0, keys.length - 150)) {
          delete map[k];
        }
      }
      Services.prefs.setStringPref("floorp.pdftweaks.pages", JSON.stringify(map));
      return;
    }
    if (msg.name !== "PdfTweaks:save") {
      return;
    }
    const { ui, page } = msg.data || {};
    if (ALLOWED.ui.includes(ui)) {
      Services.prefs.setStringPref("floorp.pdftweaks.ui", ui);
    }
    if (ALLOWED.page.includes(page)) {
      Services.prefs.setStringPref("floorp.pdftweaks.page", page);
    }
  }
}

export class FloorpModernNTParent extends FloorpPdfTweaksParent {}
