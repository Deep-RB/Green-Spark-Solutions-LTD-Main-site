/* ==========================================================================
   Forms: client-side validation (required, email, phone, length, file type /
   size), honeypot, sending → success / error states, character counters,
   file-upload list, event pre-fill on the feedback form.
   • POST only — nothing is ever put in the URL.
   • data-ajax  → submits with fetch() and expects JSON {ok:true} or
                  {ok:false, errors:{field:"msg"}} (Django view returns this).
   • data-demo="success|error" → design preview only: simulates the server.
   ========================================================================== */
(function (w, d, GS) {
  "use strict";
  var MSG = {
    required: "This field is required.",
    email: "Enter a valid email address, for example name@example.com.",
    phone: "Enter a valid phone number, including the country code.",
    min: "Please write at least {n} characters.",
    file: "Files must be PDF, JPG or PNG and no larger than {n} MB.",
    consent: "Please confirm before sending."
  };

  function fieldOf(el) { return el.closest(".field") || el.parentNode; }
  function setError(el, msg) {
    var f = fieldOf(el), err = GS.qs(".field__error", f);
    f.classList.toggle("is-invalid", !!msg); f.classList.toggle("is-valid", !msg && el.value !== "");
    el.setAttribute("aria-invalid", msg ? "true" : "false");
    if (err) { var t = GS.qs("[data-error-text]", err) || err; t.textContent = msg || ""; }
  }
  function validate(el) {
    if (el.disabled || el.type === "hidden" || el.closest(".hp-field")) return true;
    var v = (el.type === "checkbox" || el.type === "radio") ? null : el.value.trim(), msg = "";
    if (el.type === "checkbox" && el.required && !el.checked) msg = el.getAttribute("data-msg") || MSG.consent;
    else if (el.type === "radio" && el.required) {
      var any = GS.qsa('input[name="' + el.name + '"]', el.form).some(function (r) { return r.checked; });
      if (!any) msg = MSG.required;
    }
    else if (el.type === "file") {
      var max = parseFloat(el.getAttribute("data-max-mb") || "10"), ok = true;
      Array.prototype.forEach.call(el.files || [], function (f) { if (f.size > max * 1048576 || !/\.(pdf|jpe?g|png)$/i.test(f.name)) ok = false; });
      if (el.required && !(el.files && el.files.length)) msg = MSG.required; else if (!ok) msg = MSG.file.replace("{n}", max);
    }
    else if (el.required && !v) msg = el.getAttribute("data-msg") || MSG.required;
    else if (v && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = MSG.email;
    else if (v && el.type === "tel" && !/^\+?[\d\s\-()]{7,20}$/.test(v)) msg = MSG.phone;
    else if (v && el.minLength > 0 && v.length < el.minLength) msg = MSG.min.replace("{n}", el.minLength);
    setError(el, msg);
    return !msg;
  }

  GS.register("forms", function (ctx) {
    GS.qsa("form[data-validate]", ctx).forEach(function (form) {
      if (form._gs) return; form._gs = true;
      form.setAttribute("novalidate", "");
      var fields = GS.qsa("input, textarea, select", form).filter(function (el) { return el.name && !el.closest(".hp-field"); });
      fields.forEach(function (el) {
        el.addEventListener("blur", function () { if (el.value || fieldOf(el).classList.contains("is-invalid")) validate(el); });
        el.addEventListener("input", function () { if (fieldOf(el).classList.contains("is-invalid")) validate(el); });
        el.addEventListener("change", function () { if (el.type === "checkbox" || el.type === "radio" || el.type === "file" || el.tagName === "SELECT") validate(el); });
      });
      // character counters
      GS.qsa("textarea[maxlength]", form).forEach(function (ta) {
        var c = GS.qs("[data-count-for='" + ta.id + "']", form); if (!c) return;
        var upd = function () { c.textContent = ta.value.length + " / " + ta.maxLength; }; ta.addEventListener("input", upd); upd();
      });
      // file list
      GS.qsa(".upload input[type=file]", form).forEach(function (inp) {
        var up = inp.closest(".upload"), list = GS.qs(".upload__files", up);
        ["dragenter", "dragover"].forEach(function (t) { up.addEventListener(t, function () { up.classList.add("is-dragover"); }); });
        ["dragleave", "drop"].forEach(function (t) { up.addEventListener(t, function () { up.classList.remove("is-dragover"); }); });
        inp.addEventListener("change", function () {
          if (!list) return; list.textContent = "";
          Array.prototype.forEach.call(inp.files, function (f) {
            var li = d.createElement("li"), a = d.createElement("span"), b = d.createElement("span");
            a.textContent = f.name; b.textContent = (f.size / 1048576).toFixed(1) + " MB"; li.appendChild(a); li.appendChild(b); list.appendChild(li);
          });
        });
      });
      var btn = GS.qs("[type=submit]", form);
      function state(s) {
        form.setAttribute("data-state", s);
        if (btn) { btn.classList.toggle("is-loading", s === "sending"); btn.disabled = s === "sending"; }
        var box = GS.qs(".form-status--" + s, form); if (box) { box.setAttribute("tabindex", "-1"); box.focus({ preventScroll: false }); }
      }
      GS.qsa("[data-form-reset]", form).forEach(function (r) { r.addEventListener("click", function () { form.reset(); fields.forEach(function (f) { fieldOf(f).classList.remove("is-valid", "is-invalid"); }); form.removeAttribute("data-state"); }); });
      form.addEventListener("submit", function (e) {
        var hp = GS.qs(".hp-field input", form);
        var ok = fields.map(validate).every(Boolean);
        if (!ok) {
          e.preventDefault();
          var first = GS.qs(".is-invalid input, .is-invalid textarea, .is-invalid select", form); if (first) first.focus();
          var sum = GS.qs("[data-error-summary]", form);
          if (sum) { sum.hidden = false; GS.qs("[data-error-count]", sum).textContent = GS.qsa(".field.is-invalid", form).length; }
          return;
        }
        var sum2 = GS.qs("[data-error-summary]", form); if (sum2) sum2.hidden = true;
        if (hp && hp.value) { e.preventDefault(); state("success"); return; } // bot: pretend success, send nothing
        var demo = form.getAttribute("data-demo");
        if (demo) { e.preventDefault(); state("sending"); setTimeout(function () { state(demo === "error" ? "error" : "success"); if (demo !== "error") GS.toast("Thank you — your message has been sent."); }, 1300); return; }
        if (form.hasAttribute("data-ajax") && w.fetch) {
          e.preventDefault(); state("sending");
          fetch(form.action, { method: "POST", body: new FormData(form), headers: { "X-Requested-With": "XMLHttpRequest", "Accept": "application/json" }, credentials: "same-origin" })
            .then(function (r) { return r.json(); })
            .then(function (j) {
              if (j.ok) { state("success"); return; }
              Object.keys(j.errors || {}).forEach(function (k) { var el = form.elements[k]; if (el && el.nodeType) setError(el, j.errors[k]); });
              state("error");
            }).catch(function () { state("error"); });
        }
      });
    });

    /* Feedback form: pre-select the event from the link (#event=slug). The
       hash never reaches the server; Django should pre-fill server-side from
       the URL path /events/<slug>/feedback/ instead. */
    GS.qsa("[data-prefill-event]", ctx).forEach(function (sel) {
      var m = /event=([\w-]+)/.exec(w.location.hash || ""); if (!m) return;
      var opt = GS.qs('option[value="' + m[1] + '"]', sel); if (opt) { sel.value = m[1]; sel.dispatchEvent(new Event("change")); }
    });
  });
})(window, document, window.GS);
