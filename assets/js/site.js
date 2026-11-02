/* el-pro.cz – přepínač vzhledu (tmavý výchozí) a menu na mobilu. */
(function () {
  var root = document.documentElement;
  var KEY = "elpro-theme";

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#0D1B26" : "#FFFFFF");
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      var dark = theme === "dark";
      btn.setAttribute("aria-pressed", dark ? "false" : "true");
      btn.setAttribute("aria-label", dark ? "Přepnout na světlý vzhled" : "Přepnout na tmavý vzhled");
      btn.setAttribute("title", dark ? "Světlý vzhled" : "Tmavý vzhled");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(root.getAttribute("data-theme") === "light" ? "light" : "dark");

    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
        applyTheme(next);
        try { localStorage.setItem(KEY, next); } catch (e) { /* soukromé okno – volba platí jen pro tuto stránku */ }
      });
    });

    var header = document.querySelector(".site-header");
    var menuBtn = document.querySelector("[data-menu-toggle]");
    if (header && menuBtn) {
      menuBtn.addEventListener("click", function () {
        var open = !header.classList.contains("is-open");
        header.classList.toggle("is-open", open);
        menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && header.classList.contains("is-open")) {
          header.classList.remove("is-open");
          menuBtn.setAttribute("aria-expanded", "false");
          menuBtn.focus();
        }
      });
    }
  });
})();
