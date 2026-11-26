/* ==========================================================================
   "Smoke to clean air": a light canvas animation layered over hero images and
   the CTA band. Warm smoke rises from the lower left and turns into small
   green sparks and leaves as it climbs. ~70 particles, pauses off-screen,
   off with reduced motion / Save-Data.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("sparkCanvas", function (ctx) {
    if (GS.reducedMotion() || GS.saveData()) return;
    GS.qsa("[data-spark-canvas]", ctx).forEach(function (cv) {
      if (cv._gs) return; cv._gs = true;
      var c = cv.getContext("2d"); if (!c) return;
      var dpr = Math.min(w.devicePixelRatio || 1, 1.5), W = 0, H = 0, parts = [], raf = 0, visible = true;
      var mode = cv.getAttribute("data-spark-canvas") || "hero";
      var N = mode === "hero" ? (w.innerWidth < 768 ? 34 : 70) : 40;
      function size() { var r = cv.getBoundingClientRect(); W = r.width; H = r.height; cv.width = W * dpr; cv.height = H * dpr; c.setTransform(dpr, 0, 0, dpr, 0, 0); }
      function spawn(p, initial) {
        p.x = mode === "hero" ? W * (0.05 + Math.random() * 0.5) : Math.random() * W;
        p.y = initial ? Math.random() * H : H + 20;
        p.r = 18 + Math.random() * 40; p.vy = 0.25 + Math.random() * 0.55; p.vx = (Math.random() - 0.3) * 0.35;
        p.life = 0; p.seed = Math.random() * 1000; p.rot = Math.random() * 6.28; p.spin = (Math.random() - 0.5) * 0.02;
        return p;
      }
      function init() { parts = []; for (var k = 0; k < N; k++) parts.push(spawn({}, true)); }
      function leaf(x, y, s, rot, col, a) {
        c.save(); c.translate(x, y); c.rotate(rot); c.globalAlpha = a; c.fillStyle = col;
        c.beginPath(); c.moveTo(0, -s); c.bezierCurveTo(s * 0.8, -s * 0.5, s * 0.8, s * 0.5, 0, s); c.bezierCurveTo(-s * 0.8, s * 0.5, -s * 0.8, -s * 0.5, 0, -s); c.fill(); c.restore();
      }
      function frame(t) {
        raf = 0; if (!visible) return;
        c.clearRect(0, 0, W, H);
        for (var k = 0; k < parts.length; k++) {
          var p = parts[k];
          p.y -= p.vy; p.x += p.vx + Math.sin((t * 0.0004) + p.seed) * 0.35; p.rot += p.spin; p.life++;
          var h = 1 - p.y / H; // 0 bottom → 1 top
          if (p.y < -40) spawn(p, false);
          if (h < 0.55) { // smoke: soft warm grey blobs
            var a = 0.05 * Math.sin(Math.PI * Math.min(1, h / 0.55));
            var g = c.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * (1 + h));
            g.addColorStop(0, "rgba(214,205,190," + a.toFixed(3) + ")"); g.addColorStop(1, "rgba(214,205,190,0)");
            c.fillStyle = g; c.beginPath(); c.arc(p.x, p.y, p.r * (1 + h), 0, 6.283); c.fill();
          } else { // clean air: sparks + leaves
            var a2 = Math.min(1, (h - 0.55) * 4) * (1 - Math.max(0, h - 0.85) * 6);
            if (a2 <= 0) continue;
            if (p.seed % 3 < 1) leaf(p.x, p.y, 4 + (p.seed % 4), p.rot, p.seed % 2 < 1 ? "#C4EE5A" : "#7BD389", a2 * 0.75);
            else { c.globalAlpha = a2; c.fillStyle = "#D9F98E"; c.beginPath(); c.arc(p.x, p.y, 1.2 + (p.seed % 1.6), 0, 6.283); c.fill(); c.globalAlpha = 1; }
          }
        }
        raf = w.requestAnimationFrame(frame);
      }
      size(); init(); raf = w.requestAnimationFrame(frame);
      w.addEventListener("resize", function () { size(); });
      if ("IntersectionObserver" in w) new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting; if (visible && !raf) raf = w.requestAnimationFrame(frame);
      }).observe(cv);
      d.addEventListener("visibilitychange", function () { visible = !d.hidden; if (visible && !raf) raf = w.requestAnimationFrame(frame); });
    });
  });
})(window, document, window.GS);
