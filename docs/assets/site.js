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
  for (const layer of layers) {
    const active = layer === selected;
    layer.classList.toggle('is-open', active);
    layer.classList.toggle('is-related', related.includes(layer.dataset.domain));
    layer.querySelector('.layer-select').setAttribute('aria-expanded', String(active));
    document.getElementById(`insight-${layer.dataset.domain}`).hidden = !active;
  }
  document.querySelector('.inspector-welcome').hidden = Boolean(selected);
  if (currentSteps.length && !stepper.hidden) {
    const index=currentSteps.findIndex(([target])=>String(target)===id);
    if(index>=0){currentStep=index;renderJourney();}
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
let currentSteps=[],currentStep=0;
function renderJourney(){
  stepper.replaceChildren();
  const progress=document.createElement('div');progress.className='journey-progress';
  progress.setAttribute('role','progressbar');progress.setAttribute('aria-valuemin','1');progress.setAttribute('aria-valuemax',String(currentSteps.length));progress.setAttribute('aria-valuenow',String(currentStep+1));progress.setAttribute('aria-label',stepper.dataset.label);
  const dial=document.createElement('span');dial.className='journey-dial';dial.textContent=String(currentStep+1).padStart(2,'0');dial.style.setProperty('--progress',`${(currentStep+1)/currentSteps.length*100}%`);progress.append(dial);
  const copy=document.createElement('div');copy.className='journey-current';
  const kicker=document.createElement('small');kicker.textContent=`${stepper.dataset.label} / ${currentStep+1} — ${currentSteps.length}`;
  const title=document.createElement('strong');title.textContent=currentSteps[currentStep][1];copy.append(kicker,title);
  const controls=document.createElement('div');controls.className='journey-controls';
  for(const offset of [-1,1]){
    const button=document.createElement('button');button.type='button';button.textContent=offset<0?`← ${stepper.dataset.prev}`:`${stepper.dataset.next} →`;button.disabled=currentStep+offset<0||currentStep+offset>=currentSteps.length;
    button.addEventListener('click',()=>{currentStep+=offset;inspectDomain(String(currentSteps[currentStep][0]));const nextFocus=stepper.querySelector(offset<0?'.journey-controls button:first-child':'.journey-controls button:last-child');(nextFocus.disabled?stepper.querySelector('.journey-controls button:not(:disabled)'):nextFocus).focus({preventScroll:true});});controls.append(button);
  }
  stepper.append(progress,copy,controls);
}
for (const journey of journeys) {
  journey.addEventListener('click',()=>{
    document.querySelector('.overview-choice').setAttribute('aria-pressed','false');
    stepper.hidden=false;document.getElementById('journey-description').hidden=false;
    journeys.forEach(item=>item.setAttribute('aria-pressed',String(item===journey)));
    const domains=journey.dataset.domains.split(',');layers.forEach(layer=>layer.classList.toggle('in-path',domains.includes(layer.dataset.domain)));
    document.getElementById('journey-description').textContent=journey.dataset.description;
    currentSteps=JSON.parse(journey.dataset.steps);currentStep=0;
    inspectDomain(String(currentSteps[0][0]));
  });
}
function resetArchitecture() {
  currentSteps=[];
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
  const positions=nodes.map(node=>['--nx','--ny'].map(key=>parseFloat(node.style.getPropertyValue(key))));
  const layouts=[positions,positions,positions];
  let mode = 0, step = 0, playing = !motion.matches, visible = true, hover = null, timer;
  let paths = [];
  function draw() {
    const coords = layouts[mode];
    nodes.forEach((node,i) => {node.style.setProperty('--nx',`${coords[i][0]}%`);node.style.setProperty('--ny',`${coords[i][1]}%`);});
    const order = data.modes[mode][3];
    nodes.forEach((node,i)=>{node.style.order=mode===0?i:order.indexOf(i);node.querySelector('.eco-number').textContent='0'+(mode===0?i+1:order.indexOf(i)+1);});
    const edges = order.slice(0,-1).map((id,i)=>[id,order[i+1]]);
    if (mode === 0) edges.push([order[5],order[0]],[0,4],[1,5]);
    const group = ecoPanel.querySelector('.eco-links');
    group.replaceChildren();
    paths = edges.map(([from,to])=>{
      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      const x1=coords[from][0]*6,y1=coords[from][1]*4.4-22,x2=coords[to][0]*6,y2=coords[to][1]*4.4-22,m=(x1+x2)/2;
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
    node.addEventListener('focus',()=>{hover=i;schedule();});
    node.addEventListener('blur',()=>{hover=null;schedule();});
  });
  toggle.hidden=false;
  toggle.addEventListener('click',()=>{playing=!playing;schedule();});
  document.addEventListener('visibilitychange',schedule);
  motion.addEventListener('change',()=>{if(motion.matches)playing=false;schedule();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule();},{threshold:.15}).observe(ecoPanel);
  draw();schedule();
}

// Reflect the reader's location without moving focus or changing navigation history.
const sectionLinks = [...document.querySelectorAll('.header-nav a')];
const navSections = sectionLinks.map(link => document.querySelector(link.getAttribute('href')));
let navFrame = false;
function updateSectionNavigation() {
  const threshold = document.querySelector('.site-header').getBoundingClientRect().bottom + 50;
  let active = -1;
  navSections.forEach((section, index) => { if (section.getBoundingClientRect().top <= threshold) active = index; });
  sectionLinks.forEach((link, index) => {
    if (index === active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  navFrame = false;
}
addEventListener('scroll', () => {
  if (!navFrame) { navFrame = true; requestAnimationFrame(updateSectionNavigation); }
}, {passive: true});
addEventListener('resize', updateSectionNavigation);
updateSectionNavigation();

// Mobile navigation keeps ordinary links usable when JavaScript is unavailable.
const siteHeader = document.querySelector('.site-header');
const menuToggle = document.querySelector('.menu-toggle');
const mobileNavigation = matchMedia('(max-width:960px)');
siteHeader.classList.add('nav-ready');
menuToggle.hidden = false;
function setMenuOpen(open, returnFocus = false) {
  siteHeader.classList.toggle('menu-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.querySelector('span').textContent = open ? menuToggle.dataset.closeLabel : menuToggle.dataset.openLabel;
  if (returnFocus) menuToggle.focus();
  updateSectionNavigation();
}
menuToggle.addEventListener('click', () => setMenuOpen(menuToggle.getAttribute('aria-expanded') !== 'true'));
siteHeader.addEventListener('keydown', event => {
  if (event.key === 'Escape' && siteHeader.classList.contains('menu-open')) {setMenuOpen(false, true);}
});
sectionLinks.forEach(link => link.addEventListener('click', () => {
  if (mobileNavigation.matches) setMenuOpen(false, true);
}));
document.addEventListener('click', event => {
  if (!siteHeader.contains(event.target) && siteHeader.classList.contains('menu-open')) setMenuOpen(false);
});
mobileNavigation.addEventListener('change', () => setMenuOpen(false));

siteHeader.addEventListener('focusout', event => {
  if (siteHeader.classList.contains('menu-open') && !siteHeader.contains(event.relatedTarget)) setMenuOpen(false);
});
