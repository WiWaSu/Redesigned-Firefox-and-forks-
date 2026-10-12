/* Floorp Modern — новые функции окна браузера.
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
    /* ------- Floorp Modern Studio: тонкая настройка дизайна -------
       Кнопка «Дизайн» на панели, пункт в меню ☰ и Alt+Shift+S. */
    const studio = ChromeUtils.importESModule("resource://pdftweaks/FloorpModernStudio.sys.mjs");
    studio.init();
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
        ChromeUtils.importESModule("resource://pdftweaks/FloorpPdfTweaksParent.sys.mjs").openStudio(w);
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
    const CustomizableUI = win.CustomizableUI;
    const WIDGET = "fm-studio-button";
    if (CustomizableUI.getWidget(WIDGET)?.provider !== CustomizableUI.PROVIDER_API) {
      try {
        CustomizableUI.createWidget({
          id: WIDGET,
          type: "button",
          defaultArea: CustomizableUI.AREA_NAVBAR,
          label: "Дизайн",
          tooltiptext: "Floorp Modern Studio — настроить дизайн (Alt+Shift+S)",
          onCommand(event) {
            open(event.target.ownerGlobal);
          },
        });
      } catch (e) {}
    }
    // пункт в главном меню ☰ (меню создаётся при первом открытии)
    const addMenuItem = () => {
      const anchor = doc.getElementById("appMenu-settings-button");
      if (!anchor || doc.getElementById("appMenu-fm-studio")) {
        return;
      }
      const item = doc.createXULElement("toolbarbutton");
      item.id = "appMenu-fm-studio";
      item.className = "subviewbutton";
      item.setAttribute("label", "Дизайн (Floorp Modern)");
      item.addEventListener("command", () => {
        win.PanelUI?.hide();
        open(win);
      });
      anchor.before(item);
    };
    addMenuItem();
    doc.getElementById("appMenu-popup")?.addEventListener("popupshowing", addMenuItem);
    win.addEventListener("keydown", e => {
      if (e.altKey && e.shiftKey && !e.ctrlKey && !e.metaKey && e.code === "KeyS") {
        e.preventDefault();
        e.stopPropagation();
        open(win);
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
    const pick = () => {
      if (current && current.isConnected && (current.hasAttribute("soundplaying") || pausedByUs)) {
        return current;
      }
      pausedByUs = false;
      mutedByUs = false;
      return [...gB.tabs].reverse().find(t => t.hasAttribute("soundplaying") && !dismissed.has(t)) || null;
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
    const still = (tab, ms) => new Promise(r => win.setTimeout(() => r(tab.isConnected && tab.hasAttribute("soundplaying")), ms));

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
      try { mc?.pause(); } catch (e) {}
      if (await still(tab, 700)) {
        await pageMedia(tab, { action: "pause" });
        if (await still(tab, 1600) && !tab.hasAttribute("muted")) {
          tab.toggleMuteAudio();
          mutedByUs = true;
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
