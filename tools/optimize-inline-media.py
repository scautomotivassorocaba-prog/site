#!/usr/bin/env python3
"""Extract embedded base64 images without changing visual markup or URLs for visitors."""
from pathlib import Path
import base64, hashlib, re
import xml.etree.ElementTree as ET

htmlpath=Path("index.html")
html=htmlpath.read_text(encoding="utf-8")
pattern=re.compile(r"data:image/(webp|jpeg|png|svg\+xml);base64,([A-Za-z0-9+/=]+)")
folder=Path("assets/seo-extracted")
written={}
replaced=0

def externalize(match):
    global replaced
    media,b64=match.groups()
    payload=base64.b64decode(b64,validate=True)
    if media=="webp" and not (payload[:4]==b"RIFF" and payload[8:12]==b"WEBP"):
        raise ValueError("Invalid WebP embedded source")
    if media=="jpeg" and not (payload[:3]==b"\xff\xd8\xff" and payload[-2:]==b"\xff\xd9"):
        raise ValueError("Invalid JPEG embedded source")
    if media=="png" and not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Invalid PNG embedded source")
    if media=="svg+xml": ET.fromstring(payload)
    extension={"webp":"webp","jpeg":"jpg","png":"png","svg+xml":"svg"}[media]
    digest=hashlib.sha256(payload).hexdigest()[:16]
    filename=digest+"."+extension
    folder.mkdir(exist_ok=True,parents=True)
    path=folder/filename
    if path.exists() and path.read_bytes()!=payload:raise ValueError("Hash filename collision")
    if not path.exists():path.write_bytes(payload)
    written[filename]=len(payload)
    replaced+=1
    return "/assets/seo-extracted/"+filename

newhtml=pattern.sub(externalize,html)
if replaced:
    htmlpath.write_text(newhtml,encoding="utf-8")
else:
    print("No embedded images remain")
# Confirm every extracted path is in place and the document still has key features.
assert "id=\"servicos\"" in newhtml and "id=\"experiencia\"" in newhtml
assert "rel=\"canonical\"" in newhtml
assert not pattern.search(newhtml)
for filename in written:
    assert (folder/filename).exists()
print("Images extracted:",replaced,"distinct:",len(written))
print("HTML size bytes:",len(html.encode()),"->",len(newhtml.encode()))
