/* ==========================================================================
   Photo-card glow. Text under a photo card sits clean and transparent
   (outlined) and lights up in the logo green while the card is hovered,
   focused or tapped. Hooks: [data-glow] on the card; optional
   [data-glow-trigger] on the photo when only the photo should trigger it.
   Classic script, CSP-safe: it only toggles the .is-glowing class.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";

  GS.register("glow", function (ctx) {
    GS.qsa("[data-glow]", ctx).forEach(function (card) {
      if (card._gsGlow) return; card._gsGlow = true;
      var trigger = GS.qs("[data-glow-trigger]", card) || card;
      function on() { card.classList.add("is-glowing"); }
      function off() { card.classList.remove("is-glowing"); }

      trigger.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") on(); });
      trigger.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") off(); });
      card.addEventListener("focusin", on);
      card.addEventListener("focusout", function () { setTimeout(function () { if (!card.contains(d.activeElement)) off(); }, 0); });

      /* Touch: a tap lights this card and dims the one tapped before it */
      trigger.addEventListener("touchstart", function () {
        GS.qsa("[data-glow].is-glowing").forEach(function (c) { if (c !== card) c.classList.remove("is-glowing"); });
        on();
      }, { passive: true });
    });
  });
})(window, document, window.GS);
