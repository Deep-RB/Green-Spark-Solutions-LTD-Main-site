/* ==========================================================================
   Sticky scroll scenes (desktop ≥ 992px, motion allowed):
   • Expanding cards — the image grows from a rounded window to full bleed,
     then each card opens in turn as you scroll; backgrounds crossfade.
   • Floating cards — illustration tiles drift sideways around the copy.
   Below 992px / reduced motion: cards become a tap-to-open list, tiles a
   swipeable row.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("expandingCards", function (ctx) {
    GS.qsa("[data-xcards]", ctx).forEach(function (sec) {
      if (sec._gs) return; sec._gs = true;
      var scene = GS.qs(".xcards__scene", sec), bg = GS.qs(".xcards__bg", sec);
      var cards = GS.qsa(".xcard", sec), imgs = GS.qsa(".xcards__img", sec), status = GS.qs(".xcards__progress", sec);
      var active = -1, scroll = !GS.reducedMotion();
      if (scroll) sec.classList.add("xcards--scroll");
      function set(n) {
        if (n === active) return; active = n;
        cards.forEach(function (c, k) {
          c.classList.toggle("is-active", k === n);
          var b = GS.qs(".xcard__btn", c); if (b) b.setAttribute("aria-expanded", String(k === n));
        });
        imgs.forEach(function (im, k) { im.classList.toggle("is-active", k === n); });
        if (status) status.textContent = String(n + 1).padStart(2, "0") + " / " + String(cards.length).padStart(2, "0");
      }
      cards.forEach(function (c, k) {
        var b = GS.qs(".xcard__btn", c);
        if (b) b.addEventListener("click", function () {
          if (scroll && GS.isDesktop()) {
            var top = scene.getBoundingClientRect().top + w.pageYOffset;
            var span = scene.offsetHeight - w.innerHeight;
            w.scrollTo({ top: top + span * (0.25 + (k + 0.5) * 0.75 / cards.length), behavior: "smooth" });
          } else set(k);
        });
      });
      set(0);
      if (!scroll) return;
      GS.onScroll(function () {
        if (!GS.isDesktop()) { bg.style.setProperty("--clip-y", "0%"); bg.style.setProperty("--clip-x", "0%"); bg.style.setProperty("--clip-r", "0px"); return; }
        var p = GS.progress(scene);
        var grow = GS.clamp(p / 0.22, 0, 1), e = 1 - Math.pow(1 - grow, 3);
        bg.style.setProperty("--clip-y", ((1 - e) * 14).toFixed(2) + "%");
        bg.style.setProperty("--clip-x", ((1 - e) * 22).toFixed(2) + "%");
        bg.style.setProperty("--clip-r", ((1 - e) * 14).toFixed(1) + "px");
        bg.style.setProperty("--p", p.toFixed(3));
        var q = GS.clamp((p - 0.22) / 0.78, 0, 0.999);
        set(Math.floor(q * cards.length));
      });
    });
  });

  GS.register("floaters", function (ctx) {
    GS.qsa("[data-floaters]", ctx).forEach(function (sec) {
      if (sec._gs) return; sec._gs = true;
      if (GS.reducedMotion()) return;
      sec.classList.add("floaters--scroll");
      var scene = GS.qs(".floaters__scene", sec), layers = GS.qsa("[data-float-speed]", sec);
      GS.onScroll(function () {
        if (!GS.isDesktop()) { layers.forEach(function (l) { l.style.transform = ""; }); return; }
        var p = GS.progress(scene);
        layers.forEach(function (l) {
          var s = parseFloat(l.getAttribute("data-float-speed"));
          l.style.transform = "translate3d(" + ((0.5 - p) * s * w.innerWidth).toFixed(1) + "px," + ((0.5 - p) * s * 160).toFixed(1) + "px,0)";
        });
      });
    });
  });

  GS.register("featureCarousel", function (ctx) {
    GS.qsa("[data-fcarousel]", ctx).forEach(function (car) {
      if (car._gs) return; car._gs = true;
      var track = GS.qs(".fcarousel__track", car), slides = GS.qsa(".fcarousel__slide", car), bgs = GS.qsa(".fcarousel__bg", car);
      var status = GS.qs(".fcarousel__status", car), i = 0;
      function go(n) {
        i = GS.clamp(n, 0, slides.length - 1);
        var x = slides[i].offsetLeft - slides[0].offsetLeft;
        track.style.transform = "translate3d(" + (-x) + "px,0,0)";
        slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); s.setAttribute("aria-hidden", String(k !== i)); GS.qsa("a", s).forEach(function (a) { a.tabIndex = k === i ? 0 : -1; }); });
        bgs.forEach(function (b, k) { b.classList.toggle("is-active", k === i); });
        if (status) status.textContent = String(i + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
        GS.qsa("[data-fc-prev]", car).forEach(function (b) { b.disabled = i === 0; });
        GS.qsa("[data-fc-next]", car).forEach(function (b) { b.disabled = i === slides.length - 1; });
      }
      GS.qsa("[data-fc-prev]", car).forEach(function (b) { b.addEventListener("click", function () { go(i - 1); }); });
      GS.qsa("[data-fc-next]", car).forEach(function (b) { b.addEventListener("click", function () { go(i + 1); }); });
      slides.forEach(function (s, k) { s.addEventListener("click", function () { if (k !== i) go(k); }); });
      var x0 = null;
      track.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      track.addEventListener("touchend", function (e) { if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1)); x0 = null; });
      w.addEventListener("resize", function () { go(i); });
      go(0);
    });
  });
})(window, document, window.GS);
