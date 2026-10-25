/* SC - tres capas originais dos Reels selecionados; sem embed, curtidas ou scroll. */
(()=>{
"use strict";
const root=document.querySelector("[data-sc-instagram-feed]");if(!root)return;
const chosen=[
["DewiD_-Mc2D","Dia a dia da SC"],
["DeO9IT6szB_","Um dos nossos trabalhos"],
["DdHvAaAseTP","Acompanhe nossa oficina"]
];
root.replaceChildren();
chosen.forEach(([code,title],i)=>{
 const url="https://www.instagram.com/reel/"+code+"/";
 const card=document.createElement("article");card.className="sc-instagram-card";
 const head=document.createElement("div");head.className="sc-instagram-card-head";
 head.innerHTML='<span class="sc-instagram-account"><span class="sc-instagram-mark">SC</span><span class="sc-instagram-account-name">@sancustom.oficina</span></span><span class="sc-instagram-card-tag">REEL</span>';
 const media=document.createElement("div");media.className="sc-instagram-content sc-instagram-static";
 const a=document.createElement("a");a.href=url;a.target="_blank";a.rel="noopener noreferrer";a.className="sc-instagram-poster";
 a.setAttribute("aria-label","Abrir Reel "+(i+1)+" da SC no Instagram");
 const img=document.createElement("img");img.src="/assets/reels/"+code+".jpg";img.className="sc-instagram-poster-fallback";
 img.alt="Capa original do Reel "+(i+1)+" da SC no Instagram";img.loading="lazy";img.decoding="async";
 img.addEventListener("error",()=>{img.remove();media.classList.add("sc-instagram-poster-unavailable");a.textContent="Abrir Reel no Instagram ↗";});
 a.append(img);media.append(a);
 const foot=document.createElement("div");foot.className="sc-instagram-card-foot";
 const caption=document.createElement("span");caption.className="sc-instagram-card-label";caption.textContent=title;
 const link=document.createElement("a");link.href=url;link.target="_blank";link.rel="noopener noreferrer";
 link.className="sc-instagram-open";link.textContent="Ver reel ↗";
 foot.append(caption,link);card.append(head,media,foot);root.append(card);
});
const status=document.querySelector("[data-sc-instagram-status]");
if(status)status.textContent="Três Reels selecionados. Clique em uma capa para assistir no Instagram.";
})();