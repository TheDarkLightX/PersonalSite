(function () {
  "use strict";
  var root = document.documentElement;

  function isDark() { return root.getAttribute("data-theme") === "dark"; }

  function applyThemeColor() {
    var m = document.getElementById("meta-theme-color");
    if (m) m.setAttribute("content", isDark() ? "#111715" : "#f4f7f5");
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

  /* Footer year */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
})();
