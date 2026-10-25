#!/usr/bin/env python3
"""Build SC website V8 from prior inline V7, preserving gallery and scroll."""
from pathlib import Path
import re,base64,json,hashlib
root=Path('.')
s=(root/'index.html').read_text(encoding='utf8')
assert 'window.__SC_INLINE_FRAMES__' in s, 'Expected inline V7 source'
style=re.search(r'<style>(.*?)</style>',s,re.S)
logic=re.search(r'<script>\s*\(\(\)\s*=>.*?</script>',s,re.S)
frames=re.search(r'<script>\s*window\.__SC_INLINE_FRAMES__\s*=\s*(\[.*?\]);\s*</script>',s,re.S)
assert style and logic and frames
items=json.loads(frames.group(1))
assert len(items)==340,len(items)
mapping={}
for i,data in enumerate(items):
    assert data.startswith('data:image/webp;base64,')
    name=f'assets/frames/shot_{i:03d}.webp'
    f=root/name;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_bytes(base64.b64decode(data.split(',',1)[1]))
    mapping[data]=name
def unpack(m):
    src=m.group(0)
    if src in mapping:return mapping[src]
    mime,b64=src.split(';base64,',1)
    b=base64.b64decode(b64)
    ext='svg' if mime.endswith('svg+xml') else 'webp' if mime.endswith('webp') else 'png'
    name='assets/media/'+hashlib.sha256(b).hexdigest()[:16]+'.'+ext
    f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    mapping[src]=name
    return name
s=re.sub(r'data:image/(?:webp|png|svg\+xml);base64,[A-Za-z0-9+/=]+',unpack,s)
s=re.sub(r'<script>\s*window\.__SC_INLINE_FRAMES__\s*=\s*\[.*?\];\s*</script>','',s,flags=re.S)
def correct_gallery(m):
    tag=m.group(0)
    image=re.search(r'<img[^>]*src="([^"]+)"',tag)
    if image:return re.sub(r'data-photo="[^"]+"','data-photo="'+image.group(1)+'"',tag,count=1)
    return tag
s=re.sub(r'<button[^>]*class="[^"]*gallery-item[^"]*"[^>]*>\s*<img[^>]+>',correct_gallery,s,flags=re.S)
css=style.group(1)
fac=re.search(r'<img[^>]*alt="Foto real da fachada SC Soluções Automotivas em Sorocaba"[^>]*src="(assets/media/[^"]+)"',s)
assert fac, 'Real facade photo was not located'
hero=fac.group(1)
css=css.replace("../img/hero.webp",hero.replace("assets/media/","../media/"))
(root/'assets/css').mkdir(parents=True,exist_ok=True)
(root/'assets/js').mkdir(parents=True,exist_ok=True)
(root/'assets/css/base.css').write_text(css,encoding='utf8')
(root/'assets/css/refinements.css').write_bytes((root/'tools/refinements.css').read_bytes())
(root/'assets/js/app.js').write_text(logic.group(0)[8:-9],encoding='utf8')
s=re.sub(r'<style>.*?</style>','<link rel="stylesheet" href="assets/css/base.css">\n<link rel="stylesheet" href="assets/css/refinements.css">',s,count=1,flags=re.S)
s=re.sub(r'<script>\s*\(\(\)\s*=>.*?</script>','<script defer src="assets/js/app.js"></script>',s,count=1,flags=re.S)
s=s.replace('content="assets/img/hero.webp"','content="'+hero+'"')
s=s.replace('href="assets/img/hero.webp"','href="'+hero+'"')
svgs=sorted((root/'assets/media').glob('*.svg'))
if svgs:s=s.replace('assets/img/logo-sc.svg','assets/media/'+svgs[0].name)
s=s.replace('"postalCode":"18020-450",','')
(root/'index.html').write_text(s,encoding='utf8')
print('SC V8 built:',len(items),'frames,',len(mapping)-len(items),'other assets; HTML',len(s),'bytes')
