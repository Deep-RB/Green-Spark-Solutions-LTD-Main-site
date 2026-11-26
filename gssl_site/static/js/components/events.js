/* ==========================================================================
   Events: status computed from dates, card filters, countdown.
   Dates are ISO (YYYY-MM-DD or full ISO with offset) in data-* attributes:
     data-event-status data-start data-end data-feedback-start data-feedback-end
   Status:  Upcoming → (Open for feedback) → Closed
   Django should compute the same status server-side; JS only keeps the badge
   correct for cached pages.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  var LABEL = { upcoming: "Upcoming", feedback: "Open for feedback", closed: "Closed", today: "Happening today" };
  var day = GS.day = function (s, end) { if (!s) return null; var t = s.length <= 10 ? s + (end ? "T23:59:59" : "T00:00:00") : s; return new Date(t); };
  GS.now = function () { var o = d.body.classList.contains("is-preview") && d.body.getAttribute("data-now"); return o ? new Date(o) : new Date(); };
  GS.eventStatus = function (el) {
    var now = GS.now(), st = day(el.getAttribute("data-start")), en = day(el.getAttribute("data-end") || el.getAttribute("data-start"), true);
    var fs = day(el.getAttribute("data-feedback-start")), fe = day(el.getAttribute("data-feedback-end"), true);
    if (fs && fe && now >= fs && now <= fe) return "feedback";
    if (st && now < st) return "upcoming";
    if (st && en && now >= st && now <= en) return "today";
    return "closed";
  };

  GS.register("eventStatus", function (ctx) {
    GS.qsa("[data-event-status]", ctx).forEach(function (b) {
      var s = GS.eventStatus(b);
      b.className = "badge badge--" + (s === "today" ? "upcoming" : s) + (b.classList.contains("badge--lg") ? " badge--lg" : "");
      b.textContent = LABEL[s];
      var card = b.closest("[data-event-card]"); if (card) { card.setAttribute("data-status", s); card.classList.toggle("is-past", s === "closed"); }
    });
  });

  /* Filter chips / tabs over event + project cards */
  GS.register("cardFilters", function (ctx) {
    GS.qsa("[data-filter-group]", ctx).forEach(function (group) {
      if (group._gs) return; group._gs = true;
      var target = d.getElementById(group.getAttribute("data-filter-group")); if (!target) return;
      var empty = GS.qs("[data-filter-empty]", target.parentNode), live = GS.qs("[data-filter-live]", target.parentNode);
      GS.qsa("[data-filter]", group).forEach(function (chip) {
        chip.addEventListener("click", function () {
          GS.qsa("[data-filter]", group).forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
          var f = chip.getAttribute("data-filter"), n = 0;
          GS.qsa("[data-filter-item]", target).forEach(function (item) {
            var keys = (item.getAttribute("data-filter-item") + " " + (item.querySelector("[data-status]") || item).getAttribute("data-status")).split(" ");
            var show = f === "all" || keys.indexOf(f) > -1; item.hidden = !show; if (show) n++;
          });
          if (empty) empty.hidden = n > 0;
          if (live) live.textContent = n + (n === 1 ? " item" : " items") + " shown";
        });
      });
    });
  });

  /* Countdown to the end of a feedback window */
  GS.register("countdown", function (ctx) {
    GS.qsa("[data-countdown]", ctx).forEach(function (el) {
      if (el._gs) return; el._gs = true;
      var end = day(el.getAttribute("data-countdown"), true), parts = GS.qsa("b", el), offset = GS.now() - new Date();
      function tick() {
        var ms = Math.max(0, end - (new Date().getTime() + offset)), s = Math.floor(ms / 1000);
        var v = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
        parts.forEach(function (p, k) { p.textContent = String(v[k]).padStart(2, "0"); });
      }
      tick(); setInterval(tick, 1000);
    });
  });
})(window, document, window.GS);
