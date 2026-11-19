(() => {
  const root = document.documentElement;
  const videos = [...document.querySelectorAll('video[data-zal-model]')];

  function bind(video) {
    const darkCut = video.querySelector('source[media]');
    const lightCut = video.querySelector('source:not([media])');
    let pending;
    let listener;

    return function applyTheme() {
      const dark = root.dataset.theme === 'dark';
      const cut = dark ? darkCut : lightCut;
      if (cut.src === video.src) return;

      const state = pending || (video.readyState >= 1 || !video.paused ? {
        time: video.currentTime,
        playing: !video.paused && !video.ended,
        rate: video.playbackRate,
        captions: video.textTracks[0]?.mode
      } : null);

      listener?.abort();
      listener = new AbortController();
      pending = state;
      video.poster = cut.dataset.poster;

      if (state) {
        video.preload = 'auto';
        video.addEventListener('loadedmetadata', () => {
          video.currentTime = Math.min(state.time, video.duration);
          video.playbackRate = state.rate;
          if (state.captions && video.textTracks[0]) video.textTracks[0].mode = state.captions;
          pending = null;
          if (state.playing) video.play().catch(() => {});
        }, {once: true, signal: listener.signal});
      }
      video.src = cut.src;
      video.load();
    };
  }

  const updates = videos.map(bind);
  const sync = () => updates.forEach(apply => apply());
  new MutationObserver(sync).observe(root, {attributes: true, attributeFilter: ['data-theme']});
  sync();
})();
