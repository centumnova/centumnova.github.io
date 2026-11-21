(() => {
  const root = document.documentElement;
  const system = window.matchMedia("(prefers-color-scheme: dark)");
  const key = "centumnova-theme";
  let preference;
  let button;

  try {
    const saved = localStorage.getItem(key);
    if (saved === "dark" || saved === "light") preference = saved;
  } catch {
    // Theme selection still works when browser storage is unavailable.
  }

  function applyTheme() {
    const dark = preference ? preference === "dark" : system.matches;
    root.dataset.theme = dark ? "dark" : "light";
    button?.setAttribute("aria-pressed", String(dark));
  }

  applyTheme();
  system.addEventListener("change", applyTheme);
  document.addEventListener("DOMContentLoaded", () => {
    button = document.querySelector(".theme");
    button.addEventListener("click", () => {
      preference = root.dataset.theme === "dark" ? "light" : "dark";
      try {
        localStorage.setItem(key, preference);
      } catch {
        // The current page keeps the selected theme.
      }
      applyTheme();
    });
    applyTheme();
    button.hidden = false;
  });
})();
