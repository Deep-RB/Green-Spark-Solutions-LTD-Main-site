/* ==========================================================================
   District map: tooltip on hover/focus for active districts, keyboard access,
   highlights the matching row in the list fallback. District names and status
   come from data-* attributes (filled by Django from the Area module).
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  GS.register("districtMap", function (ctx) {
    GS.qsa("[data-bd-map]", ctx).forEach(function (map) {
      if (map._gs) return; map._gs = true;
      var tip = GS.qs(".bd-map__tip", map), status = map.getAttribute("data-status-label") || "Programme active";
      function show(path) {
        if (!tip) return;
        var name = path.getAttribute("data-district");
        tip.textContent = "";
        var s = d.createElement("strong"); s.textContent = name; tip.appendChild(s);
        tip.appendChild(d.createTextNode(path.getAttribute("data-label") || status));
        var r = path.getBoundingClientRect(), m = map.getBoundingClientRect();
        tip.style.left = (r.left - m.left + r.width / 2) + "px";
        tip.style.top = (r.top - m.top) + "px";
        tip.classList.add("is-visible");
        GS.qsa("[data-district-row]", map.parentNode).forEach(function (li) { li.classList.toggle("is-hover", li.getAttribute("data-district-row") === name); });
      }
      function hide() { if (tip) tip.classList.remove("is-visible"); }
      GS.qsa("[data-map-district]", map).forEach(function (p) {
        p.addEventListener("mouseenter", function () { show(p); });
        p.addEventListener("mouseleave", hide);
        p.addEventListener("focus", function () { show(p); });
        p.addEventListener("blur", hide);
        p.addEventListener("click", function () { show(p); });
      });
      GS.qsa("[data-district-row]", map.parentNode).forEach(function (li) {
        li.addEventListener("mouseenter", function () {
          var p = GS.qs('[data-map-district][data-district="' + li.getAttribute("data-district-row") + '"]', map);
          if (p) { p.classList.add("is-hover"); show(p); }
        });
        li.addEventListener("mouseleave", function () { GS.qsa(".is-hover", map).forEach(function (p) { p.classList.remove("is-hover"); }); hide(); });
      });
    });
  });
})(window, document, window.GS);
