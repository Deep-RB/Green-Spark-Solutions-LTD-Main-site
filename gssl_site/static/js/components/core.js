/* ==========================================================================
   GS core: namespace, helpers, focus trap, scroll loop. Classic script (works
   from file:// and under a strict CSP: no inline handlers, no eval).
   ========================================================================== */
(function (w, d) {
  "use strict";
  var root = d.documentElement;
  root.classList.remove("no-js");
  root.classList.add("js");

  var GS = w.GS = w.GS || {};
  GS.modules = GS.modules || {};

  GS.qs = function (sel, ctx) { return (ctx || d).querySelector(sel); };
  GS.qsa = function (sel, ctx) { return Array.prototype.slice.call((ctx || d).querySelectorAll(sel)); };
  GS.clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  GS.reducedMotion = function () { return w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches; };
  GS.saveData = function () { var c = navigator.connection; return !!(c && (c.saveData || /2g/.test(c.effectiveType || ""))); };
  GS.isDesktop = function () { return w.matchMedia("(min-width: 992px)").matches; };

  /* Storage is optional: the preview build sets data-storage="off" on <body>. */
  GS.store = {
    get: function (k) { if (d.body.getAttribute("data-storage") === "off") return null; try { return w.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { if (d.body.getAttribute("data-storage") === "off") return; try { w.localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  };

  /* Register + boot modules: GS.register("name", fn(ctx)) ; GS.boot(ctx) */
  GS.register = function (name, fn) { GS.modules[name] = fn; };
  GS.boot = function (ctx) {
    Object.keys(GS.modules).forEach(function (k) {
      try { GS.modules[k](ctx || d); } catch (e) { if (w.console) console.warn("[GS] " + k, e); }
    });
  };

  /* Focus trap for dialogs, lightbox and the mobile menu */
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  GS.trapFocus = function (container, opts) {
    opts = opts || {};
    var prev = d.activeElement;
    function items() { return GS.qsa(FOCUSABLE, container).filter(function (el) { return el.offsetParent !== null || el === d.activeElement; }); }
    function onKey(e) {
      if (e.key === "Escape" && opts.onEscape) { e.preventDefault(); opts.onEscape(); return; }
      if (e.key !== "Tab") return;
      var f = items(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    container.addEventListener("keydown", onKey);
    var f0 = opts.initial || items()[0];
    if (f0) setTimeout(function () { f0.focus({ preventScroll: true }); }, 60);
    return function release() {
      container.removeEventListener("keydown", onKey);
      if (prev && prev.focus) prev.focus({ preventScroll: true });
    };
  };

  /* Shared rAF scroll loop: GS.onScroll(fn(scrollY)) */
  var subs = [], ticking = false;
  function run() { ticking = false; var y = w.pageYOffset; for (var i = 0; i < subs.length; i++) subs[i](y); }
  function req() { if (!ticking) { ticking = true; w.requestAnimationFrame(run); } }
  w.addEventListener("scroll", req, { passive: true });
  w.addEventListener("resize", req);
  GS.onScroll = function (fn) { subs.push(fn); req(); };
  GS.refresh = req;

  /* Progress of an element through the viewport (0 → 1) */
  GS.progress = function (el, startOffset) {
    var r = el.getBoundingClientRect(), vh = w.innerHeight;
    var total = r.height - (startOffset != null ? startOffset : vh);
    if (total <= 0) total = r.height;
    return GS.clamp(-r.top / total, 0, 1);
  };

  /* Toast helper */
  GS.toast = function (msg, type) {
    var region = GS.qs(".toast-region");
    if (!region) { region = d.createElement("div"); region.className = "toast-region"; region.setAttribute("role", "status"); region.setAttribute("aria-live", "polite"); d.body.appendChild(region); }
    var t = d.createElement("div");
    t.className = "toast" + (type === "error" ? " toast--error" : "");
    var p = d.createElement("p"); p.textContent = msg;
    var icon = d.createElementNS("http://www.w3.org/2000/svg", "svg");
    icon.setAttribute("class", "icon"); icon.setAttribute("viewBox", "0 0 24 24"); icon.setAttribute("aria-hidden", "true");
    var path = d.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", type === "error" ? "M12 4 21 19.5H3zM12 10v4M12 16.8v.2" : "m5 12.5 4.5 4.5L19 7.5");
    icon.appendChild(path);
    var close = d.createElement("button"); close.className = "toast__close"; close.type = "button"; close.setAttribute("aria-label", "Dismiss"); close.textContent = "×";
    t.appendChild(icon); t.appendChild(p); t.appendChild(close);
    region.appendChild(t);
    function bye() { t.classList.add("is-leaving"); setTimeout(function () { t.remove(); }, 320); }
    close.addEventListener("click", bye);
    setTimeout(bye, 5200);
  };
})(window, document);
