#!/usr/bin/env python3
"""Install verified static thumbnail files for the three approved SC Reels.

Stops without changing the website if any thumbnail cannot be downloaded.
"""
from pathlib import Path
from hashlib import sha256
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time

ROOT = Path(__file__).resolve().parents[1]
COVERS = ROOT / "assets" / "reels"
REELS = (
    ("DewiD_-Mc2D", "Dia a dia da SC"),
    ("DeO9IT6szB_", "Um dos nossos trabalhos"),
    ("DdHvAaAseTP", "Acompanhe nossa oficina"),
)

def size_of_jpeg(blob):
    i = 2
    while i + 9 < len(blob):
        if blob[i] != 255:
            i += 1
            continue
        marker = blob[i + 1]
        i += 2
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > len(blob):
            break
        segment_size = int.from_bytes(blob[i:i+2], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if i + 7 > len(blob):
                break
            h = int.from_bytes(blob[i+3:i+5], "big")
            w = int.from_bytes(blob[i+5:i+7], "big")
            return w, h
        i += segment_size
    return (0, 0)

def fetch_cover(code):
    address = "https://www.instagram.com/p/" + code + "/media/?size=l"
    last = None
    for attempt in range(3):
        try:
            req = Request(address, headers={
                "User-Agent": "facebookexternalhit/1.1",
                "Accept": "image/jpeg,image/*;q=0.8",
            })
            with urlopen(req, timeout=20) as response:
                mime = response.headers.get("Content-Type", "").lower()
                data = response.read(2_000_001)
            width, height = size_of_jpeg(data)
            if not mime.startswith("image/jpeg") or len(data) < 10000 or len(data) > 2_000_000:
                raise ValueError("Unexpected response MIME or file size")
            if not (data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9")):
                raise ValueError("Response is not a complete JPEG")
            if width < 350 or height < 600 or height <= width:
                raise ValueError("Response is not a valid vertical Reel cover")
            print(code, width, height, len(data), sha256(data).hexdigest()[:16])
            return data
        except (HTTPError, URLError, ValueError, TimeoutError) as exc:
            last = exc
            if attempt < 2:
                time.sleep(2 + attempt * 3)
    raise RuntimeError("Failed to retrieve verified Instagram cover for " + code) from last

def javascript():
    return r'''/* SC - tres capas originais dos Reels selecionados; sem embed, curtidas ou scroll. */
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
})();'''

def main():
    # Retrieve and verify all three BEFORE writing anything.
    images = {code: fetch_cover(code) for code, _ in REELS}
    hashes = {sha256(data).hexdigest() for data in images.values()}
    if len(hashes) != len(REELS):
        raise ValueError("Duplicate thumbnail files: cannot guarantee matching Reels")
    COVERS.mkdir(parents=True, exist_ok=True)
    for code, data in images.items():
        (COVERS / (code + ".jpg")).write_bytes(data)
    (ROOT / "assets" / "sc-instagram-feed.js").write_text(javascript(), encoding="utf-8")
    print("Covers and static-only Instagram script updated.")

if __name__ == "__main__":
    main()
