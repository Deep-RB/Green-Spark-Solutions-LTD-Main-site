/* ==========================================================================
   Home video hero ([data-vhero]). Classic script, CSP-safe (CSSOM only).
   - Wide (16:9) or tall (9:16) cut chosen by screen shape, swapped on rotate.
   - Poster paints first (LCP); footage loads ~0.9 s later and fades in.
   - prefers-reduced-motion or Save-Data: poster only, the play button still works.
   - Pauses off screen and in background tabs; pause/play button (WCAG 2.2.2).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("videoHero", function (ctx) {
    GS.qsa("[data-vhero]", ctx).forEach(function (hero) {
      if (hero._gs) return; hero._gs = true;
      var video = GS.qs("video", hero), btn = GS.qs(".gs-vhero__toggle", hero);
      if (!video || !btn) return;
      var tallMQ = w.matchMedia("(max-aspect-ratio: 4/5)");
      var userPaused = GS.reducedMotion() || GS.saveData();
      var inView = true, variant = null, ready = false;

      // Title words rise in one by one (stagger set through CSSOM, not inline HTML)
      GS.qsa(".gs-vhero__title", hero).forEach(function (title) {
        if (title._split) return; title._split = true;
        var words = title.textContent.trim().split(/\s+/);
        title.textContent = "";
        words.forEach(function (word, i) {
          var outer = d.createElement("span"), inner = d.createElement("span");
          outer.className = "w"; inner.textContent = word; inner.style.setProperty("--i", i);
          outer.appendChild(inner); title.appendChild(outer);
          if (i < words.length - 1) title.appendChild(d.createTextNode(" "));
        });
      });

      function load(v) {
        if (v === variant) return;
        var t = video.currentTime || 0;
        variant = v;
        while (video.firstChild) video.removeChild(video.firstChild);
        var canWebm = video.canPlayType('video/webm; codecs="vp9"');
        [["Webm", "video/webm"], ["Mp4", "video/mp4"]].forEach(function (f) {
          var src = video.getAttribute("data-" + v + "-" + f[0].toLowerCase());
          if (!src || (f[0] === "Webm" && !canWebm)) return;
          var s = d.createElement("source"); s.src = src; s.type = f[1]; video.appendChild(s);
        });
        video.preload = "auto";
        video.load();
        if (t) video.addEventListener("loadedmetadata", function once() { video.currentTime = t; video.removeEventListener("loadedmetadata", once); });
      }
      function ui() {
        btn.hidden = false;
        btn.setAttribute("aria-pressed", String(userPaused));
        btn.setAttribute("aria-label", userPaused ? "Play background video" : "Pause background video");
      }
      function sync() {
        if (!ready) return;
        if (!userPaused && inView && !d.hidden) {
          load(tallMQ.matches ? "tall" : "wide");
          var p = video.play();
          if (p && p.catch) p.catch(function () { userPaused = true; ui(); });   // autoplay blocked (e.g. iOS Low Power)
        } else if (!video.paused) video.pause();
        ui();
      }

      video.addEventListener("playing", function () { video.classList.add("is-playing"); });
      btn.addEventListener("click", function () { userPaused = !userPaused; sync(); });
      var onShape = function () { if (variant) { load(tallMQ.matches ? "tall" : "wide"); sync(); } };
      if (tallMQ.addEventListener) tallMQ.addEventListener("change", onShape); else if (tallMQ.addListener) tallMQ.addListener(onShape);
      d.addEventListener("visibilitychange", sync);
      if ("IntersectionObserver" in w) {
        new IntersectionObserver(function (e) { inView = e[0].isIntersecting; sync(); }, { threshold: 0.05 }).observe(hero);
      }
      requestAnimationFrame(function () { hero.classList.add("is-loaded"); });
      setTimeout(function () { ready = true; sync(); }, GS.reducedMotion() ? 0 : 900);
    });
  });
})(window, document, window.GS);
