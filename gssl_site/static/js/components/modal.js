/* ==========================================================================
   Modal dialog — focus trap, Escape/backdrop close, focus restore, scroll lock.
   Trigger: <button data-modal-open="modal-id">  ·  close: [data-modal-close]
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("modal", function (ctx) {
    GS.qsa("[data-modal-open]", ctx).forEach(function (btn) {
      if (btn._gs) return; btn._gs = true;
      var m = d.getElementById(btn.getAttribute("data-modal-open")); if (!m) return;
      var release = null;
      function close() {
        m.classList.remove("is-open"); d.body.classList.remove("is-locked");
        if (release) { release(); release = null; }
        setTimeout(function () { if (!m.classList.contains("is-open")) m.setAttribute("hidden", ""); }, 420);
      }
      btn.addEventListener("click", function () {
        m.removeAttribute("hidden"); requestAnimationFrame(function () { m.classList.add("is-open"); });
        d.body.classList.add("is-locked"); release = GS.trapFocus(GS.qs(".modal__dialog", m), { onEscape: close });
      });
      if (!m._gs) { m._gs = true; GS.qsa("[data-modal-close]", m).forEach(function (c) { c.addEventListener("click", function () { m._close && m._close(); }); }); }
      m._close = close;
    });
  });
})(window, document, window.GS);
