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

const nodes = [...document.querySelectorAll('.signal-node')];
const ecosystemDescription = document.getElementById('ecosystem-description');
for (const node of nodes) {
  node.addEventListener('click', () => {
    for (const item of nodes) item.setAttribute('aria-pressed', String(item === node));
    for (const edge of document.querySelectorAll('.signal-edge')) edge.classList.toggle('active', edge.dataset.edge === node.dataset.node);
    ecosystemDescription.textContent = node.dataset.description;
  });
}
for (const choice of document.querySelectorAll('.direction-choice')) {
  choice.addEventListener('click', () => {
    for (const item of document.querySelectorAll('.direction-choice')) item.setAttribute('aria-pressed', String(item === choice));
    document.getElementById('direction-title').textContent = choice.querySelector('strong').textContent;
    document.getElementById('direction-description').textContent = choice.dataset.description;
  });
}
