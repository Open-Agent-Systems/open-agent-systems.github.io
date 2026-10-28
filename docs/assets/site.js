const layers = [...document.querySelectorAll('.architecture-layer')];
const description = document.getElementById('layer-description');
if (description && layers.length) {
  document.documentElement.classList.add('has-layer-controls');
  for (const layer of layers) {
    const button = layer.querySelector('.layer-select');
    button.addEventListener('click', () => {
      for (const candidate of layers) {
        candidate.querySelector('.layer-select').setAttribute('aria-pressed', String(candidate === layer));
      }
      description.textContent = layer.querySelector('.layer-copy').textContent;
    });
  }
}

for (const choice of document.querySelectorAll('.direction-choice')) {
  choice.addEventListener('click', () => {
    for (const item of document.querySelectorAll('.direction-choice')) item.setAttribute('aria-pressed', String(item === choice));
    document.getElementById('direction-title').textContent = choice.querySelector('strong').textContent;
    document.getElementById('direction-description').textContent = choice.dataset.description;
  });
}

const journeys = [...document.querySelectorAll('.journey-choice')];
for (const journey of journeys) {
  journey.addEventListener('click', () => {
    for (const item of journeys) item.setAttribute('aria-pressed', String(item === journey));
    const domains = journey.dataset.domains.split(',');
    for (const domain of document.querySelectorAll('[data-domain]')) {
      domain.classList.toggle('in-path', domains.includes(domain.dataset.domain));
    }
    document.getElementById('journey-description').textContent = journey.dataset.description;
  });
}
journeys[0]?.click();

// Conceptual playback; manual exploration pauses it. No live task execution.
const loopSteps = [...document.querySelectorAll('.loop-step')];
const loopToggle = document.querySelector('.loop-toggle');
if (loopSteps.length && loopToggle) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const panel = document.querySelector('.task-ecosystem');
  const copy = document.getElementById('loop-description');
  let current = 0;
  let playing = !reduced.matches;
  let visible = true;
  let timer;
  function render() {
    loopSteps.forEach((step, i) => step.setAttribute('aria-pressed', String(i === current)));
    const resources = loopSteps[current].dataset.resources.split(',');
    document.querySelectorAll('[data-resource]').forEach(el => el.classList.toggle('engaged', resources.includes(el.dataset.resource)));
    document.querySelectorAll('[data-wire]').forEach(el => el.classList.toggle('engaged', resources.includes(el.dataset.wire)));
    panel.querySelector('.loop-counter').textContent = `0${current + 1} / 04`;
    copy.textContent = loopSteps[current].dataset.copy;
    copy.setAttribute('aria-live', playing ? 'off' : 'polite');
    loopToggle.textContent = playing ? loopToggle.dataset.pause : loopToggle.dataset.play;
    panel.classList.toggle('is-playing', playing && visible && !document.hidden);
  }
  function schedule() {
    clearInterval(timer);
    render();
    if (playing && visible && !document.hidden) timer = setInterval(() => { current = (current + 1) % loopSteps.length; render(); }, 5000);
  }
  loopSteps.forEach((step, i) => step.addEventListener('click', () => { current = i; playing = false; schedule(); }));
  loopToggle.hidden = false;
  loopToggle.addEventListener('click', () => { playing = !playing; schedule(); });
  document.addEventListener('visibilitychange', schedule);
  reduced.addEventListener('change', () => { if (reduced.matches) playing = false; schedule(); });
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; schedule(); }, {threshold: 0.15}).observe(panel);
  schedule();
}
