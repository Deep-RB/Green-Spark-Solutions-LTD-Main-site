/* ==========================================================================
   Navigation: sticky chrome (solid on scroll, hides on scroll down, returns on
   scroll up), "What We Do" / "Projects in pipeline" mega dropdowns (mouse,
   touch, keyboard), mobile off-canvas menu with focus trap, footer accordion.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("chrome", function () {
    var chrome = GS.qs("[data-site-chrome]");
    if (!chrome || chrome._gs) return; chrome._gs = true;
    var spacer = GS.qs(".site-chrome__spacer");
    var lastY = w.pageYOffset, threshold = 40;
    function measure() { if (spacer) spacer.style.height = chrome.offsetHeight + "px"; }
    measure(); w.addEventListener("resize", measure);
    GS.onScroll(function (y) {
      var menuOpen = chrome.classList.contains("menu-open") || GS.qs(".has-dropdown.is-open", chrome);
      chrome.classList.toggle("is-scrolled", y > threshold);
      if (!menuOpen) {
        if (y > lastY + 6 && y > 240) chrome.classList.add("is-hidden");
        else if (y < lastY - 6 || y < 240) chrome.classList.remove("is-hidden");
      }
      lastY = y;
    });
  });

  GS.register("dropdowns", function (ctx) {
    GS.qsa("[data-dropdown]", ctx).forEach(function (item) {
      if (item._gs) return; item._gs = true;
      var btn = GS.qs("[data-dropdown-toggle]", item), panel = GS.qs("[data-dropdown-panel]", item);
      if (!btn || !panel) return;
      var timer, hoverable = w.matchMedia("(hover: hover)").matches;
      function links() { return GS.qsa("a", panel); }
      function open(focusFirst) {
        GS.qsa("[data-dropdown].is-open").forEach(function (o) { if (o !== item) close.call(o); });
        item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); panel.removeAttribute("hidden");
        if (focusFirst) { var l = links()[0]; if (l) setTimeout(function () { l.focus(); }, 30); }
      }
      function close(returnFocus) {
        item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false");
        if (returnFocus) btn.focus();
      }
      item._close = close;
      btn.addEventListener("click", function () { item.classList.contains("is-open") ? close() : open(false); });
      btn.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); open(true); }
        if (e.key === "Escape") close(true);
      });
      panel.addEventListener("keydown", function (e) {
        var l = links(), i = l.indexOf(d.activeElement);
        if (e.key === "Escape") { e.preventDefault(); close(true); }
        if (e.key === "ArrowDown") { e.preventDefault(); (l[i + 1] || l[0]).focus(); }
        if (e.key === "ArrowUp") { e.preventDefault(); (l[i - 1] || l[l.length - 1]).focus(); }
      });
      if (hoverable) {
        item.addEventListener("mouseenter", function () { clearTimeout(timer); timer = setTimeout(function () { open(false); }, 90); });
        item.addEventListener("mouseleave", function () { clearTimeout(timer); timer = setTimeout(function () { close(); }, 220); });
      }
      item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
    });
    if (!d._gsDropdownDoc) {
      d._gsDropdownDoc = true;
      d.addEventListener("click", function (e) {
        GS.qsa("[data-dropdown].is-open").forEach(function (o) { if (!o.contains(e.target) && o._close) o._close(); });
      });
    }
  });

  GS.register("mobileMenu", function () {
    var menu = GS.qs("[data-mobile-menu]"), chrome = GS.qs("[data-site-chrome]");
    if (!menu || menu._gs) return; menu._gs = true;
    var openers = GS.qsa("[data-menu-open]"), release = null;
    function open() {
      menu.removeAttribute("hidden");
      requestAnimationFrame(function () { menu.classList.add("is-open"); });
      d.body.classList.add("is-locked"); if (chrome) chrome.classList.add("menu-open");
      openers.forEach(function (b) { b.setAttribute("aria-expanded", "true"); });
      release = GS.trapFocus(menu, { onEscape: close });
    }
    function close() {
      menu.classList.remove("is-open"); d.body.classList.remove("is-locked"); if (chrome) chrome.classList.remove("menu-open");
      openers.forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      if (release) { release(); release = null; }
      setTimeout(function () { if (!menu.classList.contains("is-open")) menu.setAttribute("hidden", ""); }, 520);
    }
    openers.forEach(function (b) { b.addEventListener("click", open); });
    GS.qsa("[data-menu-close]", menu).forEach(function (b) { b.addEventListener("click", close); });
    GS.qsa("a", menu).forEach(function (a) { a.addEventListener("click", function () { if (a.getAttribute("href").charAt(0) !== "#") close(); }); });
    GS.qsa("[data-submenu-toggle]", menu).forEach(function (t) {
      var sub = d.getElementById(t.getAttribute("aria-controls"));
      t.addEventListener("click", function () {
        var on = t.getAttribute("aria-expanded") !== "true";
        t.setAttribute("aria-expanded", String(on)); if (sub) sub.classList.toggle("is-open", on);
      });
    });
    w.addEventListener("resize", function () { if (w.innerWidth >= 1200 && menu.classList.contains("is-open")) close(); });
  });

  GS.register("footerAccordion", function () {
    GS.qsa("[data-footer-acc]").forEach(function (btn) {
      if (btn._gs) return; btn._gs = true;
      var panel = d.getElementById(btn.getAttribute("aria-controls"));
      btn.addEventListener("click", function () {
        var on = btn.getAttribute("aria-expanded") !== "true";
        btn.setAttribute("aria-expanded", String(on)); if (panel) panel.classList.toggle("is-open", on);
      });
    });
  });
})(window, document, window.GS);
