(function () {
  const root = document.documentElement;
  const stored = localStorage.getItem("site-theme");
  if (stored === "dark") root.setAttribute("data-theme", "dark");

  const toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      if (next === "dark") {
        root.setAttribute("data-theme", "dark");
        localStorage.setItem("site-theme", "dark");
      } else {
        root.removeAttribute("data-theme");
        localStorage.setItem("site-theme", "light");
      }
    });
  }

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
})();
