/* ==========================================================================
   Media: looping programme animations, the Meet GSSL video modal and the
   pointer tilt on collage cards. Classic script, CSP-safe.
   - video[data-loop-video]: muted, looping, decorative. Plays only while on
     screen and only when motion is allowed; otherwise the poster frame shows.
   - [data-video-modal]: plays its video when the modal opens, pauses on close.
   - [data-tilt]: card leans towards the pointer (fine pointers only).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  function tryPlay(v) {
    if (v.preload !== "auto") { v.preload = "auto"; }
    var p = v.play(); if (p && p.catch) p.catch(function () { /* autoplay refused: poster stays */ });
  }

  GS.register("loopVideo", function (ctx) {
    var vids = GS.qsa("video[data-loop-video]", ctx).filter(function (v) { return !v._gs; });
    if (!vids.length) return;
    vids.forEach(function (v) { v._gs = true; v.muted = true; });
    if (GS.reducedMotion() || GS.saveData()) return;               // keep the still poster
    if (!("IntersectionObserver" in w)) { vids.forEach(tryPlay); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) tryPlay(v); else if (!v.paused) v.pause();
      });
    }, { rootMargin: "120px 0px" });
    vids.forEach(function (v) { io.observe(v); });
  });

  GS.register("videoModal", function (ctx) {
    GS.qsa("[data-video-modal]", d).forEach(function (m) {
      if (m._gsv) return; m._gsv = true;
      var v = GS.qs("video", m); if (!v) return;
      new MutationObserver(function () {
        if (m.classList.contains("is-open")) { v.preload = "auto"; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else if (!v.paused) v.pause();
      }).observe(m, { attributes: true, attributeFilter: ["class"] });
    });
  });

  GS.register("tilt", function (ctx) {
    if (GS.reducedMotion() || !w.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    GS.qsa("[data-tilt]", ctx).forEach(function (el) {
      if (el._gst) return; el._gst = true;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        el.style.setProperty("--rx", (x * 7).toFixed(2) + "deg");
        el.style.setProperty("--ry", (-y * 7).toFixed(2) + "deg");
      });
      el.addEventListener("pointerleave", function () { el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg"); });
    });
  });
})(window, document, window.GS);
