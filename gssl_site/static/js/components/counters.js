/* ==========================================================================
   Stat counters: count up once when visible. Markup keeps the final value as
   text (no-JS / SEO safe): <span data-count="20000" data-suffix="+">20,000+</span>
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("counters", function (ctx) {
    var els = GS.qsa("[data-count]", ctx).filter(function (e) { return !e._gs; });
    if (!els.length || GS.reducedMotion() || !("IntersectionObserver" in w)) return;
    var fmt = function (n, dec) { return n.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return; io.unobserve(en.target);
        var el = en.target, end = parseFloat(el.getAttribute("data-count")), dec = +(el.getAttribute("data-decimals") || 0);
        var pre = el.getAttribute("data-prefix") || "", suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1800;
        function step(t) {
          if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4);
          el.textContent = pre + fmt(end * e, dec) + suf;
          if (k < 1) w.requestAnimationFrame(step);
        }
        w.requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    els.forEach(function (e) { e._gs = true; io.observe(e); });
  });
})(window, document, window.GS);
