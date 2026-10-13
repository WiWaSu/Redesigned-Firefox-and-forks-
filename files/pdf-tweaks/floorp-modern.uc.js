/* Redesigned Fox (бывш. Floorp Modern) — новые функции окна браузера.
 * Загружается в каждое окно Floorp загрузчиком из папки программы (config.js).
 *
 *  1. Полоска загрузки страницы под панелью (цвет акцента).
 *  2. Всплывающие уведомления в стиле One UI («тосты»).
 *  3. Alt+Shift+C — скопировать адрес страницы.
 *  4. Уведомление о завершённой загрузке файла.
 *  5. Кнопка быстрой смены темы: Авто / Светлая / Тёмная.
 *  6. «Now Bar»: музыка играет в другой вкладке — плашка внизу с паузой и звуком.
 *  7. Уведомления о масштабе страницы и о выключенном звуке вкладки.
 *  8. Alt+Shift+D — закрыть повторяющиеся вкладки.
 *  9. Alt+Shift+Z — режим фокуса (прячет закладки и боковые панели).
 * 10. Плашка звонка: звонок в другой вкладке, микрофон / камера (Alt+Shift+M).
 */
(function () {
  "use strict";
  const win = window;
  const doc = document;
  if (win.__floorpModern) {
    return;
  }
  win.__floorpModern = true;

  const HTML = "http://www.w3.org/1999/xhtml";
  const el = (tag, cls) => {
    const e = doc.createElementNS(HTML, tag);
    if (cls) {
      e.className = cls;
    }
    return e;
  };
  const onUnload = [];

  /* журнал: ошибки пишутся в pdf-tweaks/fm-log.json, чтобы их можно было прочитать */
  const LOG = [];
  const logDir = (() => {
    try {
      return PathUtils.join(Services.dirsvc.get("UChrm", Ci.nsIFile).path, "pdf-tweaks");
    } catch (e) {
      return null;
    }
  })();
  let logTimer = 0;
  const log = (what, err) => {
    LOG.push({ t: new Date().toISOString(), what, err: err ? String(err && err.stack || err) : null });
    if (!logDir) return;
    win.clearTimeout(logTimer);
    logTimer = win.setTimeout(() => {
      IOUtils.writeJSON(PathUtils.join(logDir, "fm-log.json"), LOG).catch(() => {});
    }, 500);
  };
  log("скрипт загружен в окно");
  const safe = (name, fn) => {
    try {
      fn();
      log(name + ": ok");
    } catch (e) {
      log(name + ": ОШИБКА", e);
    }
  };
  win.addEventListener("unload", () => onUnload.forEach(f => {
    try { f(); } catch (e) {}
  }), { once: true });

  /* ------------------------------ тосты ------------------------------ */
  const host = el("div", "fm-toasts");
  try {
    (doc.getElementById("browser") || doc.documentElement).append(host);
    log("toasts: ok");
  } catch (e) {
    log("toasts: ОШИБКА", e);
  }

  function toast(text, kind = "info") {
    const t = el("div", "fm-toast");
    t.dataset.kind = kind;
    const dot = el("span", "fm-toast-dot");
    const label = el("span", "fm-toast-text");
    label.textContent = text;
    t.append(dot, label);
    host.append(t);
    win.requestAnimationFrame(() => t.classList.add("fm-in"));
    win.setTimeout(() => {
      t.classList.remove("fm-in");
      t.classList.add("fm-out");
      win.setTimeout(() => t.remove(), 300);
    }, 2400);
  }
  win.FloorpModernToast = toast;

  safe("progress bar", () => {
    /* ----------------------- полоска загрузки ------------------------- */
    const bar = el("div", "fm-progress");
    const fill = el("div", "fm-progress-fill");
    bar.append(fill);
    const toolbox = doc.getElementById("navigator-toolbox");
    if (toolbox) {
      toolbox.append(bar);
    }
    let hideTimer = 0;
    const setProgress = value => {
      win.clearTimeout(hideTimer);
      bar.classList.add("fm-active");
      fill.style.transform = `scaleX(${Math.max(0.04, Math.min(1, value))})`;
      if (value >= 1) {
        hideTimer = win.setTimeout(() => {
          bar.classList.remove("fm-active");
          hideTimer = win.setTimeout(() => (fill.style.transform = "scaleX(0)"), 250);
        }, 350);
      }
    };
    const progressListener = {
      QueryInterface: ChromeUtils.generateQI(["nsIWebProgressListener", "nsISupportsWeakReference"]),
      onStateChange(webProgress, request, flags) {
        if (!webProgress?.isTopLevel) {
          return;
        }
        const WPL = Ci.nsIWebProgressListener;
        if (flags & WPL.STATE_IS_NETWORK) {
          if (flags & WPL.STATE_START) {
            setProgress(0.08);
          } else if (flags & WPL.STATE_STOP) {
            setProgress(1);
          }
        }
      },
      onProgressChange(webProgress, request, curSelf, maxSelf, curTotal, maxTotal) {
        if (webProgress?.isTopLevel && maxTotal > 0) {
          setProgress(0.08 + 0.87 * (curTotal / maxTotal));
        }
      },
      onLocationChange() {},
      onStatusChange() {},
      onSecurityChange() {},
      onContentBlockingEvent() {},
    };
    if (win.gBrowser) {
      win.gBrowser.addProgressListener(progressListener);
      onUnload.push(() => win.gBrowser.removeProgressListener(progressListener));
      win.gBrowser.tabContainer.addEventListener("TabSelect", () => {
        const busy = win.gBrowser.selectedTab.hasAttribute("busy");
        if (!busy) {
          win.clearTimeout(hideTimer);
          bar.classList.remove("fm-active");
          fill.style.transform = "scaleX(0)";
        }
      });
    }

  });
  safe("copy url", () => {
    /* -------------------- Alt+Shift+C: копировать адрес ------------------- */
    win.addEventListener("keydown", e => {
      if (e.altKey && e.shiftKey && !e.ctrlKey && !e.metaKey && e.code === "KeyC") {
        e.preventDefault();
        e.stopPropagation();
        try {
          const uri = win.gBrowser.currentURI;
          const url = uri?.displaySpec || uri?.spec;
          if (url) {
            Cc["@mozilla.org/widget/clipboardhelper;1"]
              .getService(Ci.nsIClipboardHelper)
              .copyString(url);
            toast("Ссылка скопирована", "ok");
          }
        } catch (err) {
          toast("Не получилось скопировать ссылку", "warn");
        }
      }
    }, true);

  });
  safe("download toast", () => {
    /* -------------------- уведомление о загрузке файла -------------------- */
    (async () => {
      try {
        const { Downloads } = ChromeUtils.importESModule("resource://gre/modules/Downloads.sys.mjs");
        const list = await Downloads.getList(Downloads.ALL);
        const done = new WeakSet();
        const view = {
          onDownloadChanged(d) {
            if (!d.succeeded || done.has(d)) {
              return;
            }
            done.add(d);
            const topWin = Services.wm.getMostRecentWindow("navigator:browser");
            if (topWin !== win) {
              return;
            }
            const name = (d.target?.path || "").split(/[\\/]/).pop() || "файл";
            toast(`Загружено: ${name}`, "ok");
          },
          onDownloadAdded(d) {
            if (d.succeeded) {
              done.add(d);
            }
          },
        };
        await list.addView(view);
        onUnload.push(() => list.removeView(view));
      } catch (e) {
        console.error("[floorp-modern] downloads:", e);
      }
    })();

  });
  safe("theme button", () => {
    /* ---------------------- кнопка смены темы ---------------------- */
    const THEME_PREFS = ["browser.theme.toolbar-theme", "browser.theme.content-theme"];
    // 0 = тёмная, 1 = светлая, 2 = как в системе
    const ORDER = [2, 1, 0];
    const NAMES = { 0: "Тёмная", 1: "Светлая", 2: "Авто" };
    const currentTheme = () => {
      try {
        return Services.prefs.getIntPref(THEME_PREFS[0], 2);
      } catch (e) {
        return 2;
      }
    };
    const CustomizableUI = win.CustomizableUI;
    const WIDGET = "fm-theme-button";
    if (CustomizableUI.getWidget(WIDGET)?.provider !== CustomizableUI.PROVIDER_API) {
      try {
        CustomizableUI.createWidget({
          id: WIDGET,
          type: "button",
          defaultArea: CustomizableUI.AREA_NAVBAR,
          label: "Тема",
          tooltiptext: "Тема: Авто / Светлая / Тёмная",
          onCreated(node) {
            node.setAttribute("fm-theme", String(currentTheme()));
          },
          onCommand(event) {
            const now = currentTheme();
            const next = ORDER[(ORDER.indexOf(now) + 1) % ORDER.length];
            for (const p of THEME_PREFS) {
              Services.prefs.setIntPref(p, next);
            }
            const w = event.target.ownerGlobal;
            w.FloorpModernToast?.(`Тема: ${NAMES[next]}`, "info");
          },
        });
      } catch (e) {
        // виджет уже создан в другом окне
      }
    }
    const syncThemeButton = () => {
      const node = doc.getElementById(WIDGET);
      if (node) {
        node.setAttribute("fm-theme", String(currentTheme()));
      }
    };
    const prefObserver = { observe: syncThemeButton };
    Services.prefs.addObserver(THEME_PREFS[0], prefObserver);
    onUnload.push(() => Services.prefs.removeObserver(THEME_PREFS[0], prefObserver));
    syncThemeButton();

  });
  safe("studio", () => {
    /* ------- Redesigned Fox Studio: тонкая настройка дизайна -------
       Кнопка «Дизайн» на панели, пункт в меню ☰ и Alt+Shift+S. */
    const studio = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernStudio.sys.mjs");
    studio.init();
    // проверяем, что стили Studio дошли до этого окна; если нет — подключаем их прямо к окну
    let windowSheet = "";
    const verify = () => {
      win.setTimeout(() => {
        try {
          const wu = win.windowUtils;
          if (windowSheet) {
            try {
              wu.removeSheetUsingURIString(windowSheet, wu.USER_SHEET);
            } catch (e) {}
            windowSheet = "";
          }
          if (!studio.hasConfig()) {
            return;
          }
          const ok = win.getComputedStyle(doc.documentElement).getPropertyValue("--fm-studio-ok").trim() === "1";
          if (!ok) {
            const spec = studio.currentSheet();
            if (spec) {
              wu.loadSheetUsingURIString(spec, wu.USER_SHEET);
              windowSheet = spec;
              const ok2 = win.getComputedStyle(doc.documentElement).getPropertyValue("--fm-studio-ok").trim() === "1";
              log("studio: стили подключены к окну напрямую, " + (ok2 ? "работает" : "НЕ работает"));
            }
          }
        } catch (e) {
          log("studio: проверка стилей", e);
        }
      }, 250);
    };
    const studioObs = { observe: verify };
    Services.prefs.addObserver("floorp.modern.studio", studioObs);
    onUnload.push(() => Services.prefs.removeObserver("floorp.modern.studio", studioObs));
    verify();
    // адрес chrome://fmstudio/ для страницы настроек (страница браузера с полными правами)
    try {
      Cc["@mozilla.org/chrome/chrome-registry;1"].getService(Ci.nsIChromeRegistry)
        .convertChromeURL(Services.io.newURI("chrome://fmstudio/content/studio.html"));
    } catch (e) {
      try {
        const manifest = Services.dirsvc.get("UChrm", Ci.nsIFile);
        manifest.append("pdf-tweaks");
        manifest.append("chrome.manifest");
        Components.manager.QueryInterface(Ci.nsIComponentRegistrar).autoRegister(manifest);
      } catch (e2) {
        log("studio: chrome:// не зарегистрирован: " + e2, e2);
      }
    }
    // второй актор: заходит и на страницы браузера (новая вкладка Floorp — chrome://noraneko-newtab)
    try {
      ChromeUtils.registerWindowActor("FloorpModernNT", {
        parent: { esModuleURI: "resource://pdftweaks/FloorpPdfTweaksParent.sys.mjs" },
        child: {
          esModuleURI: "resource://pdftweaks/FloorpPdfTweaksChild.sys.mjs",
          events: { DOMContentLoaded: {} },
        },
        includeChrome: true,
        allFrames: true,
      });
    } catch (e) {
      // уже зарегистрирован другим окном
      if (!String(e).includes("NotSupportedError") && !String(e).includes("already")) {
        log("newtab actor", e);
      }
    }
    const open = w => {
      try {
        const how = ChromeUtils.importESModule("resource://pdftweaks/FloorpPdfTweaksParent.sys.mjs").openStudio(w);
        log("studio: вкладка настроек — " + how);
      } catch (e) {
        log("studio open: ОШИБКА", e);
        try {
          const t = w.gBrowser.addTrustedTab("resource://pdftweaks/studio.html", {
            triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(),
          });
          w.gBrowser.selectedTab = t;
        } catch (e2) {
          log("studio open (запасной путь): ОШИБКА", e2);
          w.FloorpModernToast?.("Не получилось открыть настройки: " + e2, "warn");
        }
      }
    };
    let lastOpen = 0;
    const openOnce = w => {
      if (Date.now() - lastOpen < 600) {
        return;
      }
      lastOpen = Date.now();
      log("studio: открываю настройки");
      open(w);
    };

    /* ---------- темы: смена прямо в браузере ---------- */
    let themes = null;
    try {
      themes = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernThemes.sys.mjs");
      themes.init();
      const syncAttr = () => doc.documentElement.setAttribute("fm-theme", themes.current());
      syncAttr();
      const tObs = { observe: syncAttr };
      Services.prefs.addObserver("floorp.modern.theme", tObs);
      onUnload.push(() => Services.prefs.removeObserver("floorp.modern.theme", tObs));
      log("темы: текущая " + themes.current());
    } catch (e) {
      log("темы: ОШИБКА", e);
    }

    /* ---------- быстрая панель по кнопке «Дизайн» ---------- */
    const QP_CSS = `
      #fm-quick-panel { --arrowpanel-padding: 0; }
      #fm-quick-panel .fm-qp { display: flex; flex-direction: column; gap: 12px; width: 344px; padding: 14px; box-sizing: border-box;
        font: menu; font-size: 13px; color: var(--fm-ink, var(--arrowpanel-color, CanvasText)); }
      #fm-quick-panel .fm-qp-head { display: flex; align-items: center; gap: 8px; }
      #fm-quick-panel .fm-qp-title { font-weight: 700; font-size: 15px; flex: 1; }
      #fm-quick-panel .fm-qp-cap { font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; opacity: .6; margin: 2px 2px -4px; }
      #fm-quick-panel .fm-qp-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
      #fm-quick-panel .fm-qp-theme { all: unset; display: flex; flex-direction: column; gap: 5px; padding: 5px; border-radius: 12px; cursor: pointer;
        border: 1.5px solid transparent; transition: scale calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease), background-color .2s, border-color .2s; }
      #fm-quick-panel .fm-qp-theme:hover { background: var(--fm-hover, rgb(128 128 128 / .12)); scale: 1.04; }
      #fm-quick-panel .fm-qp-theme:active { scale: .95; }
      #fm-quick-panel .fm-qp-theme[on] { border-color: var(--fm-accent, AccentColor); background: var(--fm-soft, rgb(128 128 128 / .12)); }
      #fm-quick-panel .fm-qp-pv { position: relative; height: 42px; border-radius: 8px; overflow: hidden; background: var(--a);
        box-shadow: inset 0 0 0 1px rgb(128 128 128 / .25); }
      #fm-quick-panel .fm-qp-pv > span { position: absolute; display: block; }
      #fm-quick-panel .fm-qp-pv > span:nth-child(1) { inset: 5px 5px auto 5px; height: 8px; border-radius: 4px; background: var(--b); }
      #fm-quick-panel .fm-qp-pv > span:nth-child(2) { inset: 17px 5px 5px 5px; border-radius: 5px; background: var(--b); opacity: .7; }
      #fm-quick-panel .fm-qp-pv > span:nth-child(3) { left: 10px; bottom: 9px; width: 22px; height: 6px; border-radius: 3px; background: var(--c); }
      #fm-quick-panel .fm-qp-name { font-size: 11.5px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-inline: 2px; }
      #fm-quick-panel .fm-qp-row { display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 12px;
        background: var(--fm-hover, rgb(128 128 128 / .1)); cursor: pointer; }
      #fm-quick-panel .fm-qp-row > span:first-child { flex: 1; font-weight: 600; }
      #fm-quick-panel .fm-qp-sw { width: 38px; height: 22px; border-radius: 11px; background: rgb(128 128 128 / .45); position: relative; transition: background-color .2s; }
      #fm-quick-panel .fm-qp-sw::after { content: ""; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 8px; background: #fff;
        transition: translate calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease); }
      #fm-quick-panel .fm-qp-sw[on] { background: var(--fm-accent, AccentColor); }
      #fm-quick-panel .fm-qp-sw[on]::after { translate: 16px 0; }
      #fm-quick-panel .fm-qp-seg { display: flex; gap: 4px; padding: 3px; border-radius: 12px; background: var(--fm-hover, rgb(128 128 128 / .1)); }
      #fm-quick-panel .fm-qp-seg > button { all: unset; flex: 1; text-align: center; padding: 6px 0; border-radius: 9px; cursor: pointer; font-weight: 600; }
      #fm-quick-panel .fm-qp-seg > button[on] { background: var(--fm-accent, AccentColor); color: var(--fm-on-accent, #fff); }
      #fm-quick-panel .fm-qp-dots { display: flex; gap: 8px; flex-wrap: wrap; padding-inline: 2px; }
      #fm-quick-panel .fm-qp-dot { all: unset; width: 24px; height: 24px; border-radius: 12px; cursor: pointer; background: var(--c);
        box-shadow: inset 0 0 0 1px rgb(128 128 128 / .35); transition: scale calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease); }
      #fm-quick-panel .fm-qp-dot:hover { scale: 1.15; }
      #fm-quick-panel .fm-qp-dot[on] { box-shadow: 0 0 0 2px var(--fm-menu, Canvas), 0 0 0 4px var(--c); }
      #fm-quick-panel .fm-qp-dot.auto { background: conic-gradient(#ff5c5c, #ffd25c, #5cff8a, #5cc8ff, #a35cff, #ff5c5c); }
      #fm-quick-panel .fm-qp-more { all: unset; text-align: center; padding: 10px; border-radius: 12px; cursor: pointer; font-weight: 700;
        background: var(--fm-accent, AccentColor); color: var(--fm-on-accent, #fff); transition: scale calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease); }
      #fm-quick-panel .fm-qp-more:hover { scale: 1.02; }
      #fm-quick-panel .fm-qp-more:active { scale: .97; }
    `;
    try {
      win.windowUtils.loadSheetUsingURIString("data:text/css;charset=utf-8," + encodeURIComponent(QP_CSS), win.windowUtils.AUTHOR_SHEET);
    } catch (e) {
      log("быстрая панель: стили", e);
    }
    const ACCENTS = ["#3E91FF", "#8E6BFF", "#FF5C8A", "#FF7A45", "#FFB020", "#2FBF71", "#14B8C4", "#9AA0A6"];
    let panel = null;
    let fill = null;
    const buildPanel = () => {
      panel = doc.createXULElement("panel");
      panel.id = "fm-quick-panel";
      panel.setAttribute("type", "arrow");
      panel.setAttribute("role", "dialog");
      panel.setAttribute("noautofocus", "true");
      const box = el("div", "fm-qp");
      panel.append(box);
      (doc.getElementById("mainPopupSet") || doc.documentElement).append(panel);

      const head = el("div", "fm-qp-head");
      const title = el("div", "fm-qp-title");
      title.textContent = "Redesigned Fox";
      head.append(title);
      box.append(head);

      const cap = text => {
        const c = el("div", "fm-qp-cap");
        c.textContent = text;
        box.append(c);
      };
      // темы
      cap("Тема");
      const grid = el("div", "fm-qp-grid");
      box.append(grid);
      for (const [id, name, sw] of (themes ? themes.THEMES : [])) {
        const b = el("button", "fm-qp-theme");
        b.dataset.id = id;
        const pv = el("div", "fm-qp-pv");
        pv.style.setProperty("--a", sw[0]);
        pv.style.setProperty("--b", sw[1]);
        pv.style.setProperty("--c", sw[2]);
        pv.append(el("span"), el("span"), el("span"));
        const n = el("div", "fm-qp-name");
        n.textContent = name;
        b.append(pv, n);
        b.addEventListener("click", () => {
          for (const x of grid.children) x.toggleAttribute("on", x === b);
          themes.setTheme(id).then(ok => {
            log("темы: выбрана " + id + (ok ? "" : " (файлы не обновлены: " + themes.lastErrors().join("; ") + ")"));
            toast("Тема: " + name, "info");
          }, e => {
            log("темы: ОШИБКА", e);
            toast("Не получилось сменить тему", "warn");
          });
        });
        grid.append(b);
      }
      // без скруглений
      const sq = el("div", "fm-qp-row");
      const sqLabel = el("span");
      sqLabel.textContent = "Без скруглений";
      const sqSw = el("span", "fm-qp-sw");
      sq.append(sqLabel, sqSw);
      sq.addEventListener("click", () => {
        const cfg = studio.readConfig();
        if (cfg.square) {
          delete cfg.square;
        } else {
          cfg.square = true;
        }
        studio.save(cfg);
        sqSw.toggleAttribute("on", !!cfg.square);
        toast(cfg.square ? "Скругления убраны" : "Скругления как в теме", "info");
      });
      box.append(sq);
      // светлая / тёмная
      cap("Оформление");
      const seg = el("div", "fm-qp-seg");
      for (const [v, label] of [[2, "Авто"], [1, "Светлое"], [0, "Тёмное"]]) {
        const b = el("button");
        b.textContent = label;
        b.dataset.v = String(v);
        b.addEventListener("click", () => {
          Services.prefs.setIntPref("browser.theme.toolbar-theme", v);
          Services.prefs.setIntPref("browser.theme.content-theme", v);
          for (const x of seg.children) x.toggleAttribute("on", x === b);
        });
        seg.append(b);
      }
      box.append(seg);
      // акцент
      cap("Акцент");
      const dots = el("div", "fm-qp-dots");
      const auto = el("button", "fm-qp-dot auto");
      auto.title = "Как в теме / Windows";
      auto.dataset.c = "";
      dots.append(auto);
      for (const c of ACCENTS) {
        const d = el("button", "fm-qp-dot");
        d.style.setProperty("--c", c);
        d.dataset.c = c;
        d.title = c;
        dots.append(d);
      }
      dots.addEventListener("click", e => {
        const d = e.target.closest?.(".fm-qp-dot");
        if (!d) {
          return;
        }
        const cfg = studio.readConfig();
        if (d.dataset.c) {
          cfg.accent = d.dataset.c;
        } else {
          delete cfg.accent;
        }
        studio.save(cfg);
        for (const x of dots.children) x.toggleAttribute("on", x === d);
      });
      box.append(dots);
      // все настройки
      const more = el("button", "fm-qp-more");
      more.textContent = "Все настройки дизайна…";
      more.addEventListener("click", () => {
        panel.hidePopup();
        openOnce(win);
      });
      box.append(more);

      fill = () => {
        const cur = themes ? themes.current() : "";
        for (const x of grid.children) x.toggleAttribute("on", x.dataset.id === cur);
        const cfg = studio.readConfig();
        sqSw.toggleAttribute("on", !!cfg.square);
        let mode = 2;
        try {
          mode = Services.prefs.getIntPref("browser.theme.toolbar-theme", 2);
        } catch (e) {}
        for (const x of seg.children) x.toggleAttribute("on", x.dataset.v === String(mode));
        for (const x of dots.children) x.toggleAttribute("on", (x.dataset.c || "") === (cfg.accent || ""));
      };
      panel.addEventListener("popupshowing", () => fill());
      panel.addEventListener("popuphidden", () => (lastHidden = Date.now()));
    };
    let lastToggle = 0;
    let lastHidden = 0;
    const togglePanel = node => {
      // нажатие на кнопку при открытой панели: панель уже закрылась от этого же нажатия
      if (Date.now() - lastToggle < 400 || Date.now() - lastHidden < 300) {
        return;
      }
      lastToggle = Date.now();
      try {
        if (!panel) {
          buildPanel();
        }
        if (panel.state === "open" || panel.state === "showing") {
          panel.hidePopup();
          return;
        }
        let anchor = node && node.isConnected && node.getBoundingClientRect().width ? node : null;
        anchor = anchor?.querySelector?.(".toolbarbutton-icon") || anchor || doc.getElementById("PanelUI-menu-button");
        panel.openPopup(anchor, "bottomright topright", 0, 0, false, false);
        log("быстрая панель: открыта");
      } catch (e) {
        log("быстрая панель: ОШИБКА — открываю вкладку настроек", e);
        openOnce(win);
      }
    };

    const CustomizableUI = win.CustomizableUI;
    const WIDGET = "fm-studio-button";
    const hook = node => {
      if (!node || node._fmHooked) {
        return;
      }
      node._fmHooked = true;
      node.addEventListener("click", e => {
        if (e.button === 0) {
          e.stopPropagation();
          e.preventDefault();
          node.ownerGlobal.FloorpModernQuickPanel?.(node);
        }
      });
      node.addEventListener("command", e => {
        e.stopPropagation();
        node.ownerGlobal.FloorpModernQuickPanel?.(node);
      });
    };
    win.FloorpModernQuickPanel = togglePanel;
    if (CustomizableUI.getWidget(WIDGET)?.provider !== CustomizableUI.PROVIDER_API) {
      try {
        CustomizableUI.createWidget({
          id: WIDGET,
          type: "button",
          defaultArea: CustomizableUI.AREA_NAVBAR,
          label: "Дизайн",
          tooltiptext: "Redesigned Fox — тема, скругления, акцент (Alt+Shift+S — все настройки)",
          onCreated(node) {
            hook(node);
          },
        });
      } catch (e) {}
    }
    hook(doc.getElementById(WIDGET));
    // пункт в главном меню ☰ (меню создаётся при первом открытии)
    const addMenuItem = () => {
      const anchor = doc.getElementById("appMenu-settings-button");
      if (!anchor || doc.getElementById("appMenu-fm-studio")) {
        return;
      }
      const item = doc.createXULElement("toolbarbutton");
      item.id = "appMenu-fm-studio";
      item.className = "subviewbutton";
      item.setAttribute("label", "Дизайн (Redesigned Fox)");
      item.addEventListener("command", () => {
        win.PanelUI?.hide();
        openOnce(win);
      });
      anchor.before(item);
    };
    addMenuItem();
    doc.getElementById("appMenu-popup")?.addEventListener("popupshowing", addMenuItem);
    win.addEventListener("keydown", e => {
      if (e.altKey && e.shiftKey && !e.ctrlKey && !e.metaKey && e.code === "KeyS") {
        e.preventDefault();
        e.stopPropagation();
        openOnce(win);
      }
    }, true);
  });
  safe("now bar", () => {
    /* ------------- «Now Bar»: что играет в другой вкладке ------------- */
    const gB = win.gBrowser;
    if (!gB) {
      return;
    }
    // плашку можно выключить в установщике (Настройка → Плеер Now Bar)
    try {
      if (!Services.prefs.getBoolPref("floorp.modern.nowbar", true)) {
        return;
      }
    } catch (e) {}
    const bar = el("div", "fm-nowbar");
    const eq = el("div", "fm-nowbar-eq");
    eq.append(el("span"), el("span"), el("span"));
    // обложка трека поверх эквалайзера (если сайт её даёт)
    const art = el("img", "fm-nowbar-art");
    art.alt = "";
    art.addEventListener("error", () => art.removeAttribute("src"));
    eq.append(art);
    // тонкая полоска прогресса по низу плашки
    const progress = el("div", "fm-nowbar-progress");
    const progressFill = el("div", "fm-nowbar-progress-fill");
    progress.append(progressFill);
    const title = el("div", "fm-nowbar-title");
    const prev = el("div", "fm-nowbar-btn fm-nowbar-prev");
    const play = el("div", "fm-nowbar-btn fm-nowbar-play");
    const next = el("div", "fm-nowbar-btn fm-nowbar-next");
    const mute = el("div", "fm-nowbar-btn fm-nowbar-mute");
    const close = el("div", "fm-nowbar-btn fm-nowbar-close");
    prev.title = "Назад";
    next.title = "Вперёд";
    play.title = "Пауза / продолжить";
    mute.title = "Звук вкладки";
    close.title = "Скрыть";
    bar.append(eq, title, prev, play, next, mute, close, progress);
    host.after(bar);

    let current = null;      // вкладка, которую показывает плашка
    let pausedByUs = false;  // мы поставили на паузу — плашку не прячем
    const dismissed = new WeakSet();

    const controller = tab => {
      try {
        return tab.linkedBrowser.browsingContext.mediaController;
      } catch (e) {
        return null;
      }
    };
    // во вкладке идёт звонок (микрофон / камера) — это работа для плашки звонка
    const inCall = tab => {
      const w = tab._sharingState?.webRTC;
      return !!(w && (w.microphone || w.camera)) || /camera|microphone/.test(tab.getAttribute("sharing") || "");
    };
    // значок звука у вкладки гаснет с задержкой ~3 с; «уже тихо» видно по soundplaying-scheduledremoval
    const audible = tab => tab.hasAttribute("soundplaying") && !tab.hasAttribute("soundplaying-scheduledremoval");
    const pick = () => {
      if (current && current.isConnected && !inCall(current) && (current.hasAttribute("soundplaying") || pausedByUs)) {
        return current;
      }
      pausedByUs = false;
      mutedByUs = false;
      return [...gB.tabs].reverse().find(t => t.hasAttribute("soundplaying") && !dismissed.has(t) && !inCall(t)) || null;
    };
    const render = () => {
      current = pick();
      const show = !!current && current !== gB.selectedTab && !dismissed.has(current);
      bar.classList.toggle("fm-in", show);
      doc.documentElement.toggleAttribute("fm-nowbar", show);
      if (!current) {
        if (bar._shown) {
          bar._shown = false;
          pollTitle(false);
        }
        return;
      }
      if (!title.textContent || bar.dataset.tab !== String(current.linkedPanel)) {
        title.textContent = current.label || "Музыка";
        bar.dataset.tab = String(current.linkedPanel);
      }
      bar.toggleAttribute("data-paused", pausedByUs);
      bar.toggleAttribute("data-muted", current.hasAttribute("muted"));
      if (show !== bar._shown) {
        bar._shown = show;
        pollTitle(show);
      }
      if (show) {
        placeSaved();
      }
    };

    /* ---- перетаскивание плашки; место запоминается ---- */
    const POS_PREF = "floorp.modern.nowbar.pos";
    const area = () => bar.offsetParent || bar.parentNode;
    const placeAt = (x, y) => {
      const p = area();
      const maxX = Math.max(0, p.clientWidth - bar.offsetWidth - 8);
      const maxY = Math.max(0, p.clientHeight - bar.offsetHeight - 8);
      bar.style.left = Math.min(maxX, Math.max(8, x)) + "px";
      bar.style.top = Math.min(maxY, Math.max(8, y)) + "px";
      bar.style.bottom = "auto";
      bar.setAttribute("data-moved", "true");
    };
    function placeSaved() {
      let saved = "";
      try {
        saved = Services.prefs.getStringPref(POS_PREF, "");
      } catch (e) {}
      const m = /^([\d.]+),([\d.]+)$/.exec(saved);
      if (!m) {
        return;
      }
      const p = area();
      placeAt(+m[1] * p.clientWidth, +m[2] * p.clientHeight);
    }
    let drag = null;
    bar.addEventListener("pointerdown", e => {
      if (e.button !== 0 || e.target.closest(".fm-nowbar-btn")) {
        return;
      }
      const r = bar.getBoundingClientRect();
      const pr = area().getBoundingClientRect();
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, dx: e.clientX - r.left + pr.left, dy: e.clientY - r.top + pr.top, moved: false };
      bar.setPointerCapture(e.pointerId);
    });
    bar.addEventListener("pointermove", e => {
      if (!drag || e.pointerId !== drag.id) {
        return;
      }
      if (!drag.moved && Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) < 5) {
        return;
      }
      drag.moved = true;
      bar.classList.add("fm-dragging");
      placeAt(e.clientX - drag.dx, e.clientY - drag.dy);
    });
    const endDrag = e => {
      if (!drag || e.pointerId !== drag.id) {
        return;
      }
      if (drag.moved) {
        const p = area();
        const x = parseFloat(bar.style.left) / p.clientWidth;
        const y = parseFloat(bar.style.top) / p.clientHeight;
        try {
          Services.prefs.setStringPref(POS_PREF, `${x.toFixed(4)},${y.toFixed(4)}`);
        } catch (err) {}
        // после перетаскивания клик по названию не должен переключать вкладку
        bar.addEventListener("click", ev => ev.stopPropagation(), { capture: true, once: true });
      }
      bar.classList.remove("fm-dragging");
      drag = null;
    };
    bar.addEventListener("pointerup", endDrag);
    bar.addEventListener("pointercancel", endDrag);
    // двойной клик по пустому месту — вернуть плашку вниз по центру
    bar.addEventListener("dblclick", e => {
      if (e.target.closest(".fm-nowbar-btn")) {
        return;
      }
      try {
        Services.prefs.clearUserPref(POS_PREF);
      } catch (err) {}
      bar.removeAttribute("data-moved");
      bar.style.left = bar.style.top = bar.style.bottom = "";
    });
    win.addEventListener("resize", () => bar.classList.contains("fm-in") && placeSaved());

    title.addEventListener("click", () => current && (gB.selectedTab = current));
    /* ---- управление звуком в странице ----
       1) MediaController Firefox — работает там, где сайт сам сообщает о плеере (YouTube).
       2) Если не помогло — просим страницу (через наш actor) поставить на паузу
          сами <audio>/<video> (так работает Telegram и другие сайты без Media Session).
       3) Если звук всё равно играет — выключаем звук вкладки, чтобы «стоп» сработал всегда. */
    let mutedByUs = false;
    const pageMedia = async (tab, data) => {
      const out = [];
      try {
        for (const bc of tab.linkedBrowser.browsingContext.getAllBrowsingContextsInSubtree()) {
          const actor = bc.currentWindowGlobal?.getActor("FloorpPdfTweaks");
          if (actor) {
            out.push(actor.sendQuery("FM:media", data).catch(() => null));
          }
        }
      } catch (e) {
        log("now bar: страница недоступна", e);
      }
      return (await Promise.all(out)).filter(Boolean);
    };
    const wait = ms => new Promise(r => win.setTimeout(r, ms));
    // играет ли ещё что-то: спрашиваем саму страницу (видит и «невидимые» плееры Telegram),
    // если страница не ответила — смотрим на значок звука вкладки
    const stillPlaying = async tab => {
      if (!tab.isConnected) {
        return false;
      }
      const info = await pageMedia(tab, { action: "info" });
      return info.some(x => x.playing) || audible(tab);
    };

    play.addEventListener("click", async () => {
      const tab = current;
      if (!tab) {
        return;
      }
      const mc = controller(tab);
      if (pausedByUs) {
        pausedByUs = false;
        if (mutedByUs && tab.hasAttribute("muted")) {
          tab.toggleMuteAudio();
        }
        mutedByUs = false;
        try { mc?.play(); } catch (e) {}
        await pageMedia(tab, { action: "play" });
        render();
        return;
      }
      pausedByUs = true;
      render();
      // 1) кнопка паузы самого сайта (Media Session) — так сайт видит паузу у себя в интерфейсе
      try { mc?.pause(); } catch (e) {}
      await wait(350);
      // 2) ставим на паузу сами звуки страницы, в том числе невидимые (Telegram)
      if (await stillPlaying(tab)) {
        const r = await pageMedia(tab, { action: "pause" });
        log("now bar: пауза на странице — " + r.map(x => x.count).join(","));
        await wait(500);
        // 3) не вышло — выключаем звук вкладки, чтобы «стоп» срабатывал всегда
        if (await stillPlaying(tab) && !tab.hasAttribute("muted")) {
          tab.toggleMuteAudio();
          mutedByUs = true;
          log("now bar: страница не остановилась, звук вкладки выключен");
        }
      }
      render();
    });
    const mediaKey = async (main, alt, delta) => {
      const tab = current;
      const mc = tab && controller(tab);
      if (!tab) {
        return;
      }
      let keys = [];
      try {
        keys = [...(mc?.supportedKeys || [])];
      } catch (e) {}
      try {
        if (keys.includes(main)) {
          main === "previoustrack" ? mc.prevTrack() : mc.nextTrack();
        } else if (keys.includes(alt)) {
          alt === "seekbackward" ? mc.seekBackward(10) : mc.seekForward(10);
        } else {
          // сайт не сообщает о плеере: перематываем сам звук на 10 секунд
          const r = await pageMedia(tab, { action: "seek", delta });
          if (!r.some(x => x.count)) {
            toast("Этот сайт не даёт переключать треки", "warn");
          }
        }
      } catch (e) {
        log("now bar: назад/вперёд не сработало", e);
      }
      win.setTimeout(refreshTitle, 600);
    };
    prev.addEventListener("click", () => mediaKey("previoustrack", "seekbackward", -10));
    next.addEventListener("click", () => mediaKey("nexttrack", "seekforward", 10));

    /* ---- название трека: Media Session сайта или сам плеер на странице ---- */
    let titleTimer = 0;
    let tick = 0;
    const bigArt = list => {
      const arr = [...(list || [])].filter(a => a?.src);
      const size = a => Math.max(0, ...String(a.sizes || "").split(/\s+/).map(x => parseInt(x, 10) || 0));
      arr.sort((x, y) => size(y) - size(x));
      return arr[0]?.src || "";
    };
    async function refreshTitle() {
      const tab = current;
      if (!tab) {
        return;
      }
      tick++;
      let name = "", cover = "";
      try {
        const md = controller(tab)?.getMetadata?.();
        if (md?.title && md.title !== tab.label) {
          name = md.artist ? `${md.title} — ${md.artist}` : md.title;
        }
        cover = bigArt(md?.artwork);
      } catch (e) {}
      let pos = null;
      for (const r of await pageMedia(tab, { action: "info" })) {
        if (!name && r.title) {
          name = r.artist ? `${r.title} — ${r.artist}` : r.title;
        }
        if (!cover && r.artwork) {
          cover = r.artwork;
        }
        if (!pos && r.duration > 0) {
          pos = r;
        }
      }
      if (tab !== current) {
        return;
      }
      title.textContent = name || tab.label || "Музыка";
      title.title = (name ? name + "\n" : "") + (tab.label || "");
      // обложка: картинка сайта, иначе значок вкладки
      const src = /^(https?|data|blob):/.test(cover) ? cover : (tab.image || "");
      if (src && art.getAttribute("src") !== src) {
        art.setAttribute("src", src);
      }
      bar.toggleAttribute("data-art", !!src);
      bar.toggleAttribute("data-progress", !!pos);
      if (pos) {
        progressFill.style.transform = `scaleX(${Math.min(1, Math.max(0, pos.position / pos.duration)).toFixed(4)})`;
      }
    }
    const pollTitle = on => {
      win.clearInterval(titleTimer);
      if (on) {
        refreshTitle();
        titleTimer = win.setInterval(refreshTitle, 1000);
        scheduleMini();
      } else {
        bar.classList.remove("fm-mini");
      }
    };

    /* ---- мини-режим: через 5 с плашка сворачивается в кружок с обложкой,
       при наведении снова раскрывается (как Dynamic Island) ---- */
    let miniTimer = 0;
    function scheduleMini() {
      win.clearTimeout(miniTimer);
      miniTimer = win.setTimeout(() => {
        if (!bar.matches(":hover") && !drag) {
          bar.classList.add("fm-mini");
        }
      }, 5000);
    }
    bar.addEventListener("mouseenter", () => {
      win.clearTimeout(miniTimer);
      bar.classList.remove("fm-mini");
    });
    bar.addEventListener("mouseleave", scheduleMini);

    /* ---- медиа-клавиши клавиатуры, пока окно браузера активно ---- */
    win.addEventListener("keydown", e => {
      if (!current || !bar.classList.contains("fm-in")) {
        return;
      }
      const map = { MediaPlayPause: () => play.click(), MediaTrackNext: () => next.click(), MediaTrackPrevious: () => prev.click() };
      const fn = map[e.key];
      if (fn) {
        e.preventDefault();
        e.stopPropagation();
        fn();
      }
    }, true);
    mute.addEventListener("click", () => {
      current?.toggleMuteAudio();
      render();
    });
    close.addEventListener("click", () => {
      if (current) {
        dismissed.add(current);
      }
      pausedByUs = false;
      render();
    });

    const tc = gB.tabContainer;
    const onAttr = e => {
      const changed = e.detail?.changed || [];
      if (changed.includes("soundplaying") || changed.includes("muted") || changed.includes("label")) {
        if (changed.includes("soundplaying") && e.target.hasAttribute("soundplaying")) {
          dismissed.delete(e.target);
          if (e.target === current) {
            pausedByUs = false;
          }
        }
        render();
      }
    };
    tc.addEventListener("TabAttrModified", onAttr);
    tc.addEventListener("TabSelect", render);
    tc.addEventListener("TabClose", () => win.setTimeout(render, 0));
    onUnload.push(() => {
      tc.removeEventListener("TabAttrModified", onAttr);
      tc.removeEventListener("TabSelect", render);
    });
  });

  safe("call bar", () => {
    /* ------------- плашка звонка: микрофон / камера заняты в другой вкладке -------------
       Сверху по центру, как «островок» на телефоне: сайт, время звонка,
       выключить микрофон / камеру, перейти к звонку. */
    const gB = win.gBrowser;
    if (!gB) {
      return;
    }
    const CSS = `
      .fm-callbar { position: absolute; left: 50%; top: 10px; z-index: 1002; display: flex; align-items: center; gap: 4px;
        max-width: min(520px, calc(100% - 40px)); padding: 5px 6px 5px 6px; border-radius: 999px;
        background: var(--fm-bar, #1c1d21); color: var(--fm-ink, #f2f3f5); border: 1px solid var(--fm-line, rgb(255 255 255 / .1));
        box-shadow: 0 10px 30px rgb(0 0 0 / .35); font: 500 13px var(--fm-font, system-ui);
        opacity: 0; translate: -50% -14px; scale: .94; pointer-events: none;
        transition: opacity .25s ease, translate calc(.45s * var(--fm-k, 1)) var(--fm-spring, ease), scale calc(.45s * var(--fm-k, 1)) var(--fm-spring, ease), padding .3s; }
      .fm-callbar.fm-in { opacity: 1; translate: -50% 0; scale: 1; pointer-events: auto; }
      .fm-callbar-dot { flex: none; width: 30px; height: 30px; border-radius: 50%; position: relative; background: #2fbf71 center / 16px no-repeat;
        -moz-context-properties: fill; fill: #fff;
        background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='context-fill'><path d='M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z'/></svg>"); }
      .fm-callbar[data-kind="camera"] .fm-callbar-dot { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='context-fill'><rect x='2.5' y='6' width='13' height='12' rx='3'/><path d='M17 10.2l4.1-2.6a.6.6 0 0 1 .9.5v7.8a.6.6 0 0 1-.9.5L17 13.8z'/></svg>"); }
      .fm-callbar-dot::after { content: ""; position: absolute; inset: -3px; border-radius: 50%; border: 2px solid #2fbf71; animation: fm-call-ring 1.6s ease-out infinite; }
      .fm-callbar[data-mic-off] .fm-callbar-dot { background-color: #e5484d; }
      .fm-callbar[data-mic-off] .fm-callbar-dot::after { border-color: #e5484d; }
      @keyframes fm-call-ring { from { opacity: .8; scale: .9; } to { opacity: 0; scale: 1.5; } }
      .fm-callbar-text { flex: 1; min-width: 0; display: flex; flex-direction: column; padding: 0 8px; cursor: pointer; line-height: 1.2; }
      .fm-callbar-site { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 600; }
      .fm-callbar-time { font-size: 11.5px; opacity: .7; font-variant-numeric: tabular-nums; }
      .fm-callbar-text:hover .fm-callbar-site { color: var(--fm-accent, AccentColor); }
      .fm-callbar-btn { flex: none; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; background: center / 17px no-repeat;
        -moz-context-properties: fill; fill: currentColor; transition: background-color .2s, scale calc(.3s * var(--fm-k, 1)) var(--fm-spring, ease); }
      .fm-callbar-btn:hover { background-color: var(--fm-hover, rgb(128 128 128 / .15)); }
      .fm-callbar-btn:active { scale: .9; }
      .fm-callbar-btn[hidden] { display: none; }
      .fm-callbar-btn[data-off] { background-color: #e5484d; fill: #fff; }
      .fm-callbar-mic { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='context-fill' stroke-width='2' stroke-linecap='round'><rect x='9' y='3' width='6' height='11' rx='3' fill='context-fill'/><path d='M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21'/></svg>"); }
      .fm-callbar-mic[data-off] { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='context-fill' stroke-width='2' stroke-linecap='round'><rect x='9' y='3' width='6' height='11' rx='3' fill='context-fill'/><path d='M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M4 4l16 16'/></svg>"); }
      .fm-callbar-cam { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='context-fill'><rect x='2.5' y='6' width='13' height='12' rx='3'/><path d='M17 10.2l4.1-2.6a.6.6 0 0 1 .9.5v7.8a.6.6 0 0 1-.9.5L17 13.8z'/></svg>"); }
      .fm-callbar-cam[data-off] { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='context-fill' stroke='context-fill' stroke-width='2' stroke-linecap='round'><rect x='2.5' y='6' width='13' height='12' rx='3' stroke='none'/><path d='M17 10.2l4.1-2.6a.6.6 0 0 1 .9.5v7.8a.6.6 0 0 1-.9.5L17 13.8z' stroke='none'/><path d='M3 3l18 18' fill='none'/></svg>"); }
      .fm-callbar-go { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='context-fill' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5'/></svg>"); }
      .fm-callbar-hide { background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='context-fill' stroke-width='2' stroke-linecap='round'><path d='M7 7l10 10M17 7L7 17'/></svg>"); background-size: 14px; opacity: .7; }
      .fm-callbar.fm-mini { padding: 4px 12px 4px 4px; }
      .fm-callbar.fm-mini .fm-callbar-btn, .fm-callbar.fm-mini .fm-callbar-site { display: none; }
      .fm-callbar.fm-mini .fm-callbar-dot { width: 24px; height: 24px; background-size: 13px; }
      .fm-callbar.fm-mini .fm-callbar-time { font-size: 12.5px; opacity: 1; font-weight: 600; }
    `;
    try {
      win.windowUtils.loadSheetUsingURIString("data:text/css;charset=utf-8," + encodeURIComponent(CSS), win.windowUtils.AUTHOR_SHEET);
    } catch (e) {
      log("call bar: стили", e);
    }
    const bar = el("div", "fm-callbar");
    const dot = el("div", "fm-callbar-dot");
    const text = el("div", "fm-callbar-text");
    const site = el("div", "fm-callbar-site");
    const time = el("div", "fm-callbar-time");
    text.append(site, time);
    const mic = el("div", "fm-callbar-btn fm-callbar-mic");
    const cam = el("div", "fm-callbar-btn fm-callbar-cam");
    const go = el("div", "fm-callbar-btn fm-callbar-go");
    const hide = el("div", "fm-callbar-btn fm-callbar-hide");
    mic.title = "Микрофон: выключить / включить";
    cam.title = "Камера: выключить / включить";
    go.title = "Перейти к звонку";
    hide.title = "Скрыть до конца звонка";
    bar.append(dot, text, mic, cam, go, hide);
    host.after(bar);

    const started = new WeakMap();   // вкладка → когда начался звонок
    const muted = new WeakMap();     // вкладка → { mic, cam } выключены нами
    const dismissed = new WeakSet();
    let current = null;

    const state = tab => {
      const w = tab._sharingState?.webRTC || {};
      const attr = tab.getAttribute("sharing") || "";
      return {
        mic: !!w.microphone || attr.includes("microphone"),
        cam: !!w.camera || attr.includes("camera"),
        screen: !!w.screen || attr.includes("screen"),
      };
    };
    const host_ = tab => {
      try {
        return tab.linkedBrowser.currentURI.host.replace(/^www\./, "");
      } catch (e) {
        return "";
      }
    };
    const fmt = ms => {
      const t = Math.max(0, Math.floor(ms / 1000));
      const h = Math.floor(t / 3600), m = Math.floor(t / 60) % 60, s = t % 60;
      const p = n => String(n).padStart(2, "0");
      return h ? `${h}:${p(m)}:${p(s)}` : `${p(m)}:${p(s)}`;
    };
    // команды микрофону / камере — тем же способом, что и кнопки Firefox в индикаторе доступа
    const send = (tab, name) => {
      let n = 0;
      try {
        for (const bc of tab.linkedBrowser.browsingContext.getAllBrowsingContextsInSubtree()) {
          const actor = bc.currentWindowGlobal?.getActor("WebRTC");
          if (actor) {
            actor.sendAsyncMessage(name);
            n++;
          }
        }
      } catch (e) {
        log("call bar: " + name, e);
      }
      return n;
    };

    let timer = 0;
    let miniTimer = 0;
    const render = () => {
      const calls = [...gB.tabs].filter(t => {
        const st = state(t);
        if (st.mic || st.cam) {
          if (!started.has(t)) {
            started.set(t, Date.now());
          }
          return true;
        }
        started.delete(t);
        muted.delete(t);
        dismissed.delete(t);
        return false;
      });
      current = calls.find(t => t === current) || calls[calls.length - 1] || null;
      const show = !!current && current !== gB.selectedTab && !dismissed.has(current);
      bar.classList.toggle("fm-in", show);
      doc.documentElement.toggleAttribute("fm-callbar", show);
      win.clearInterval(timer);
      if (!current) {
        return;
      }
      const st = state(current);
      const m = muted.get(current) || {};
      bar.dataset.kind = st.cam ? "camera" : "phone";
      site.textContent = (st.cam ? "Видеозвонок · " : "Звонок · ") + (host_(current) || current.label);
      site.title = current.label;
      mic.hidden = !st.mic;
      cam.hidden = !st.cam;
      mic.toggleAttribute("data-off", !!m.mic);
      cam.toggleAttribute("data-off", !!m.cam);
      bar.toggleAttribute("data-mic-off", !!m.mic);
      const tick = () => {
        if (current) {
          time.textContent = fmt(Date.now() - (started.get(current) || Date.now())) + (m.mic ? " · микрофон выключен" : "");
        }
      };
      tick();
      if (show) {
        timer = win.setInterval(tick, 1000);
      }
    };
    const scheduleMini = () => {
      win.clearTimeout(miniTimer);
      miniTimer = win.setTimeout(() => {
        if (!bar.matches(":hover")) {
          bar.classList.add("fm-mini");
        }
      }, 6000);
    };
    bar.addEventListener("mouseenter", () => {
      win.clearTimeout(miniTimer);
      bar.classList.remove("fm-mini");
    });
    bar.addEventListener("mouseleave", scheduleMini);

    const toggle = (kind, onMsg, offMsg) => {
      if (!current) {
        return;
      }
      const m = muted.get(current) || {};
      const off = !m[kind];
      const n = send(current, off ? onMsg : offMsg);
      if (!n) {
        toast("Этот браузер не даёт выключить " + (kind === "mic" ? "микрофон" : "камеру") + " отсюда — перейдите к звонку", "warn");
        return;
      }
      m[kind] = off;
      muted.set(current, m);
      toast(kind === "mic" ? (off ? "Микрофон выключен" : "Микрофон включен") : (off ? "Камера выключена" : "Камера включена"), "info");
      render();
    };
    mic.addEventListener("click", () => toggle("mic", "webrtc:MuteMicrophone", "webrtc:UnmuteMicrophone"));
    cam.addEventListener("click", () => toggle("cam", "webrtc:MuteCamera", "webrtc:UnmuteCamera"));
    const goTo = () => {
      if (current) {
        gB.selectedTab = current;
      }
    };
    go.addEventListener("click", goTo);
    text.addEventListener("click", goTo);
    hide.addEventListener("click", () => {
      if (current) {
        dismissed.add(current);
      }
      render();
    });
    // Alt+Shift+M — микрофон в звонке (из любой вкладки)
    win.addEventListener("keydown", e => {
      if (e.altKey && e.shiftKey && !e.ctrlKey && e.code === "KeyM" && current) {
        e.preventDefault();
        e.stopPropagation();
        toggle("mic", "webrtc:MuteMicrophone", "webrtc:UnmuteMicrophone");
      }
    }, true);

    const tc = gB.tabContainer;
    const onAttr = e => {
      const changed = e.detail?.changed || [];
      if (changed.includes("sharing") || changed.includes("label") || changed.includes("busy")) {
        render();
      }
    };
    const onSelect = () => {
      render();
      if (bar.classList.contains("fm-in")) {
        bar.classList.remove("fm-mini");
        scheduleMini();
      }
    };
    tc.addEventListener("TabAttrModified", onAttr);
    tc.addEventListener("TabSelect", onSelect);
    tc.addEventListener("TabClose", () => win.setTimeout(render, 0));
    // запасная проверка: не во всех сборках вкладка сообщает об изменении доступа
    const poll = win.setInterval(render, 4000);
    onUnload.push(() => {
      tc.removeEventListener("TabAttrModified", onAttr);
      tc.removeEventListener("TabSelect", onSelect);
      win.clearInterval(poll);
      win.clearInterval(timer);
    });
    render();
  });

  safe("zoom and mute toasts", () => {
    /* ---------------- масштаб страницы и звук вкладки ---------------- */
    const gB = win.gBrowser;
    if (!gB) {
      return;
    }
    let lastBrowser = gB.selectedBrowser;
    const zoomOf = b => {
      try {
        return Math.round(win.ZoomManager.getZoomForBrowser(b) * 100);
      } catch (e) {
        return 0;
      }
    };
    let lastZoom = zoomOf(lastBrowser);
    let zoomTimer = 0;
    win.addEventListener("FullZoomChange", () => {
      win.clearTimeout(zoomTimer);
      zoomTimer = win.setTimeout(() => {
        const b = gB.selectedBrowser;
        const z = zoomOf(b);
        if (b === lastBrowser && z && z !== lastZoom) {
          toast(`Масштаб ${z}%`, "info");
        }
        lastBrowser = b;
        lastZoom = z;
      }, 120);
    }, true);
    gB.tabContainer.addEventListener("TabSelect", () => {
      lastBrowser = gB.selectedBrowser;
      lastZoom = zoomOf(lastBrowser);
    });
    gB.tabContainer.addEventListener("TabAttrModified", e => {
      if (e.target === gB.selectedTab && (e.detail?.changed || []).includes("muted")) {
        toast(e.target.hasAttribute("muted") ? "Звук вкладки выключен" : "Звук вкладки включён", "info");
      }
    });
  });

  safe("shortcuts", () => {
    /* ------------ Alt+Shift+D — дубли, Alt+Shift+Z — режим фокуса ------------ */
    win.addEventListener("keydown", e => {
      if (!e.altKey || !e.shiftKey || e.ctrlKey || e.metaKey) {
        return;
      }
      if (e.code === "KeyD") {
        e.preventDefault();
        e.stopPropagation();
        const gB = win.gBrowser;
        const seen = new Set();
        const extra = [];
        // выбранная вкладка остаётся, закрываем её копии
        for (const t of [gB.selectedTab, ...gB.tabs]) {
          if (t.pinned) {
            continue;
          }
          const url = t.linkedBrowser?.currentURI?.spec;
          if (!url || url === "about:blank") {
            continue;
          }
          if (seen.has(url)) {
            if (t !== gB.selectedTab) {
              extra.push(t);
            }
          } else {
            seen.add(url);
          }
        }
        const uniq = [...new Set(extra)];
        if (uniq.length) {
          gB.removeTabs(uniq);
          toast(`Закрыто одинаковых вкладок: ${uniq.length}`, "ok");
        } else {
          toast("Одинаковых вкладок нет", "info");
        }
      } else if (e.code === "KeyZ") {
        e.preventDefault();
        e.stopPropagation();
        const on = !doc.documentElement.hasAttribute("fm-focus");
        doc.documentElement.toggleAttribute("fm-focus", on);
        toast(on ? "Режим фокуса: Alt+Shift+Z — выйти" : "Режим фокуса выключен", "info");
      }
    }, true);
  });
  safe("gpu switch", () => {
    /* ---- переключение видеокарты (встроенная ↔ дискретная) ----
       Windows сбрасывает графику, и открытые PDF остаются с пустыми страницами.
       Ловим сброс и просим все открытые PDF перерисоваться (сейчас и ещё раз чуть позже). */
    const gB = win.gBrowser;
    if (!gB) {
      return;
    }
    const refreshAll = () => {
      for (const tab of gB.tabs) {
        try {
          for (const bc of tab.linkedBrowser.browsingContext.getAllBrowsingContextsInSubtree()) {
            bc.currentWindowGlobal?.getActor("FloorpPdfTweaks")?.sendAsyncMessage("FM:pdf-refresh");
          }
        } catch (e) {}
      }
    };
    let lastReset = 0;
    const observer = {
      observe(subject, topic) {
        const now = Date.now();
        if (now - lastReset < 3000) {
          return;
        }
        lastReset = now;
        log("сброс графики: " + topic);
        win.setTimeout(refreshAll, 1200);
        win.setTimeout(refreshAll, 4000);
      },
    };
    const topics = ["compositor-reinitialized", "graphics-device-reset", "gpu-process-crashed"];
    for (const t of topics) {
      Services.obs.addObserver(observer, t);
    }
    onUnload.push(() => topics.forEach(t => {
      try { Services.obs.removeObserver(observer, t); } catch (e) {}
    }));
  });
})();
