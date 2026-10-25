/* SC Soluções Automotivas — V18. Expandir e recolher os cards de serviços. */
(()=>{
'use strict';
const section=document.querySelector('#servicos');
const grid=section?.querySelector('.service-grid');
if(!grid||grid.querySelectorAll(':scope > .service-card').length<7)return;
if(!grid.id)grid.id='scServicesGrid';
if(grid.nextElementSibling?.classList.contains('sc-services-toggle-wrap'))return;
const wrap=document.createElement('div');wrap.className='sc-services-toggle-wrap';
const button=document.createElement('button');button.className='sc-services-toggle';button.type='button';
button.setAttribute('aria-controls',grid.id);button.setAttribute('aria-expanded','false');
button.innerHTML='<span class="sc-services-toggle-text">Mostrar mais serviços</span><span class="sc-services-toggle-icon" aria-hidden="true">⌄</span>';
wrap.append(button);grid.insertAdjacentElement('afterend',wrap);
let expanded=false;
const render=()=>{grid.classList.toggle('sc-services-collapsed',!expanded);button.setAttribute('aria-expanded',String(expanded));button.querySelector('.sc-services-toggle-text').textContent=expanded?'Mostrar menos':'Mostrar mais serviços'};
button.addEventListener('click',()=>{expanded=!expanded;render()});
render();
})();
