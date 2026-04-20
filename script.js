(() => {
  const root = document.documentElement;
  const btn = document.querySelector('[data-theme-toggle]');
  let theme = 'light';

  const applyTheme = (value) => {
    root.setAttribute('data-theme', value);
    if (!btn) return;
    btn.setAttribute('aria-label', value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    btn.querySelector('.theme-icon').textContent = value === 'dark' ? '☀' : '◐';
  };

  applyTheme(theme);

  btn?.addEventListener('click', () => {
    theme = theme === 'dark' ? 'light' : 'dark';
    applyTheme(theme);
  });
})();
