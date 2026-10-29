for (const choice of document.querySelectorAll('.direction-choice')) {
  choice.addEventListener('click', () => {
    for (const item of document.querySelectorAll('.direction-choice')) item.setAttribute('aria-pressed', String(item === choice));
    document.getElementById('direction-title').textContent = choice.querySelector('strong').textContent;
    document.getElementById('direction-description').textContent = choice.dataset.description;
  });
}

const layers = [...document.querySelectorAll('.architecture-layer')];
const journeys = [...document.querySelectorAll('.journey-choice')];
const stepper = document.querySelector('.journey-stepper');
const architectureMap = document.querySelector('.architecture-map');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let selectedDomain = null;
function inspectDomain(id, moveFocus = false) {
  selectedDomain = id;
  document.querySelector('.capability-inspector').scrollTop = 0;
  const selected = layers.find(layer => layer.dataset.domain === id);
  const related = selected?.dataset.related.split(',') || [];
  architectureMap.classList.toggle('is-exploring', Boolean(selected));
  document.querySelector('.inspected-edges')?.remove();
  if (selected) {
    const group=document.createElementNS('http://www.w3.org/2000/svg','g');group.classList.add('inspected-edges');
    const point=layer=>[parseFloat(layer.style.getPropertyValue('--mx'))*10,parseFloat(layer.style.getPropertyValue('--my'))*6.2-45];
    const [x1,y1]=point(selected);
    related.forEach(target=>{
      const [x2,y2]=point(layers.find(layer=>layer.dataset.domain===target)),middle=(x1+x2)/2;
      const path=document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d',`M${x1} ${y1}C${middle} ${y1},${middle} ${y2},${x2} ${y2}`);path.classList.add('scene-edge','is-connected');group.append(path);
    });
    const svg=document.querySelector('.iso-map-svg');svg.insertBefore(group,svg.querySelector('.scene-object'));
  }
  document.querySelectorAll('.iso-map-svg .scene-object').forEach(object => {object.classList.toggle('is-selected',object.dataset.object === id);object.classList.toggle('is-connected',related.includes(object.dataset.object));});
  for (const layer of layers) {
    const active = layer === selected;
    layer.classList.toggle('is-open', active);
    layer.classList.toggle('is-related', related.includes(layer.dataset.domain));
    layer.querySelector('.layer-select').setAttribute('aria-expanded', String(active));
    document.getElementById(`insight-${layer.dataset.domain}`).hidden = !active;
  }
  document.querySelector('.inspector-welcome').hidden = Boolean(selected);
  for (const button of stepper.querySelectorAll('button')) button.setAttribute('aria-pressed', String(button.dataset.target === id));
  document.querySelectorAll('.insight-navigation').forEach(el=>el.remove());
  if (selected) {
    const steps=[...stepper.querySelectorAll('button')];
    const index=steps.findIndex(button=>button.dataset.target===id);
    if(index>=0 && !stepper.hidden){
      const nav=document.createElement('div');nav.className='insight-navigation';
      for(const offset of [-1,1]){
        const target=steps[index+offset];if(!target)continue;
        const button=document.createElement('button');button.type='button';
        button.textContent=(offset<0?'← ':'')+target.querySelector('strong').textContent+(offset>0?' →':'');
        button.addEventListener('click',()=>inspectDomain(target.dataset.target,true));nav.append(button);
      }
      const panel=document.getElementById(`insight-${id}`);panel.insertBefore(nav,panel.querySelector('.insight-close'));
    }
  }
  if (moveFocus && selected) {
    const button = selected.querySelector('.layer-select');
    button.focus({preventScroll:true});
    document.querySelector('.capability-inspector').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'nearest'});
  }
}
for (const layer of layers) {
  layer.querySelector('.layer-select').addEventListener('click', () => inspectDomain(selectedDomain === layer.dataset.domain ? null : layer.dataset.domain, matchMedia('(max-width:960px)').matches));
  document.querySelector(`[data-close="${layer.dataset.domain}"]`).addEventListener('click', () => {inspectDomain(null);layer.querySelector('.layer-select').focus({preventScroll:true});});
  layer.addEventListener('keydown', event => {if(event.key==='Escape' && selectedDomain===layer.dataset.domain){event.preventDefault();inspectDomain(null);layer.querySelector('.layer-select').focus({preventScroll:true});}});
}
document.querySelector('.capability-inspector').addEventListener('keydown',event=>{if(event.key==='Escape' && selectedDomain!==null){const id=selectedDomain;inspectDomain(null);document.querySelector(`[data-layer="${id}"]`).focus({preventScroll:true});}});
for (const button of document.querySelectorAll('.related-capability')) button.addEventListener('click', () => inspectDomain(button.dataset.target,true));
for (const journey of journeys) {
  journey.addEventListener('click', () => {
    document.querySelector('.overview-choice').setAttribute('aria-pressed','false');
    stepper.hidden=false;
    document.getElementById('journey-description').hidden=false;
    inspectDomain(null);
    for (const item of journeys) item.setAttribute('aria-pressed', String(item === journey));
    const domains = journey.dataset.domains.split(',');
    for (const layer of layers) layer.classList.toggle('in-path', domains.includes(layer.dataset.domain));
    document.querySelectorAll('.iso-map-svg .scene-edge').forEach(edge=>edge.classList.toggle('in-path',domains.includes(edge.dataset.from)&&domains.includes(edge.dataset.to)));
    document.getElementById('journey-description').textContent = journey.dataset.description;
    stepper.replaceChildren();
    JSON.parse(journey.dataset.steps).forEach(([id,label],index)=>{
      const button = document.createElement('button');
      button.type='button';button.dataset.target=String(id);button.setAttribute('aria-pressed','false');button.setAttribute('aria-controls',`insight-${id}`);
      const number=document.createElement('span');number.textContent=String(index+1).padStart(2,'0');
      const title=document.createElement('strong');title.textContent=label;
      button.append(number,title);button.addEventListener('click',()=>inspectDomain(String(id),true));stepper.append(button);
    });
  });
}
function resetArchitecture() {
  inspectDomain(null);
  journeys.forEach(button=>button.setAttribute('aria-pressed','false'));
  layers.forEach(layer=>layer.classList.remove('in-path'));
  document.querySelectorAll('.iso-map-svg .scene-edge').forEach(edge=>edge.classList.remove('in-path'));
  stepper.hidden=true;
  document.getElementById('journey-description').hidden=true;
  document.querySelector('.overview-choice').setAttribute('aria-pressed','true');
}
document.querySelector('.explorer-reset')?.addEventListener('click',resetArchitecture);
document.querySelector('.overview-choice')?.addEventListener('click',resetArchitecture);
journeys[0]?.click();
resetArchitecture();

