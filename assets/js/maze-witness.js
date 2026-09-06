(function () {
  'use strict';
  const host = document.querySelector('[data-maze-demo]');
  if (!host || !window.MazeWitness) return;
  const core = window.MazeWitness;
  const svg = host.querySelector('svg');
  const status = host.querySelector('[data-maze-status]');
  const detail = host.querySelector('[data-maze-detail]');
  const pause = host.querySelector('[data-maze-pause]');
  const select = host.querySelector('select');
  const buttons = [...host.querySelectorAll('[data-maze-run]')];
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0, paused = false, active = false, progress = 0, last = null, step, length, complete, delay;
  const ns = 'http://www.w3.org/2000/svg';
  const element = (name,attrs,parent=svg) => {
    const el = document.createElementNS(ns,name);
    Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));
    parent.appendChild(el);
    return el;
  };
  const point = p => `${p[0]*32+16},${p[1]*32+16}`;
  const cells = new Map();
  core.rows.forEach((row,y)=>[...row].forEach((char,x)=>{
    const r = element('rect',{x:x*32+1,y:y*32+1,width:30,height:30,rx:1,class:char==='#'?'maze-wall':'maze-cell'});
    if(char!=='#') cells.set(`${x},${y}`,r);
  }));
  const proposal = element('polyline',{class:'maze-proposal',fill:'none'});
  const trace = element('polyline',{class:'maze-trace',fill:'none'});
  const dot = element('circle',{r:5,class:'maze-dot'});
  for (const [p,label] of [[core.start,'S'],[core.goal,'G']]) {
    const t = element('text',{x:p[0]*32+16,y:p[1]*32+21,'text-anchor':'middle',class:'maze-marker'});
    t.textContent=label;
  }

  function stop() {
    cancelAnimationFrame(frame);
    active=false; paused=false; last=null;
    pause.hidden=true; pause.textContent='Pause';
    buttons.forEach(b=>b.disabled=false);
    select.disabled=false;
  }
  function reset() {
    stop();
    host.dataset.result='ready';
    status.textContent='A proposal is waiting for a check.';
    detail.textContent='The dashed line is a candidate trajectory. S is Start; G is Goal.';
    cells.forEach(c=>c.classList.remove('maze-visited','maze-rejected'));
    proposal.setAttribute('points',core.routes[select.value].map(point).join(' '));
    trace.setAttribute('points','');
    dot.setAttribute('cx',core.start[0]*32+16);
    dot.setAttribute('cy',core.start[1]*32+16);
  }
  function tick(time) {
    if(!active || paused) return;
    if(last===null) last=time;
    if(time-last>=delay) {
      last=time;
      step(progress++);
      if(progress>=length) { const done=complete; stop(); done(); return; }
    }
    frame=requestAnimationFrame(tick);
  }
  function animate(count,interval,onStep,onComplete) {
    active=true; paused=false; progress=0; last=null;
    length=count; delay=interval; step=onStep; complete=onComplete;
    buttons.forEach(b=>b.disabled=true); select.disabled=true;
    if(reducedMotion.matches) {
      for(let i=0;i<count;i++) onStep(i);
      stop(); onComplete();
    } else {
      pause.hidden=false;
      frame=requestAnimationFrame(tick);
    }
  }
  function check() {
    reset();
    const path=core.routes[select.value];
    const result=core.checkRoute(path);
    host.dataset.result='checking';
    status.textContent='Checker: inspecting the proposed trajectory…';
    detail.textContent='Each position and move must satisfy the maze rules.';
    animate(result.index+1,110,i=>{
      const p=path[i];
      dot.setAttribute('cx',p[0]*32+16); dot.setAttribute('cy',p[1]*32+16);
      trace.setAttribute('points',path.slice(0,i+1).map(point).join(' '));
    },()=>{
      host.dataset.result=result.accepted?'accepted':'rejected';
      status.textContent=result.accepted?'Accepted: this trajectory solves the maze.':'Rejected: reaching the goal is not enough.';
      detail.textContent=result.reason+(result.accepted?' Green means accepted under these rules; it does not certify optimality.':'');
    });
  }
  function explore() {
    reset();
    const reachable=core.enumerateReachable();
    host.dataset.result='exploring';
    proposal.setAttribute('points','');
    status.textContent='Deterministic search: enumerating reachable positions…';
    detail.textContent='This search checks all four possible moves at each visited position.';
    animate(reachable.length,55,i=>{
      const p=reachable[i];
      cells.get(p.join(',')).classList.add('maze-visited');
      // This marker is a search cursor, not a claimed adjacent-step trajectory.
      dot.setAttribute('cx',p[0]*32+16); dot.setAttribute('cy',p[1]*32+16);
    },()=>{
      host.dataset.result='exhausted';
      status.textContent=`Exhaustive within this model: ${reachable.length} reachable positions checked.`;
      detail.textContent='The search queue is empty. Coverage is complete for reachable cell positions in this fixed maze; this does not enumerate every possible trajectory.';
    });
  }
  host.querySelector('[data-maze-run="check"]').addEventListener('click',check);
  host.querySelector('[data-maze-run="explore"]').addEventListener('click',explore);
  host.querySelector('[data-maze-reset]').addEventListener('click',reset);
  select.addEventListener('change',reset);
  pause.addEventListener('click',()=>{
    paused=!paused;
    pause.textContent=paused?'Resume':'Pause';
    if(paused) cancelAnimationFrame(frame);
    else {last=null; frame=requestAnimationFrame(tick);}
  });
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden && active && !paused) pause.click();
  });
  reset();
})();
