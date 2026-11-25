/* ==========================================================================
   Priority programmes showcase ([data-showcase]). WAI-ARIA tabs (arrow keys,
   Home/End) that also advance on their own every 9 s, with a progress bar in
   the active tab. Autoplay pauses on hover, keyboard focus, a hidden browser
   tab or when the section is off screen, and never runs with reduced motion.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  var DUR = 9000;

  GS.register("showcase", function (ctx) {
    GS.qsa("[data-showcase]", ctx).forEach(function (root) {
      if (root._gs) return; root._gs = true;
      var tabs = GS.qsa('[role="tab"]', root); if (!tabs.length) return;
      var i = 0, t0 = 0, elapsed = 0, raf = 0, hover = false, focus = false, visible = false;
      var auto = !GS.reducedMotion();

      function select(k, byUser) {
        i = (k + tabs.length) % tabs.length;
        tabs.forEach(function (t, j) {
          var on = j === i; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
          t.style.setProperty("--p", "0");
          var p = d.getElementById(t.getAttribute("aria-controls"));
          if (p) {
            p.hidden = !on;
            GS.qsa("video", p).forEach(function (v) { if (!on && !v.paused) v.pause(); });
          }
        });
        elapsed = 0; t0 = performance.now();
        if (byUser) auto = false;                       // a choice by the visitor stops the rotation
        if (!auto) tabs[i].style.setProperty("--p", "1");
      }

      function running() { return auto && visible && !hover && !focus && !d.hidden; }
      function tick(now) {
        raf = requestAnimationFrame(tick);
        if (!running()) { t0 = now - elapsed; return; }
        elapsed = now - t0;
        tabs[i].style.setProperty("--p", Math.min(elapsed / DUR, 1).toFixed(3));
        if (elapsed >= DUR) select(i + 1, false);
      }

      tabs.forEach(function (t, k) {
        t.addEventListener("click", function () { select(k, true); });
        t.addEventListener("keydown", function (e) {
          var n = null;
          if (e.key === "ArrowRight" || e.key === "ArrowDown") n = k + 1;
          if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = k - 1;
          if (e.key === "Home") n = 0; if (e.key === "End") n = tabs.length - 1;
          if (n !== null) { e.preventDefault(); select(n, true); tabs[i].focus(); }
        });
      });
      root.addEventListener("pointerenter", function () { hover = true; });
      root.addEventListener("pointerleave", function () { hover = false; });
      root.addEventListener("focusin", function () { focus = true; });
      root.addEventListener("focusout", function () { setTimeout(function () { focus = root.contains(d.activeElement); }, 0); });
      if ("IntersectionObserver" in w) {
        new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: .25 }).observe(root);
      } else { visible = true; }

      select(0, false);
      if (auto) raf = requestAnimationFrame(tick); else tabs[0].style.setProperty("--p", "1");
    });
  });
})(window, document, window.GS);