// Illustration only. No model calls or runtime telemetry.
const ecoPanel = document.querySelector('.eco-panel');
if (ecoPanel) {
  const data = JSON.parse(ecoPanel.dataset.eco);
  const nodes = [...ecoPanel.querySelectorAll('.eco-node')];
  const modes = [...ecoPanel.querySelectorAll('.eco-mode')];
  const toggle = ecoPanel.querySelector('.eco-toggle');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const positions=[[15,32],[48,32],[81,32],[22,76],[51,76],[81,76]];
  const layouts=[positions,positions,positions];
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
      const x1=coords[from][0]*6,y1=coords[from][1]*4.4-45,x2=coords[to][0]*6,y2=coords[to][1]*4.4-45,m=(x1+x2)/2;
      path.setAttribute('d',`M${x1} ${y1} C${m} ${y1},${m} ${y2},${x2} ${y2}`);
      path.dataset.from=from; path.dataset.to=to;
      group.append(path);
      return path;
    });
    ecoPanel.dataset.view=mode;
    ecoPanel.querySelector('.scene-title').textContent=data.sceneTitles[mode];
    ecoPanel.querySelector('.eco-core span').textContent=data.modes[mode][1];
    ecoPanel.querySelector('#eco-summary').textContent=data.modes[mode][2];
    modes.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===mode)));
  }
  function render() {
    const id=data.modes[mode][3][step];
    const highlighted=hover === null ? id : hover;
    nodes.forEach((node,i)=>{node.setAttribute('aria-pressed',String(i===id));node.classList.toggle('eco-highlight',i===highlighted);});
    paths.forEach(path=>path.classList.toggle('active',Number(path.dataset.from)===highlighted || Number(path.dataset.to)===highlighted));
    ecoPanel.querySelectorAll('.scene-object').forEach(object=>object.classList.toggle('is-selected',Number(object.dataset.object)===highlighted));
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
