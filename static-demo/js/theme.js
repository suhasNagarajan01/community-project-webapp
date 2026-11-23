/**
 * Static Demo Theme Controller
 * Handles 1-click switching between Emerald Green & White and Warm Earth & Beige,
 * plus Dark/Light mode, with persistence in localStorage.
 */
(function () {
  const THEME_KEY = 'static_demo_theme';
  const MODE_KEY = 'static_demo_mode';

  function init() {
    const html = document.documentElement;
    const meta = document.querySelector('meta[name="color-scheme"]');
    
    let theme = localStorage.getItem(THEME_KEY) || 'green';
    let mode = localStorage.getItem(MODE_KEY) || 'light';

    apply(theme, mode);
  }

  function apply(theme, mode) {
    const html = document.documentElement;
    const meta = document.querySelector('meta[name="color-scheme"]');

    html.setAttribute('data-theme', theme);
    html.setAttribute('data-mode', mode);
    html.setAttribute('data-bs-theme', mode === 'dark' ? 'dark' : 'light');

    if (meta) {
      meta.setAttribute('content', mode === 'dark' ? 'dark' : (mode === 'light' ? 'light' : 'light dark'));
    }

    localStorage.setItem(THEME_KEY, theme);
    localStorage.setItem(MODE_KEY, mode);
  }

  window.DemoTheme = {
    setTheme: function (theme) {
      const mode = localStorage.getItem(MODE_KEY) || 'light';
      apply(theme, mode);
    },
    toggleMode: function () {
      const theme = localStorage.getItem(THEME_KEY) || 'green';
      const currentMode = localStorage.getItem(MODE_KEY) || 'light';
      const newMode = currentMode === 'dark' ? 'light' : 'dark';
      apply(theme, newMode);
    }
  };

  init();
})();
