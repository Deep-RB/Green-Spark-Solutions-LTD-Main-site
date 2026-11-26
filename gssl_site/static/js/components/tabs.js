/* ==========================================================================
   Tabs (WAI-ARIA tabs pattern: arrow keys, Home/End).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("tabs", function (ctx) {
    GS.qsa("[data-tabs]", ctx).forEach(function (root) {
      if (root._gs) return; root._gs = true;
      var tabs = GS.qsa('[role="tab"]', root);
      function select(t, focus) {
        tabs.forEach(function (x) {
          var on = x === t; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1;
          var p = d.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on;
        });
        if (focus) t.focus();
        root.dispatchEvent(new CustomEvent("gs:tab", { detail: { id: t.id } }));
      }
      tabs.forEach(function (t, k) {
        t.addEventListener("click", function () { if (!t.disabled) select(t); });
        t.addEventListener("keydown", function (e) {
          var en = tabs.filter(function (x) { return !x.disabled; }), j = en.indexOf(t), n = null;
          if (e.key === "ArrowRight") n = en[(j + 1) % en.length];
          if (e.key === "ArrowLeft") n = en[(j - 1 + en.length) % en.length];
          if (e.key === "Home") n = en[0]; if (e.key === "End") n = en[en.length - 1];
          if (n) { e.preventDefault(); select(n, true); }
        });
      });
    });
  });
})(window, document, window.GS);
