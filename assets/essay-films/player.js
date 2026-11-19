(() => {
  'use strict';
  const root = document.documentElement;
  const players = [];
  const dark = () => root.dataset.theme === 'dark';
  const theme = () => dark() ? 'dark' : 'light';

  function init(figure) {
    const video = figure.querySelector('video');
    const covers = {
      light: figure.querySelector('.film-light'),
      dark: figure.querySelector('.film-dark')
    };
    const error = figure.querySelector('.film-error');
    const toggle = document.querySelector('[aria-controls="' + figure.id + '"].film-clock-link');
    let pending = null;
    let controller = null;

    function updateToggle(open) {
      if (!toggle) return;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('.film-clock-text').textContent = open ? 'Hide the clock example' : 'Watch the clock example';
    }

    function stop() {
      if (controller) controller.abort();
      pending = null;
      video.pause();
      video.removeAttribute('src');
      video.load();
      video.hidden = true;
      delete figure.dataset.started;
    }

    function loadCut(state) {
      if (controller) controller.abort();
      controller = new AbortController();
      const options = {once: true, signal: controller.signal};
      pending = state;
      error.hidden = true;
      video.poster = covers[theme()].querySelector('img').src;
      video.addEventListener('loadedmetadata', () => {
        video.currentTime = Math.min(state.time, video.duration);
        video.playbackRate = state.rate;
        if (video.textTracks.length && state.captions) video.textTracks[0].mode = state.captions;
        pending = null;
        if (state.playing) video.play().catch(() => {});
      }, options);
      video.addEventListener('error', () => {
        stop();
        error.hidden = false;
      }, options);
      video.src = covers[theme()].href;
      video.load();
    }

    function start(event) {
      if (event && (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button > 0)) return;
      if (event) event.preventDefault();
      if (toggle) {figure.hidden = false; updateToggle(true);}
      video.hidden = false;
      figure.dataset.started = '';
      loadCut({time: 0, playing: true, rate: 1});
      // Keep the user's play gesture for browsers that require it.
      video.play().catch(() => {});
      video.focus({preventScroll: true});
      if (toggle && video.getBoundingClientRect().bottom > innerHeight) {
        const head = document.querySelector('.site-header');
        const offset = head ? head.getBoundingClientRect().height : 0;
        window.scrollTo({top: scrollY + figure.getBoundingClientRect().top - offset - 12, behavior: 'instant'});
      }
    }

    Object.values(covers).forEach(cover => cover.addEventListener('click', start));
    if (toggle) {
      toggle.addEventListener('click', event => {
        if (figure.hidden) {start(event); return;}
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        stop();
        error.hidden = true;
        figure.hidden = true;
        updateToggle(false);
      });
    }

    return function syncTheme() {
      const cover = covers[theme()];
      if (toggle) toggle.href = cover.href;
      if (!figure.hasAttribute('data-started') || video.src === cover.href) return;
      const state = pending || {
        time: video.currentTime,
        playing: !video.paused && !video.ended,
        rate: video.playbackRate,
        captions: video.textTracks.length && video.textTracks[0].mode
      };
      loadCut(state);
    };
  }

  document.querySelectorAll('.essay-film').forEach(figure => players.push(init(figure)));
  const sync = () => players.forEach(update => update());
  new MutationObserver(sync).observe(root, {attributes:true, attributeFilter:['data-theme']});
  sync();
  // The site's theme button persists the reader's explicit choice.
  const preference = matchMedia('(prefers-color-scheme: dark)');
  preference.addEventListener('change', () => {
    try {if (localStorage.getItem('site-theme')) return;} catch (_) {}
    if (preference.matches) root.dataset.theme = 'dark';
    else root.removeAttribute('data-theme');
    const button = document.querySelector('[data-theme-toggle]');
    if (button) {
      button.setAttribute('aria-pressed', String(dark()));
      button.setAttribute('aria-label', dark() ? 'Switch to light theme' : 'Switch to dark theme');
    }
    const meta = document.getElementById('meta-theme-color');
    if (meta) meta.content = dark() ? '#0a0a0a' : '#fafafa';
  });
})();
