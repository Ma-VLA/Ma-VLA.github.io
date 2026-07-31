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
    ['/contents.html', 'Contents', '전체 목차'],
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

  /* ═══ OWNER: TRAINING-SERVER (RTX A5000) · 2026-07-31 · 규약: /OWNERSHIP.md ═══
     페이지 내 목차와 그림 라이트박스. 둘 다 기존 마크업에서 자동으로 만든다.
     목차는 <main> 바로 아래 <section id="..."> 를 훑어서 세우므로,
     섹션에 id만 붙이면 목차에 저절로 들어간다. 페이지 HTML은 수정할 필요 없다.
     ═══════════════════════════════════════════════════════════════════════ */

  const main = document.querySelector('main');

  /* ── 페이지 내 목차 ── */
  const sections = main ? [...main.querySelectorAll(':scope > section[id]')].filter((s) => s.id !== 'top') : [];
  if (sections.length >= 3) {
    // 라벨은 section-label → eyebrow → h2 → h3 순으로 찾는다. 그 요소가 이미
    // data-en/data-ko 를 들고 있으면 그대로 복사해서 언어 토글이 목차에도 걸리게 한다.
    const entries = sections.map((section) => {
      const source = section.querySelector('.section-label, .eyebrow, h2, h3');
      const en = source?.dataset.en || source?.textContent.trim() || section.id;
      const ko = source?.dataset.ko || en;
      return { id: section.id, en, ko };
    });

    const toc = document.createElement('nav');
    toc.className = 'page-toc';
    toc.setAttribute('aria-label', 'On this page');
    toc.innerHTML = `
      <button class="page-toc__tab" type="button" aria-expanded="false" aria-controls="page-toc-panel">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h8"/></svg>
        <span data-en="Contents" data-ko="목차">Contents</span>
      </button>
      <div class="page-toc__panel" id="page-toc-panel">${entries.map(({ id, en, ko }, i) =>
        `<a href="#${id}" data-toc="${id}"><span class="page-toc__num">${String(i + 1).padStart(2, '0')}</span><span data-en="${en.replace(/"/g, '&quot;')}" data-ko="${ko.replace(/"/g, '&quot;')}">${en}</span></a>`
      ).join('')}</div>`;
    document.body.appendChild(toc);

    const tocTab = toc.querySelector('.page-toc__tab');
    tocTab.addEventListener('click', () => {
      const open = toc.classList.toggle('is-open');
      tocTab.setAttribute('aria-expanded', String(open));
    });
    toc.querySelectorAll('[data-toc]').forEach((link) => link.addEventListener('click', () => {
      toc.classList.remove('is-open');
      tocTab.setAttribute('aria-expanded', 'false');
    }));

    // scroll-spy: 뷰포트 상단에서 35% 지점을 지난 마지막 섹션이 현재 위치다.
    const links = [...toc.querySelectorAll('[data-toc]')];
    const syncActive = () => {
      const mark = window.scrollY + window.innerHeight * 0.35;
      let current = sections[0].id;
      sections.forEach((s) => { if (s.getBoundingClientRect().top + window.scrollY <= mark) current = s.id; });
      links.forEach((l) => l.classList.toggle('is-active', l.dataset.toc === current));
    };
    window.addEventListener('scroll', syncActive, { passive: true });
    window.addEventListener('resize', syncActive, { passive: true });
    syncActive();
  }

  /* ── 그림 라이트박스 ── */
  // 그림은 지금까지 새 탭으로 원본을 열었다. 근거를 보려고 페이지를 떠나게 된다.
  const figureLinks = [...document.querySelectorAll('.report-figure a[href$=".png"], .figure-card a[href$=".png"]')];
  if (figureLinks.length) {
    const items = figureLinks.map((a) => ({
      src: a.getAttribute('href'),
      alt: a.querySelector('img')?.alt || '',
      caption: a.closest('figure')?.querySelector('figcaption')?.textContent.trim() || '',
    }));

    const box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML = `
      <img alt="">
      <div class="lightbox__bar">
        <button type="button" data-lb="prev" aria-label="Previous figure">◀</button>
        <span class="lightbox__count"></span>
        <span class="lightbox__caption"></span>
        <a class="lightbox__open" target="_blank" rel="noopener noreferrer" data-en="Original ↗" data-ko="원본 ↗">Original ↗</a>
        <button type="button" data-lb="close" data-en="Close (Esc)" data-ko="닫기 (Esc)">Close (Esc)</button>
      </div>`;
    document.body.appendChild(box);

    const img = box.querySelector('img');
    const count = box.querySelector('.lightbox__count');
    const caption = box.querySelector('.lightbox__caption');
    const original = box.querySelector('.lightbox__open');
    let index = 0;

    const render = () => {
      const item = items[index];
      img.src = item.src;
      img.alt = item.alt;
      caption.textContent = item.caption;
      original.href = item.src;
      count.textContent = `${index + 1} / ${items.length}`;
      // 한 장뿐이면 이동 버튼은 의미가 없다.
      box.querySelectorAll('[data-lb="prev"], [data-lb="next"]').forEach((b) => {
        b.hidden = items.length < 2;
      });
      count.hidden = items.length < 2;
    };
    const open = (i) => { index = i; render(); box.classList.add('is-open'); document.body.style.overflow = 'hidden'; };
    const close = () => { box.classList.remove('is-open'); document.body.style.overflow = ''; };
    const step = (d) => { index = (index + d + items.length) % items.length; render(); };

    // 다음 버튼은 prev 뒤에 넣어야 순서가 맞는다.
    const next = document.createElement('button');
    next.type = 'button'; next.dataset.lb = 'next'; next.textContent = '▶';
    next.setAttribute('aria-label', 'Next figure');
    count.after(next);

    figureLinks.forEach((a, i) => a.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return; // 새 탭으로 열려는 의도는 존중
      event.preventDefault();
      open(i);
    }));
    box.addEventListener('click', (event) => {
      const action = event.target.closest('[data-lb]')?.dataset.lb;
      if (action === 'prev') step(-1);
      else if (action === 'next') step(1);
      else if (action === 'close' || event.target === box) close();
    });
    document.addEventListener('keydown', (event) => {
      if (!box.classList.contains('is-open')) return;
      if (event.key === 'Escape') close();
      else if (event.key === 'ArrowLeft') step(-1);
      else if (event.key === 'ArrowRight') step(1);
    });
  }

  applyLanguage();
  applyTheme();
})();
