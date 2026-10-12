// Floorp Modern loader. Loads scripts from <profile>\chrome\pdf-tweaks\
try {
  const Ci = Components.interfaces;
  const Cc = Components.classes;
  const dir = Cc["@mozilla.org/file/directory_service;1"]
    .getService(Ci.nsIProperties)
    .get("UChrm", Ci.nsIFile);
  dir.append("pdf-tweaks");
  if (dir.exists()) {
    const io = Cc["@mozilla.org/network/io-service;1"].getService(Ci.nsIIOService);
    io.getProtocolHandler("resource")
      .QueryInterface(Ci.nsIResProtocolHandler)
      .setSubstitution("pdftweaks", io.newFileURI(dir));

    // 1. просмотрщик PDF: тема и рисование
    ChromeUtils.registerWindowActor("FloorpPdfTweaks", {
      parent: { esModuleURI: "resource://pdftweaks/FloorpPdfTweaksParent.sys.mjs" },
      child: {
        esModuleURI: "resource://pdftweaks/FloorpPdfTweaksChild.sys.mjs",
        events: { DOMContentLoaded: {} },
      },
      allFrames: true,
      safeForUntrustedWebProcess: true,
    });

    // 2. новые функции окна браузера
    const script = dir.clone();
    script.append("floorp-modern.uc.js");
    if (script.exists()) {
      const loader = Cc["@mozilla.org/moz/jssubscript-loader;1"].getService(Ci.mozIJSSubScriptLoader);
      Cc["@mozilla.org/observer-service;1"].getService(Ci.nsIObserverService).addObserver({
        observe(win) {
          try {
            if (win.location.href === "chrome://browser/content/browser.xhtml") {
              loader.loadSubScriptWithOptions("resource://pdftweaks/floorp-modern.uc.js", {
                target: win,
                ignoreCache: true,
              });
            }
          } catch (e) {
            Components.utils.reportError(e);
          }
        },
      }, "browser-delayed-startup-finished");
    }
  }
} catch (e) {
  Components.utils.reportError(e);
}
