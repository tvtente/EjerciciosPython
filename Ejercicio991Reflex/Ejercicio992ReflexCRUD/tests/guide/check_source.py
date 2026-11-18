"""Comprueba fidelidad del código y enlaces HTML/PowerPoint sin ejecutar Reflex."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import zipfile

ROOT=Path(__file__).resolve().parents[2]
html=(ROOT/'entregables/guia_crud_interactiva.html').read_text()
data=json.loads(re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',html,re.S).group(1))
class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.value=''
    def handle_data(self,value):self.value+=value
for file,record in data['files'].items():
    source=(ROOT/file).read_text();assert source==record['source']
    assert hashlib.sha256(source.encode()).hexdigest()==record['sha256']
    for original,rendered in zip(source.splitlines(),record['lines'],strict=True):
        parser=Text();parser.feed(rendered);assert parser.value==original,(file,original,parser.value)
for sid,s in data['symbols'].items():
    if 'file' in s:assert 1<=s['start']<=s['definition']<=s['end']<=len(data['files'][s['file']]['lines']),sid
for flow in data['flows'].values():
    assert flow['entry'] in data['symbols']
    assert flow['capture'] in data['screenshots']
    for step in flow['steps']:assert step['target'] in data['symbols']
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
source=ROOT/'entregables/CRUD_Reflex_interactivo_con_diagramas.pptx'
output=ROOT/'entregables/CRUD_Reflex_con_guia_HTML.pptx'
count=0
with zipfile.ZipFile(source) as old,zipfile.ZipFile(output) as new:
    for name in old.namelist():
        if name.startswith('ppt/media/'):assert old.read(name)==new.read(name),'Imagen modificada'
        if not re.fullmatch(r'ppt/slides/slide\d+\.xml',name):continue
        before=ET.fromstring(old.read(name));after=ET.fromstring(new.read(name))
        a=[n.text for n in before.findall('.//a:t',ns)];b=[n.text for n in after.findall('.//a:t',ns)]
        assert b[:-1]==a and b[-1]=='Explorar código ↗','El contenido anterior debe conservarse'
        rels=ET.fromstring(new.read(name.replace('slides/','slides/_rels/')+'.rels'))
        hrefs=[n.attrib['Target'] for n in rels if n.attrib.get('Type','').endswith('/hyperlink')]
        assert len(hrefs)==1
        path=urlsplit(hrefs[0]);assert path.path=='guia_crud_interactiva.html';query=parse_qs(path.fragment)
        assert query['symbol'][0] in data['symbols'];assert query['flow'][0] in data['flows'];count+=1
assert count==39
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=["\']https?://',html),'La guía debe funcionar sin recursos externos'
print('OK: código íntegro, rangos reales, capturas incluidas y 39 enlaces relativos a destinos válidos. Texto e imágenes anteriores del PowerPoint conservados.')
