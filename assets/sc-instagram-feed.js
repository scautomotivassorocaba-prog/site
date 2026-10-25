/* SC - publicacoes fixas: SOMENTE fotos clicaveis, sem embed Instagram. */
(()=>{
'use strict';
const root=document.querySelector('[data-sc-instagram-feed]');if(!root)return;
const chosen=[
{code:'DewiD_-Mc2D',title:'Dia a dia da SC',backup:'/assets/media/38788e61588a4b9a.webp'},
{code:'DeO9IT6szB_',title:'Trabalho na oficina',backup:'/assets/media/62d85892f3632cdc.webp'},
{code:'DdHvAaAseTP',title:'Mais da nossa oficina',backup:'/assets/media/c1c68a3ee7c63f25.webp'}
];
root.replaceChildren();
chosen.forEach(({code,title,backup},i)=>{
const url='https://www.instagram.com/reel/'+code+'/';
const card=document.createElement('article');card.className='sc-instagram-card';
const head=document.createElement('div');head.className='sc-instagram-card-head';
head.innerHTML='<span class="sc-instagram-account"><span class="sc-instagram-mark">SC</span><span class="sc-instagram-account-name">@sancustom.oficina</span></span><span class="sc-instagram-card-tag">REEL</span>';
const media=document.createElement('div');media.className='sc-instagram-content sc-instagram-static';
const a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener noreferrer';a.className='sc-instagram-poster';
a.setAttribute('aria-label','Abrir Reel '+(i+1)+' da SC no Instagram');
const fallback=document.createElement('img');fallback.src=backup;fallback.alt='Foto da SC Solucoes Automotivas. Abrir Reel no Instagram.';fallback.className='sc-instagram-poster-fallback';fallback.loading='lazy';fallback.decoding='async';
fallback.addEventListener('error',()=>{fallback.style.display='none';media.classList.add('sc-instagram-poster-unavailable')});
a.append(fallback);media.append(a);
// Tenta usar a capa publica original, caso o Instagram permita; sem bloquear a foto reserva.
const cover=new Image();cover.className='sc-instagram-original-cover';cover.alt='Capa do Reel da SC';cover.decoding='async';cover.loading='lazy';
cover.addEventListener('load',()=>{if(cover.naturalWidth>=180&&cover.naturalHeight>=180){a.append(cover);a.classList.add('sc-instagram-has-cover')}});
cover.src='https://www.instagram.com/p/'+code+'/media/?size=l';
const foot=document.createElement('div');foot.className='sc-instagram-card-foot';
const label=document.createElement('span');label.className='sc-instagram-card-label';label.textContent=title;
const more=document.createElement('a');more.className='sc-instagram-open';more.href=url;more.target='_blank';more.rel='noopener noreferrer';more.textContent='Ver reel ↗';
foot.append(label,more);card.append(head,media,foot);root.append(card);
});
const status=document.querySelector('[data-sc-instagram-status]');
if(status)status.textContent='Três Reels selecionados da SC. Toque na imagem para assistir no Instagram.';
})();