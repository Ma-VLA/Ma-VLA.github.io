(() => {
  const root = document.documentElement;
  const header = document.querySelector('.site-header');
  const navShell = document.querySelector('.nav-shell');
  const nav = document.querySelector('.primary-nav');
  const currentPath = window.location.pathname.replace(/\/index\.html$/, '/') || '/';
  const navItems = [
    ['/', 'Home', '홈'],
    ['/research.html', 'Research Program', '연구 프로그램'],
    ['/system/dobot-e6.html', 'Systems', '시스템'],
    ['/results.html', 'Experiments', '실험'],
    ['/publications.html', 'Publications', '논문'],
    ['/resources.html', 'Resources', '자료'],
  ];

  if (nav) {
    nav.innerHTML = navItems.map(([href, en, ko]) => {
      const isCurrent = href === '/'
        ? currentPath === '/'
        : currentPath === href || (href === '/system/dobot-e6.html' && currentPath.startsWith('/system/'));
      return `<a href="${href}"${isCurrent ? ' aria-current="page"' : ''} data-en="${en}" data-ko="${ko}">${en}</a>`;
    }).join('') + `
      <a href="https://kyle-riss.github.io/" target="_blank" rel="noopener noreferrer" data-en="Researcher ↗" data-ko="연구자 ↗">Researcher ↗</a>
      <span class="nav-actions">
        <button class="lang-btn" data-language-toggle type="button">한국어</button>
        <button class="icon-btn" data-theme-toggle type="button"></button>
      </span>`;
  }

  if (navShell && nav) {
    const menuButton = document.createElement('button');
    menuButton.className = 'menu-btn';
    menuButton.type = 'button';
    menuButton.setAttribute('aria-label', 'Open navigation');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.innerHTML = '<span></span><span></span><span></span>';
    navShell.insertBefore(menuButton, nav);
    menuButton.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    });
    nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    }));
  }

  const languageButton = document.querySelector('[data-language-toggle]');
  const themeButton = document.querySelector('[data-theme-toggle]');
  let language = localStorage.getItem('flowbridge-language') || 'en';
  let theme = localStorage.getItem('ma-vla-theme') || 'light';

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
    localStorage.setItem('ma-vla-theme', theme);
    applyTheme();
  });

  applyLanguage();
  applyTheme();
})();
