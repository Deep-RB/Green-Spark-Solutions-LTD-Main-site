/* ==========================================================================
   Hero slider: crossfade + Ken Burns, dots with progress, prev/next, pause.
   Pauses on hover/focus, when the tab is hidden, and never autoplays with
   prefers-reduced-motion. Image-only slides show the .hero__fallback copy.
   Optional CMS video per slide: <video data-hero-video data-src="…mp4">
   (desktop only, not on Save-Data, not with reduced motion).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  function splitWords(el) {
    if (!el || el._split) return; el._split = true;
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    words.forEach(function (word, i) {
      var o = d.createElement("span"); o.className = "w";
      var inner = d.createElement("span"); inner.textContent = word;
      inner.style.transitionDelay = (0.08 * i + 0.25) + "s";
      o.appendChild(inner); el.appendChild(o);
      if (i < words.length - 1) el.appendChild(d.createTextNode(" "));
    });
  }

  GS.register("heroSlider", function (ctx) {
    GS.qsa("[data-hero-slider]", ctx).forEach(function (hero) {
      if (hero._gs) return; hero._gs = true;
      var slides = GS.qsa("[data-slide]", hero);
      var contents = GS.qsa("[data-slide-content]", hero);
      var dots = GS.qsa("[data-slide-dot]", hero);
      var count = GS.qs("[data-slide-count]", hero);
      var pauseBtn = GS.qs("[data-slider-pause]", hero);
      var reduce = GS.reducedMotion(), i = 0, timer = null, paused = reduce, hovering = false;
      var interval = 7000;
      GS.qsa(".hero__title", hero).forEach(splitWords);
      if (reduce) hero.classList.add("is-static", "is-paused");
      requestAnimationFrame(function () { setTimeout(function () { hero.classList.add("is-loaded"); }, 80); });

      function loadVideo(slide) {
        var v = GS.qs("video[data-hero-video]", slide);
        if (!v || reduce || GS.saveData() || !GS.isDesktop()) return;
        if (!v.src && v.getAttribute("data-src")) { v.src = v.getAttribute("data-src"); }
        var p = v.play(); if (p && p.then) p.then(function () { v.classList.add("is-playing"); }).catch(function () {});
      }
      function stopVideo(slide) { var v = GS.qs("video[data-hero-video]", slide); if (v && !v.paused) v.pause(); }

      function go(n, user) {
        var prev = i; i = (n + slides.length) % slides.length;
        slides.forEach(function (s, k) {
          var on = k === i; s.classList.toggle("is-active", on); s.setAttribute("aria-hidden", String(!on));
          GS.qsa("a, button", s).forEach(function (el) { el.tabIndex = on ? 0 : -1; });
        });
        var has = false;
        contents.forEach(function (c) { var on = +c.getAttribute("data-slide-content") === i; c.classList.toggle("is-active", on); if (on) has = true; });
        hero.setAttribute("data-active-has-content", String(has));
        dots.forEach(function (dot, k) {
          if (k === i) { dot.setAttribute("aria-current", "true"); var c = dot.cloneNode(true); dot.parentNode.replaceChild(c, dot); dots[k] = c; bindDot(c, k); }
          else dot.removeAttribute("aria-current");
        });
        if (count) count.textContent = String(i + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
        if (prev !== i) stopVideo(slides[prev]);
        loadVideo(slides[i]);
        if (user) restart();
      }
      function tick() { go(i + 1); }
      function restart() { clearInterval(timer); if (!paused && !hovering) timer = setInterval(tick, interval); }
      function bindDot(dot, k) { dot.addEventListener("click", function () { go(k, true); }); }
      dots.forEach(bindDot);
      GS.qsa("[data-slide-prev]", hero).forEach(function (b) { b.addEventListener("click", function () { go(i - 1, true); }); });
      GS.qsa("[data-slide-next]", hero).forEach(function (b) { b.addEventListener("click", function () { go(i + 1, true); }); });
      if (pauseBtn) pauseBtn.addEventListener("click", function () {
        paused = !paused; hero.classList.toggle("is-paused", paused);
        pauseBtn.setAttribute("aria-label", paused ? "Play slideshow" : "Pause slideshow");
        pauseBtn.setAttribute("aria-pressed", String(paused));
        if (!paused) hero.classList.remove("is-static");
        restart();
      });
      hero.addEventListener("mouseenter", function () { hovering = true; hero.classList.add("is-paused"); clearInterval(timer); });
      hero.addEventListener("mouseleave", function () { hovering = false; if (!paused) hero.classList.remove("is-paused"); restart(); });
      hero.addEventListener("focusin", function () { hovering = true; clearInterval(timer); hero.classList.add("is-paused"); });
      hero.addEventListener("focusout", function (e) { if (!hero.contains(e.relatedTarget)) { hovering = false; if (!paused) hero.classList.remove("is-paused"); restart(); } });
      hero.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") go(i + 1, true); if (e.key === "ArrowLeft") go(i - 1, true); });
      d.addEventListener("visibilitychange", function () { if (d.hidden) clearInterval(timer); else restart(); });
      // touch swipe
      var x0 = null;
      hero.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      hero.addEventListener("touchend", function (e) { if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1), true); x0 = null; });
      go(0); restart();
    });
  });
})(window, document, window.GS);
