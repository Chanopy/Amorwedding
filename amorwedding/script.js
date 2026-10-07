(() => {
  'use strict';

  document.querySelectorAll('[data-kakao]').forEach(link => {
    link.href = window.AMOR_CONFIG?.kakaoChannelUrl || 'https://pf.kakao.com/_SKRMX';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', link.textContent.trim() + ' (새 창)');
  });

  // Reveal each section once, with a gentle stagger for side-by-side cards.
  // No scroll interception: mouse, touch, anchor links and keyboard stay native.
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionTargets = [...document.querySelectorAll(
    '.hero-content, .reveal, .quote-banner > p, .footer-top, .business-info, .footer-bottom'
  )];
  let motionObserver;
  function reveal(target) {
    target.classList.add('is-visible');
    motionObserver?.unobserve(target);
  }
  function startSectionMotion() {
    if (motionPreference.matches || !('IntersectionObserver' in window)) return;
    motionObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) reveal(entry.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -32px 0px' });
    document.querySelectorAll('.package-grid, .features, .consult').forEach(group => {
      [...group.children].forEach((child, index) => {
        child.style.setProperty('--amor-reveal-delay', `${Math.min(index, 3) * 120}ms`);
      });
    });
    motionTargets.forEach(target => {
      // Already-passed content is immediately available on restored scroll positions.
      if (target.getBoundingClientRect().bottom <= 0) return;
      target.classList.add('motion-ready');
      motionObserver.observe(target);
    });
    document.addEventListener('focusin', event => {
      const target = event.target.closest('.motion-ready');
      if (target) reveal(target);
    });
  }
  startSectionMotion();
  motionPreference.addEventListener('change', event => {
    if (event.matches) {
      motionObserver?.disconnect();
      motionTargets.forEach(target => target.classList.remove('motion-ready'));
    }
  });

  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-nav');
  function closeMenu() {
    menu.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '메뉴 열기');
  }
  menuButton.addEventListener('click', () => {
    menu.hidden = !menu.hidden;
    menuButton.setAttribute('aria-expanded', String(!menu.hidden));
    menuButton.setAttribute('aria-label', menu.hidden ? '메뉴 열기' : '메뉴 닫기');
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { closeMenu(); menuButton.focus(); } });
  window.matchMedia('(min-width:701px)').addEventListener('change', e => { if (e.matches) closeMenu(); });
  const hero = document.querySelector('.hero-photo');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  function parallax() {
    if (frame) return;
    frame = requestAnimationFrame(() => {
      hero.style.transform = reduceMotion.matches ? 'none' : `translateY(${Math.min(window.scrollY * .23, 240)}px) scale(1.08)`;
      frame = 0;
    });
  }
  window.addEventListener('scroll', parallax, { passive: true });
  reduceMotion.addEventListener('change', parallax);
  parallax();

  const header = document.querySelector('.header');
  let lastY = window.scrollY;
  let scrollFrame = 0;
  window.addEventListener('scroll', () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      const y = Math.max(0, window.scrollY);
      if (y <= 94 || !menu.hidden || header.contains(document.activeElement)) {
        header.classList.remove('is-hidden');
      } else if (Math.abs(y - lastY) > 5) {
        header.classList.toggle('is-hidden', y > lastY);
      }
      if (Math.abs(y - lastY) > 5 || y <= 94) lastY = y;
      scrollFrame = 0;
    });
  }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));

  const journey = document.querySelector('.journey');
  [...journey.children].forEach((step, index) => step.style.setProperty('--step-delay', `${index * 900}ms`));
  document.querySelectorAll('.feature-number svg :is(path, circle)').forEach(path => path.setAttribute('pathLength', '1'));
  const animated = [journey, ...document.querySelectorAll('.feature')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-playing');
        observer.unobserve(entry.target);
      }
    }), { threshold: .35 });
    animated.forEach(element => observer.observe(element));
  } else animated.forEach(element => element.classList.add('is-playing'));
})();
