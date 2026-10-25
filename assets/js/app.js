(() => {
  'use strict';
  const $ = q => document.querySelector(q);
  const $$ = q => [...document.querySelectorAll(q)];
  const nav=$('#nav'),menuBtn=$('#menuButton'),mobileNav=$('#mobileNav'),mobileCta=$('.mobile-cta');
  const setMenu=open=>{mobileNav.hidden=!open;menuBtn.setAttribute('aria-expanded',String(open));menuBtn.setAttribute('aria-label',open?'Fechar menu':'Abrir menu');document.body.classList.toggle('no-scroll',open)};
  menuBtn.addEventListener('click',()=>setMenu(mobileNav.hidden));
  mobileNav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!mobileNav.hidden)setMenu(false)});
  window.addEventListener('resize',()=>{if(innerWidth>920&&!mobileNav.hidden)setMenu(false)},{passive:true});
  if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){
    const ob=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');ob.unobserve(e.target)}}),{rootMargin:'0px 0px -25px 0px',threshold:.03});
    $$('.reveal').forEach(el=>ob.observe(el));
  }else $$('.reveal').forEach(el=>el.classList.add('is-visible'));

  const systems={
    motor:['Motor','O conjunto responsável pelo movimento. Uma avaliação cuidadosa ajuda a identificar a origem de possíveis falhas.'],
    suspensao:['Suspensão','Estabilidade, conforto e contato do veículo com o solo.'],
    freios:['Freios','Componentes importantes para a segurança na condução.'],
    injecao:['Injeção eletrônica','Sensores e componentes que influenciam o funcionamento do motor.']
  };
  $$('.system-tab').forEach(btn=>btn.addEventListener('click',()=>{
    $$('.system-tab').forEach(b=>{const on=b===btn;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on))});
    const [title,description]=systems[btn.dataset.system];$('#systemName').textContent=title;$('#systemDesc').textContent=description;
  }));

  // The canvas NEVER clears between seeks. It draws only decoded frames, so scrolling
  // cannot briefly expose the black container while a new image is loading.
  const frameCount=340;
  const urls=window.__SC_INLINE_FRAMES__ || Array.from({length:frameCount},(_,i)=>'assets/frames/shot_'+String(i).padStart(3,'0')+'.webp');
  const zone=$('#storyScroller'),sticky=$('#storySticky'),canvas=$('#storyCanvas'),poster=$('#storyFrame'),caption=$('.story-caption'),bar=$('#storyProgress');
  const ctx=canvas.getContext('2d',{alpha:false,desynchronized:false});
  const cache=new Map();const inFlight=new Set();const jobs=[];
  let target=0,displayed=-1,raf=false,active=false,simultaneous=0,latestProgress=0;
  const MAX_PENDING=4,MAX_CACHE=50;

  function addJob(i){if(i<0||i>=frameCount||cache.has(i)||inFlight.has(i)||jobs.includes(i))return;jobs.push(i)}
  function enqueueNear(index){
    // Prioritize the requested frame, then immediate neighbors and scroll direction.
    const offset=[0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,8,-8,10,-10,12,-12];
    offset.forEach(d=>addJob(index+d));
    if(jobs.length>100)jobs.splice(0,jobs.length-100);
    runQueue();
  }
  function runQueue(){
    jobs.sort((a,b)=>Math.abs(a-target)-Math.abs(b-target));
    while(simultaneous<MAX_PENDING&&jobs.length){
      const i=jobs.shift();if(cache.has(i)||inFlight.has(i))continue;
      simultaneous++;inFlight.add(i);
      const image=new Image();image.decoding='async';
      let settled=false;
      const finish=(success)=>{
        if(settled)return;settled=true;simultaneous--;inFlight.delete(i);
        if(success&&image.naturalWidth>0){cache.set(i,image);prune();schedule();}
        runQueue();
      };
      image.onload=()=>{if(typeof image.decode==='function')image.decode().then(()=>finish(true),()=>finish(true));else finish(true)};
      image.onerror=()=>finish(false);
      image.src=urls[i];
    }
  }
  function prune(){
    if(cache.size<=MAX_CACHE)return;
    [...cache.keys()].sort((a,b)=>Math.abs(b-target)-Math.abs(a-target))
      .slice(0,cache.size-MAX_CACHE).forEach(i=>cache.delete(i));
  }
  function resize(){
    const r=canvas.getBoundingClientRect();if(r.width<1||r.height<1)return;
    const dpr=Math.min(devicePixelRatio||1,1.6,Math.sqrt(2300000/(r.width*r.height)));
    const w=Math.max(1,Math.round(r.width*dpr)),h=Math.max(1,Math.round(r.height*dpr));
    if(canvas.width!==w||canvas.height!==h){
      const previous=displayed;
      canvas.width=w;canvas.height=h;
      displayed=-1;
      // Resizing resets the canvas pixels. Repaint an already decoded frame on
      // the SAME tick; if there is none yet, expose the poster rather than black.
      if(cache.has(previous)) draw(cache.get(previous),previous);
      else if(cache.has(target)) draw(cache.get(target),target);
      else canvas.classList.remove('ready');
      render();
    }
  }
  function draw(image,index){
    if(!ctx||!image||!image.naturalWidth)return;
    const cw=canvas.width,ch=canvas.height,iw=image.naturalWidth,ih=image.naturalHeight;
    // Do not crop the SC sign during the last part of the animation on phones.
    const fitLogo=(index/(frameCount-1)>.83 && innerWidth<730);
    const scale=fitLogo?Math.min(cw/iw,ch/ih):Math.max(cw/iw,ch/ih);
    const w=iw*scale,h=ih*scale;
    ctx.fillStyle='#14191e';ctx.fillRect(0,0,cw,ch);
    if(fitLogo){
      // Soft fill matches the sign, instead of leaving two oversized black bands.
      const backScale=Math.max(cw/iw,ch/ih)*1.12;
      const bw=iw*backScale,bh=ih*backScale;
      ctx.save();ctx.filter='blur(26px) brightness(.40)';
      ctx.drawImage(image,(cw-bw)/2,(ch-bh)/2,bw,bh);
      ctx.restore();
    }
    ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
    ctx.drawImage(image,(cw-w)/2,(ch-h)/2,w,h);
    displayed=index;canvas.classList.add('ready');
  }
  function render(){
    if(!ctx)return;
    // If the target is not decoded, keep the LAST decoded image in place. Never set
    // a new <img>.src during scroll and never blank the canvas to indicate loading.
    // Hold the last decoded frame while a new target is loading. Do not
    // display arbitrary intermediate frames from out-of-order network requests.
    if(cache.has(target)){
      if(displayed!==target)draw(cache.get(target),target);
    }else if(displayed<0){
      let nearest=-1,dist=Infinity;
      for(const i of cache.keys()){
        const d=Math.abs(i-target);
        if(d<dist){nearest=i;dist=d;}
      }
      if(nearest>=0&&dist<=8)draw(cache.get(nearest),nearest);
      // Otherwise keep the original <img> poster visible.
    }
  }
  function progress(){
    const rect=zone.getBoundingClientRect(),travel=Math.max(1,rect.height-sticky.getBoundingClientRect().height);
    return Math.min(1,Math.max(0,-rect.top/travel));
  }
  function update(){
    raf=false;
    latestProgress=progress();target=Math.min(frameCount-1,Math.round(latestProgress*(frameCount-1)));
    bar.style.width=(latestProgress*100).toFixed(2)+'%';
    caption.classList.toggle('is-ending',latestProgress>.27);
    nav.classList.toggle('is-scrolled',scrollY>40);
    if(mobileCta)mobileCta.classList.toggle('is-visible',scrollY>innerHeight*.73);
    // During ordinary site scroll don't queue 340 images until the user approaches video.
    const r=zone.getBoundingClientRect();
    active=r.bottom>-innerHeight&&r.top<innerHeight*2;
    if(active)enqueueNear(target);
    render();
    window.__scScrollQA={target,displayed,progress:latestProgress,decoded:cache.size,loading:simultaneous};
  }
  function schedule(){if(!raf){raf=true;requestAnimationFrame(update)}}
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting)){enqueueNear(0);observer.disconnect()}},{rootMargin:'1200px 0px'});
    observer.observe(zone);
  }else enqueueNear(0);
  poster.addEventListener('load',schedule);
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',()=>{resize();schedule()},{passive:true});
  if('ResizeObserver' in window) new ResizeObserver(()=>{resize();schedule()}).observe(canvas);
  resize();schedule();

  const dialog=$('#lightbox'),full=$('#lightboxImage'),close=$('#lightboxClose');
  $$('.gallery-item').forEach(btn=>btn.addEventListener('click',()=>{full.src=btn.dataset.photo;full.alt=btn.dataset.alt||'Foto ampliada';if(dialog.showModal)dialog.showModal()}));
  close.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
  $('#year').textContent=String(new Date().getFullYear());
})();
