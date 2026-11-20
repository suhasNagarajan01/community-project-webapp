/**
 * Daily Wage Platform Theme & Mode Controller
 * Handles dual themes (Emerald Green vs Warm Earth Beige) and Dark/Light mode
 */
(function () {
  const STORAGE_THEME_KEY = 'dailywage_theme_pref';
  const STORAGE_MODE_KEY = 'dailywage_mode_pref';

  function initTheme() {
    const html = document.documentElement;
    const metaColorScheme = document.querySelector('meta[name="color-scheme"]');

    // Read stored or server-rendered values
    let theme = localStorage.getItem(STORAGE_THEME_KEY) || html.getAttribute('data-theme') || 'green';
    let mode = localStorage.getItem(STORAGE_MODE_KEY) || html.getAttribute('data-mode') || 'light';

    applyTheme(theme, mode);
  }

  function applyTheme(theme, mode) {
    const html = document.documentElement;
    const metaColorScheme = document.querySelector('meta[name="color-scheme"]');

    html.setAttribute('data-theme', theme);
    html.setAttribute('data-mode', mode);

    if (metaColorScheme) {
      metaColorScheme.setAttribute('content', mode === 'dark' ? 'dark' : (mode === 'light' ? 'light' : 'light dark'));
    }

    localStorage.setItem(STORAGE_THEME_KEY, theme);
    localStorage.setItem(STORAGE_MODE_KEY, mode);

    // Update active indicators on any theme toggles in UI
    document.querySelectorAll('[data-theme-btn]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-theme-btn') === theme);
    });

    document.querySelectorAll('[data-mode-btn]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-mode-btn') === mode);
    });
  }

  // Expose global controller
  window.DailyWageTheme = {
    setTheme: function (theme) {
      const mode = localStorage.getItem(STORAGE_MODE_KEY) || document.documentElement.getAttribute('data-mode') || 'light';
      applyTheme(theme, mode);
      // Persist to server if logged in
      fetch('/accounts/toggle-theme/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCsrfToken(),
        },
        body: `theme=${encodeURIComponent(theme)}&mode=${encodeURIComponent(mode)}`
      }).catch(err => console.debug('Theme sync:', err));
    },

    toggleMode: function () {
      const theme = localStorage.getItem(STORAGE_THEME_KEY) || document.documentElement.getAttribute('data-theme') || 'green';
      const currentMode = localStorage.getItem(STORAGE_MODE_KEY) || document.documentElement.getAttribute('data-mode') || 'light';
      const newMode = currentMode === 'dark' ? 'light' : 'dark';
      applyTheme(theme, newMode);

      fetch('/accounts/toggle-theme/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCsrfToken(),
        },
        body: `theme=${encodeURIComponent(theme)}&mode=${encodeURIComponent(newMode)}`
      }).catch(err => console.debug('Theme sync:', err));
    }
  };

  function getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }

  // Initialize immediately
  initTheme();
})();
