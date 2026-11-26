/* ==========================================================================
   Notice bar: shown only inside its window (data-window-start/-end, normally
   an event's feedback window) and until dismissed. Dismissal is remembered
   per notice id (localStorage, optional). Requires events.js (GS.day/GS.now).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  /* Notice bar: visible only inside its window and until dismissed */
  GS.register("noticeBar", function () {
    var bar = GS.qs("[data-notice-bar]"); if (!bar || bar._gs) return; bar._gs = true;
    var now = GS.now(), s = GS.day(bar.getAttribute("data-window-start")), e = GS.day(bar.getAttribute("data-window-end"), true);
    var id = "gs-notice-" + (bar.getAttribute("data-notice-id") || "x");
    if ((s && now < s) || (e && now > e) || GS.store.get(id) === "1") { bar.hidden = true; GS.refresh(); return; }
    var btn = GS.qs("[data-notice-dismiss]", bar);
    if (btn) btn.addEventListener("click", function () {
      bar.classList.add("is-dismissed"); GS.store.set(id, "1");
      setTimeout(function () { bar.hidden = true; w.dispatchEvent(new Event("resize")); }, 420);
    });
  });

})(window, document, window.GS);
