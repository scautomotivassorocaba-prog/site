#!/usr/bin/env python3
from pathlib import Path
import re,json
from PIL import Image,ImageDraw,ImageFont
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if not all(x in s for x in ['<head>','</head>','<section','id="servicos"','<footer']):
  raise RuntimeError('Unexpected homepage structure, refusing to change design')
# Remove previous SEO-only head declarations while retaining CSS, scripts and original site behavior.
s=re.sub(r'<title>[^<]*</title>','',s,count=1,flags=re.I)
s=re.sub(r'<meta\s+name=["\'](?:description|robots|twitter:card|twitter:title|twitter:description|twitter:image)["\'][^>]*>','',s,flags=re.I)
s=re.sub(r'<meta\s+property=["\'](?:og:[^"\']+)["\'][^>]*>','',s,flags=re.I)
s=re.sub(r'<link\s+rel=["\'](?:canonical|manifest|icon)["\'][^>]*>','',s,flags=re.I)
s=re.sub(r'<script\s+type=["\']application/ld\+json["\']\s*>.*?</script>','',s,flags=re.I|re.S)
base="https://site-zeta-steel.vercel.app"
biz={"@type":"AutoRepair","@id":"https://site-zeta-steel.vercel.app/#oficina","name":"SC Soluções Automotivas","alternateName":"San Custom Oficina","url":"https://site-zeta-steel.vercel.app/","telephone":"+5515997166028","image":"https://site-zeta-steel.vercel.app/assets/og-sc.jpg","address":{"@type":"PostalAddress","streetAddress":"Rua Anselmo Todesco, 21, Vila Colorau","addressLocality":"Sorocaba","addressRegion":"SP","addressCountry":"BR"},"areaServed":{"@type":"City","name":"Sorocaba"},"sameAs":["https://www.instagram.com/sancustom.oficina/"],"hasMap":"https://www.google.com/maps/search/?api=1&query=SC%20Solu%C3%A7%C3%B5es%20Automotivas%20Rua%20Anselmo%20Todesco%2021%20Sorocaba"}
home={"title":"Oficina Mecânica em Sorocaba | SC Soluções Automotivas","desc":"Oficina mecânica em Sorocaba: freios, suspensão, troca de óleo, revisão, injeção eletrônica, diagnóstico, embreagem e arrefecimento. SC Soluções Automotivas.","url":"https://site-zeta-steel.vercel.app/"}
seo='<title>'+home['title']+'</title>' + '<meta name="description" content="'+home['desc']+'">' + '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">' + '<link rel="canonical" href="'+home['url']+'">' + '<link rel="icon" type="image/svg+xml" href="/favicon.svg">' + '<link rel="manifest" href="/site.webmanifest">' + '<meta property="og:type" content="website">' + '<meta property="og:locale" content="pt_BR">' + '<meta property="og:site_name" content="SC Soluções Automotivas">' + '<meta property="og:title" content="'+home['title']+'">' + '<meta property="og:description" content="'+home['desc']+'">' + '<meta property="og:url" content="'+home['url']+'">' + '<meta property="og:image" content="'+base+'/assets/og-sc.jpg">' + '<meta property="og:image:width" content="1200">' + '<meta property="og:image:height" content="630">' + '<meta name="twitter:card" content="summary_large_image">' + '<meta name="twitter:title" content="'+home['title']+'">' + '<meta name="twitter:description" content="'+home['desc']+'">' + '<meta name="twitter:image" content="'+base+'/assets/og-sc.jpg">'
schema={"@context":"https://schema.org","@graph":[biz,{"@type":"WebSite","@id":base+"/#website","url":base+"/","name":"SC Soluções Automotivas","inLanguage":"pt-BR","publisher":{"@id":biz['@id']}},{"@type":"WebPage","@id":base+"/#webpage","url":base+"/","name":home['title'],"description":home['desc'],"inLanguage":"pt-BR","isPartOf":{"@id":base+"/#website"},"about":{"@id":biz['@id']}}]}
seo+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
if 'data-sc-seo="v20"' not in s:
  seo+='<link rel="stylesheet" href="/assets/sc-seo-links.css" data-sc-seo="v20">'
s=s.replace('</head>',seo+'</head>',1)
if 'class="sc-seo-hub-link"' not in s:
  match=re.search(r'<section[^>]+id="servicos"[^>]*>.*?</section>',s,flags=re.S|re.I)
  if not match:raise RuntimeError('Services section missing')
  section=match.group(0)
  block='<p class="sc-seo-hub-link"><a href="/servicos/">Conheça todos os serviços da SC em Sorocaba ↗</a></p>'
  section=section[:-len('</section>')]+block+'</section>'
  s=s[:match.start()]+section+s[match.end():]
if s.count('class="sc-seo-hub-link"')!=1:raise RuntimeError('Duplicate services hub link')
p.write_text(s,encoding='utf-8')
# Proper OG JPEG generated without external fonts, logos or unlicensed images.
img=Image.new('RGB',(1200,630),(9,13,19))
pix=img.load()
for y in range(630):
  for x in range(1200):
    red=max(0,1-((x-1050)**2/(960**2)+(y-40)**2/(550**2))**0.5)
    pix[x,y]=(int(9+40*red),int(13+5*red),int(19+12*red))
d=ImageDraw.Draw(img)
d.rounded_rectangle((74,62,210,200),radius=28,fill=(221,31,60))
try:
  heavy=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',82)
  title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',58)
  body=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',30)
  small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
except OSError:
  heavy=title=body=small=ImageFont.load_default()
d.text((85,77),'SC',fill='white',font=heavy)
d.text((240,90),'SOLUÇÕES AUTOMOTIVAS',fill='#ffffff',font=body)
d.text((75,260),'Oficina mecânica',font=title,fill='white')
d.text((75,333),'em Sorocaba.',font=title,fill='white')
d.rounded_rectangle((75,451,870,455),radius=2,fill=(228,35,61))
d.text((75,489),'Freios  •  Suspensão  •  Revisões  •  Diagnósticos',font=small,fill='#c9d0d9')
d.text((75,548),'Vila Colorau  |  (15) 99716-6028',font=small,fill='#c9d0d9')
out=Path('assets/og-sc.jpg');out.parent.mkdir(exist_ok=True,parents=True);img.save(out,format='JPEG',quality=91,optimize=True,subsampling=0)
print('Optimized home + generated',out, out.stat().st_size)
