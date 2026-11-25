/* ==========================================================================
   Accordion (FAQ). data-accordion="single" keeps one panel open.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("accordion", function (ctx) {
    GS.qsa("[data-accordion]", ctx).forEach(function (root) {
      if (root._gs) return; root._gs = true;
      var single = root.getAttribute("data-accordion") === "single";
      GS.qsa(".accordion__trigger", root).forEach(function (btn) {
        var panel = d.getElementById(btn.getAttribute("aria-controls"));
        btn.addEventListener("click", function () {
          if (btn.getAttribute("aria-disabled") === "true") return;
          var on = btn.getAttribute("aria-expanded") !== "true";
          if (single && on) GS.qsa(".accordion__trigger", root).forEach(function (o) {
            if (o !== btn) { o.setAttribute("aria-expanded", "false"); var p = d.getElementById(o.getAttribute("aria-controls")); if (p) p.classList.remove("is-open"); }
          });
          btn.setAttribute("aria-expanded", String(on)); if (panel) panel.classList.toggle("is-open", on);
        });
      });
    });
  });
})(window, document, window.GS);
