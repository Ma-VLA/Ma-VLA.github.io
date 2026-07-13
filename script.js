(() => {
  const root = document.documentElement;
  const languageButton = document.querySelector('[data-language-toggle]');
  const themeButton = document.querySelector('[data-theme-toggle]');
  let language = localStorage.getItem('flowbridge-language') || 'en';
  let theme = 'light';

  const applyLanguage = () => {
    root.lang = language === 'ko' ? 'ko' : 'en';
    document.querySelectorAll('[data-en][data-ko]').forEach((element) => {
      element.textContent = element.dataset[language];
    });
    if (languageButton) {
      languageButton.textContent = language === 'en' ? '한국어' : 'EN';
      languageButton.setAttribute('aria-label', language === 'en' ? '한국어로 전환' : 'Switch to English');
    }
  };

  const applyTheme = () => {
    root.dataset.theme = theme;
    if (!themeButton) return;
    themeButton.innerHTML = theme === 'dark'
      ? '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>'
      : '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>';
    themeButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  };

  languageButton?.addEventListener('click', () => {
    language = language === 'en' ? 'ko' : 'en';
    localStorage.setItem('flowbridge-language', language);
    applyLanguage();
  });

  themeButton?.addEventListener('click', () => {
    theme = theme === 'light' ? 'dark' : 'light';
    applyTheme();
  });

  applyLanguage();
  applyTheme();
})();
