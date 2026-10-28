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

// Illustration only. No model calls or runtime telemetry.
const ecoPanel = document.querySelector('.eco-panel');
if (ecoPanel) {
  const data = JSON.parse(ecoPanel.dataset.eco);
  const nodes = [...ecoPanel.querySelectorAll('.eco-node')];
  const modes = [...ecoPanel.querySelectorAll('.eco-mode')];
  const toggle = ecoPanel.querySelector('.eco-toggle');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const layouts = [
    [[28,18],[72,18],[87,50],[72,82],[28,82],[13,50]],
    [[15,22],[71,22],[85,78],[43,22],[57,78],[15,78]],
    [[15,78],[43,78],[71,78],[85,22],[15,22],[50,22]]
  ];
  let mode = 0, step = 0, playing = !motion.matches, visible = true, hover = null, timer;
  let paths = [];
  function draw() {
    const coords = layouts[mode];
    nodes.forEach((node,i) => {node.style.setProperty('--nx',`${coords[i][0]}%`);node.style.setProperty('--ny',`${coords[i][1]}%`);});
    const order = data.modes[mode][3];
    nodes.forEach((node,i)=>{node.style.order=order.indexOf(i);node.querySelector('.eco-number').textContent='0'+(mode===0?i+1:order.indexOf(i)+1);});
    const edges = order.slice(0,-1).map((id,i)=>[id,order[i+1]]);
    if (mode === 0) edges.push([order[5],order[0]],[0,4],[1,5]);
    const group = ecoPanel.querySelector('.eco-links');
    group.replaceChildren();
    paths = edges.map(([from,to])=>{
      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d',`M${coords[from][0]*6} ${coords[from][1]*4} Q300 ${mode===0 ? 200 : (coords[from][1]+coords[to][1])*2-50} ${coords[to][0]*6} ${coords[to][1]*4}`);
      path.dataset.from=from; path.dataset.to=to;
      group.append(path);
      return path;
    });
    ecoPanel.dataset.view=mode;
    ecoPanel.querySelector('.eco-core span').textContent=data.modes[mode][1];
    ecoPanel.querySelector('#eco-summary').textContent=data.modes[mode][2];
    modes.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===mode)));
  }
  function render() {
    const id=data.modes[mode][3][step];
    const highlighted=hover === null ? id : hover;
    nodes.forEach((node,i)=>{node.setAttribute('aria-pressed',String(i===id));node.classList.toggle('eco-highlight',i===highlighted);});
    paths.forEach(path=>path.classList.toggle('active',Number(path.dataset.from)===highlighted || Number(path.dataset.to)===highlighted));
    ecoPanel.querySelector('.eco-progress').textContent=`0${step+1} / 06`;
    const detail=ecoPanel.querySelector('#eco-detail');
    detail.setAttribute('aria-live',playing?'off':'polite');
    detail.textContent=data.nodes[id][1];
    toggle.textContent=playing?data.pause:data.play;
    ecoPanel.classList.toggle('eco-playing',playing&&visible&&!document.hidden&&hover===null);
  }
  function schedule() {
    clearInterval(timer);render();
    if(playing&&visible&&!document.hidden&&hover===null) timer=setInterval(()=>{step=(step+1)%6;render();},4500);
  }
  modes.forEach((button,i)=>button.addEventListener('click',()=>{mode=i;step=0;hover=null;draw();schedule();}));
  nodes.forEach((node,i)=>{
    node.addEventListener('click',()=>{step=data.modes[mode][3].indexOf(i);playing=false;schedule();});
    node.addEventListener('pointerenter',()=>{hover=i;schedule();});
    node.addEventListener('pointerleave',()=>{hover=null;schedule();});
  });
  toggle.hidden=false;
  toggle.addEventListener('click',()=>{playing=!playing;schedule();});
  document.addEventListener('visibilitychange',schedule);
  motion.addEventListener('change',()=>{if(motion.matches)playing=false;schedule();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule();},{threshold:.15}).observe(ecoPanel);
  draw();schedule();
}
