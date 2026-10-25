/* SC: Reels oficiais escolhidos manualmente pela cliente; não fazer substituição automática. */
(()=>{
'use strict';
const root=document.querySelector('[data-sc-instagram-feed]');if(!root)return;
const chosen=[
['DewiD_-Mc2D','Confira a rotina da SC'],
['DeO9IT6szB_','Um dos nossos trabalhos'],
['DdHvAaAseTP','Acompanhe nossa oficina']
];
root.replaceChildren();
chosen.forEach(([shortcode,label],i)=>{
const url='https://www.instagram.com/reel/'+shortcode+'/';
const card=document.createElement('article');card.className='sc-instagram-card';
const head=document.createElement('div');head.className='sc-instagram-card-head';
head.innerHTML='<span class="sc-instagram-account"><span class="sc-instagram-mark">SC</span><span class="sc-instagram-account-name">@sancustom.oficina</span></span><span class="sc-instagram-card-tag">REEL</span>';
const media=document.createElement('div');media.className='sc-instagram-content';
const backup=document.createElement('a');backup.href=url;backup.target='_blank';backup.rel='noopener noreferrer';backup.className='sc-instagram-placeholder';backup.setAttribute('aria-label','Abrir Reel '+(i+1)+' da SC no Instagram');
backup.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="18" cy="6.4" r="1"/></svg><span>Ver publicação no Instagram ↗</span>';
const frame=document.createElement('iframe');frame.loading='lazy';frame.src=url+'embed/captioned/';frame.title='Reel '+(i+1)+' do Instagram da SC';frame.referrerPolicy='strict-origin-when-cross-origin';frame.allow='encrypted-media; picture-in-picture';frame.addEventListener('load',()=>{backup.hidden=true});
media.append(backup,frame);
const foot=document.createElement('div');foot.className='sc-instagram-card-foot';
const caption=document.createElement('span');caption.className='sc-instagram-card-label';caption.textContent=label;
const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.className='sc-instagram-open';link.textContent='Ver reel ↗';
foot.append(caption,link);card.append(head,media,foot);root.append(card);
});
})();