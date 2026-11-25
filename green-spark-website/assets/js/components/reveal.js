/* ==========================================================================
   Scroll motion: fade/rise reveals, letter-by-letter text reveal tied to
   scroll, dotted route drawing in the intro collage, gentle parallax.
   All of it is skipped with prefers-reduced-motion (content shows at once).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("reveal", function (ctx) {
    var els = GS.qsa("[data-reveal], [data-reveal-group], .process, .bd-map, .collage__card", ctx).filter(function (e) { return !e._gsr; });
    if (!els.length) return;
    if (GS.reducedMotion() || !("IntersectionObserver" in w)) { els.forEach(function (e) { e.classList.add("is-revealed"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-revealed"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    els.forEach(function (e) { e._gsr = true; io.observe(e); });
  });

  GS.register("textReveal", function (ctx) {
    GS.qsa("[data-text-reveal]", ctx).forEach(function (el) {
      if (el._gs) return; el._gs = true;
      if (GS.reducedMotion()) return;
      var chars = [];
      function walk(node, parent) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = d.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(" ")); return; }
              var word = d.createElement("span"); word.className = "tr-word";
              part.split("").forEach(function (ch) { var s = d.createElement("span"); s.className = "tr-ch"; s.textContent = ch; word.appendChild(s); chars.push(s); });
              frag.appendChild(word);
            });
            node.replaceChild(frag, n);
          } else if (n.nodeType === 1) walk(n);
        });
      }
      var label = el.textContent.trim();
      walk(el);
      el.setAttribute("aria-label", label);
      GS.qsa(".tr-word", el).forEach(function (wd) { wd.setAttribute("aria-hidden", "true"); });
      var last = -1;
      GS.onScroll(function () {
        var r = el.getBoundingClientRect(), vh = w.innerHeight;
        var p = GS.clamp((vh * 0.85 - r.top) / (r.height + vh * 0.45), 0, 1);
        var n = Math.round(p * chars.length);
        if (n === last) return;
        for (var k = 0; k < chars.length; k++) chars[k].classList.toggle("is-on", k < n);
        last = n;
      });
    });
  });

  GS.register("collageRoute", function (ctx) {
    GS.qsa("[data-route]", ctx).forEach(function (wrap) {
      if (wrap._gs) return; wrap._gs = true;
      var mask = GS.qs(".route-mask", wrap), pins = GS.qsa(".collage__pin", wrap);
      if (GS.reducedMotion()) { if (mask) mask.style.strokeDashoffset = "0"; pins.forEach(function (p) { p.classList.add("is-on"); }); return; }
      GS.onScroll(function () {
        var r = wrap.getBoundingClientRect(), vh = w.innerHeight;
        var p = GS.clamp((vh * 0.75 - r.top) / (r.height * 0.95), 0, 1);
        if (mask) mask.style.strokeDashoffset = String(1 - p);
        pins.forEach(function (pin, k) { pin.classList.toggle("is-on", p > 0.12 + k * 0.32); });
      });
    });
  });

  GS.register("parallax", function (ctx) {
    if (GS.reducedMotion()) return;
    GS.qsa("[data-parallax]", ctx).forEach(function (el) {
      if (el._gs) return; el._gs = true;
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.12;
      GS.onScroll(function () {
        var r = el.parentElement.getBoundingClientRect(), vh = w.innerHeight;
        if (r.bottom < 0 || r.top > vh) return;
        var center = (r.top + r.height / 2 - vh / 2);
        el.style.transform = "translate3d(0," + (-center * speed).toFixed(1) + "px,0)";
      });
    });
  });
})(window, document, window.GS);
