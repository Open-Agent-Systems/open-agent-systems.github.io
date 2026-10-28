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
