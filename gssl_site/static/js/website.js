/* ==========================================================================
   Website bootstrap: page-level widgets that are not reusable components,
   then boots every registered module.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  /* Green ICS anatomy: hotspots highlight the matching part in the list */
  GS.register("anatomy", function (ctx) {
    GS.qsa("[data-anatomy]", ctx).forEach(function (root) {
      if (root._gs) return; root._gs = true;
      var spots = GS.qsa("[data-part]", root), rows = GS.qsa("[data-part-row]", root);
      function set(name) {
        spots.forEach(function (s) { s.setAttribute("aria-pressed", String(s.getAttribute("data-part") === name)); });
        rows.forEach(function (r) { r.classList.toggle("is-active", r.getAttribute("data-part-row") === name); });
      }
      spots.forEach(function (s) { s.addEventListener("click", function () { set(s.getAttribute("data-part")); }); s.addEventListener("mouseenter", function () { set(s.getAttribute("data-part")); }); });
      rows.forEach(function (r) { r.addEventListener("mouseenter", function () { set(r.getAttribute("data-part-row")); }); });
    });
  });

  /* Component library: demo buttons that switch a form between its states */
  GS.register("demoStates", function (ctx) {
    GS.qsa("[data-demo-state]", ctx).forEach(function (b) {
      if (b._gs) return; b._gs = true;
      b.addEventListener("click", function () {
        var f = d.getElementById(b.getAttribute("data-target")); if (!f) return;
        var s = b.getAttribute("data-demo-state");
        if (s === "toast") { GS.toast("Saved. This is a toast notification."); return; }
        if (s === "loading") { var bt = GS.qs("[type=submit]", f); bt.classList.add("is-loading"); setTimeout(function () { bt.classList.remove("is-loading"); }, 1800); return; }
        f.setAttribute("data-state", s);
      });
    });
  });

  /* Photo cards: if a hosted stock photo cannot load (offline, blocked by a
     content policy), show the local photo-slot image instead */
  GS.register("photoFallback", function (ctx) {
    GS.qsa("img[data-fallback]", ctx).forEach(function (im) {
      if (im._gsFb) return; im._gsFb = true;
      function swap() {
        var f = im.getAttribute("data-fallback");
        if (!f || im.getAttribute("src") === f) return;
        im.removeAttribute("srcset"); im.src = f;
      }
      im.addEventListener("error", swap);
      if (im.complete && im.currentSrc && im.naturalWidth === 0) swap();
    });
  });

  /* Preloader: the GSSL spark shows until the page has loaded */
  (function () {
    var pl = d.querySelector("[data-preloader]"); if (!pl) return;
    var t0 = Date.now(), done = false;
    function hide() {
      if (done) return; done = true;
      setTimeout(function () {
        pl.classList.add("is-done");
        setTimeout(function () { if (pl.parentNode) pl.parentNode.removeChild(pl); }, 700);
      }, Math.max(0, 450 - (Date.now() - t0)));
    }
    if (d.readyState === "complete") hide(); else w.addEventListener("load", hide);
    setTimeout(hide, 2500);
  })();

  /* Green ICS product viewer: the photo follows the selected model tab */
  GS.register("productViewer", function (ctx) {
    GS.qsa("[data-product-viewer]", ctx).forEach(function (root) {
      if (root._gs) return; root._gs = true;
      var figs = GS.qsa("[data-product]", root), tabs = GS.qsa('[role="tab"]', root);
      function sync() {
        var sel = tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0]; if (!sel) return;
        var id = sel.getAttribute("aria-controls");
        figs.forEach(function (f) { f.hidden = f.getAttribute("data-product") !== id; });
      }
      tabs.forEach(function (t) { t.addEventListener("click", function () { setTimeout(sync, 0); }); t.addEventListener("keydown", function () { setTimeout(sync, 0); }); });
      sync();
    });
  });

  /* Year in footer */
  GS.register("year", function (ctx) { GS.qsa("[data-year]", ctx).forEach(function (y) { y.textContent = new Date().getFullYear(); }); });

  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", function () { GS.boot(d); });
  else GS.boot(d);
})(window, document, window.GS);
