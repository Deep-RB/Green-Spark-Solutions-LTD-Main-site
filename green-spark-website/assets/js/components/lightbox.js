/* ==========================================================================
   Lightbox (gallery) — traps focus, close on Escape/backdrop,
   restore focus to the trigger, lock page scroll.
   Lightbox triggers: <a href="large.jpg" data-lightbox="album-id" data-caption="…">
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("lightbox", function (ctx) {
    var triggers = GS.qsa("[data-lightbox]", ctx).filter(function (t) { return !t._gs; });
    if (!triggers.length) return;
    var lb = GS.qs("[data-lightbox-root]");
    if (!lb) return;
    var img = GS.qs(".lightbox__img", lb), cap = GS.qs(".lightbox__caption", lb), cnt = GS.qs("[data-lb-count]", lb);
    var group = [], i = 0, release = null;
    function show(n) {
      i = (n + group.length) % group.length; var t = group[i];
      img.classList.add("is-loading");
      img.onload = function () { img.classList.remove("is-loading"); };
      img.src = t.getAttribute("href"); img.alt = t.getAttribute("data-alt") || (GS.qs("img", t) || {}).alt || "";
      cap.textContent = t.getAttribute("data-caption") || "";
      if (cnt) cnt.textContent = (i + 1) + " / " + group.length;
    }
    function open(t) {
      var name = t.getAttribute("data-lightbox");
      group = GS.qsa('[data-lightbox="' + name + '"]');
      lb.removeAttribute("hidden"); requestAnimationFrame(function () { lb.classList.add("is-open"); });
      d.body.classList.add("is-locked"); show(group.indexOf(t));
      release = GS.trapFocus(lb, { onEscape: close, initial: GS.qs("[data-lb-close]", lb) });
    }
    function close() {
      lb.classList.remove("is-open"); d.body.classList.remove("is-locked");
      if (release) { release(); release = null; }
      setTimeout(function () { if (!lb.classList.contains("is-open")) lb.setAttribute("hidden", ""); }, 420);
    }
    if (!lb._gs) {
      lb._gs = true;
      GS.qs("[data-lb-close]", lb).addEventListener("click", close);
      GS.qs("[data-lb-prev]", lb).addEventListener("click", function () { show(i - 1); });
      GS.qs("[data-lb-next]", lb).addEventListener("click", function () { show(i + 1); });
      lb.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
      lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lightbox__stage")) close(); });
    }
    triggers.forEach(function (t) { t._gs = true; t.addEventListener("click", function (e) { e.preventDefault(); open(t); }); });
  });
})(window, document, window.GS);
