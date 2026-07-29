(function () {
  "use strict";
  var root = document.documentElement;

  function isDark() { return root.getAttribute("data-theme") === "dark"; }

  function applyThemeColor() {
    var m = document.getElementById("meta-theme-color");
    if (m) m.setAttribute("content", isDark() ? "#0a0a0a" : "#fafafa");
  }

  function syncToggle(btn) {
    var dark = isDark();
    btn.setAttribute("aria-pressed", String(dark));
    btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  }

  /* Theme toggle (theme itself is already applied in the <head> to avoid a flash) */
  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    syncToggle(toggle);
    toggle.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      if (next === "dark") root.setAttribute("data-theme", "dark");
      else root.removeAttribute("data-theme");
      try { localStorage.setItem("site-theme", next); } catch (e) {}
      applyThemeColor();
      syncToggle(toggle);
    });
  }

  /* Mobile navigation disclosure */
  var navToggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("primary-nav");
  if (navToggle && nav) {
    var closeNav = function () {
      nav.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    };
    navToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
      if (open) {
        var first = nav.querySelector("a");
        if (first) first.focus();
      }
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeNav();
    });
    document.addEventListener("click", function (e) {
      if (nav.classList.contains("open") && !nav.contains(e.target) && !navToggle.contains(e.target)) closeNav();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        closeNav();
        navToggle.focus();
      }
    });
  }

  /* Scroll-spy: highlight the in-page nav link for the section in view */
  if ("IntersectionObserver" in window) {
    [".main-nav", ".side-nav"].forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (navEl) {
        var map = {};
        var targets = [];
        navEl.querySelectorAll('a[href^="#"]').forEach(function (a) {
          var id = a.getAttribute("href").slice(1);
          if (!id) return;
          var el = document.getElementById(id);
          if (el) { map[id] = a; targets.push(el); }
        });
        if (!targets.length) return;
        var spy = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting) return;
            Object.keys(map).forEach(function (k) {
              map[k].classList.remove("is-active");
              map[k].removeAttribute("aria-current");
            });
            map[en.target.id].classList.add("is-active");
            map[en.target.id].setAttribute("aria-current", "true");
          });
        }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
        targets.forEach(function (t) { spy.observe(t); });
      });
    });
  }

  /* Scroll-reveal (only when the user has not asked for reduced motion) */
  if ("IntersectionObserver" in window &&
      window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
    var revealSel = ".project-card, .snapshot-list article, .timeline-list article, " +
                    ".packet-card, .writing-list li, .metric-card, .stat";
    var ro = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("reveal-in"); obs.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    document.querySelectorAll(revealSel).forEach(function (el) {
      el.classList.add("reveal");
      ro.observe(el);
    });
  }

  /* Looping demo videos: play only when visible; skip on reduced-motion or data-saver */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  var vids = document.querySelectorAll("video[data-autoplay]");
  if (vids.length && !reduce && !saveData && "IntersectionObserver" in window) {
    var vo = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) en.target.play().catch(function () {});
        else en.target.pause();
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { vo.observe(v); });
  }

  /* Figure click-to-zoom (essays) */
  var figures = document.querySelectorAll(".essay-prose figure");
  if (figures.length) {
    var modal = document.createElement("div");
    modal.className = "figure-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "Enlarged figure");
    modal.hidden = true;
    var modalClose = document.createElement("button");
    modalClose.type = "button";
    modalClose.className = "figure-modal-close";
    modalClose.setAttribute("aria-label", "Close figure");
    modalClose.innerHTML = '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>';
    var modalInner = document.createElement("div");
    modalInner.className = "figure-modal-inner";
    modal.appendChild(modalClose);
    modal.appendChild(modalInner);
    document.body.appendChild(modal);

    var closeModal = function () {
      modal.hidden = true;
      modalInner.innerHTML = "";
      document.body.style.overflow = "";
      if (lastTrigger) lastTrigger.focus();
    };
    var lastTrigger = null;

    modalClose.addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !modal.hidden) closeModal();
    });

    figures.forEach(function (fig) {
      fig.classList.add("zoomable");
      fig.setAttribute("tabindex", "0");
      fig.setAttribute("role", "button");
      var obj = fig.querySelector("object[data]");
      var srcUrl = obj ? obj.getAttribute("data") : null;
      if (obj) {
        var label = obj.getAttribute("aria-label") || "Figure";
        fig.setAttribute("aria-label", "Zoom: " + label);
      }
      var openModal = function () {
        if (!srcUrl) return;
        lastTrigger = fig;
        modalInner.innerHTML = "";
        var img = document.createElement("img");
        img.src = srcUrl;
        img.alt = obj ? (obj.getAttribute("aria-label") || "Figure") : "Figure";
        modalInner.appendChild(img);
        var cap = fig.querySelector("figcaption");
        if (cap) {
          var capClone = document.createElement("p");
          capClone.className = "figure-modal-caption";
          capClone.textContent = cap.textContent;
          modalInner.appendChild(capClone);
        }
        var link = document.createElement("a");
        link.href = srcUrl;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = "Open full-size SVG";
        link.className = "figure-modal-link";
        modalInner.appendChild(link);
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        modalClose.focus();
      };
      fig.addEventListener("click", openModal);
      fig.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openModal(); }
      });
    });
  }

  /* Footer year */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
})();
