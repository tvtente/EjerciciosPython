#!/usr/bin/env python3
"""Añade enlaces relativos al HTML, conservando las diapositivas del original.

Ejecutar desde cualquier directorio. No cambia el PowerPoint de origen.
"""
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlencode
import re
import zipfile
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'entregables/CRUD_Reflex_interactivo_con_diagramas.pptx'
OUTPUT=ROOT/'entregables/CRUD_Reflex_con_guia_HTML.pptx'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
REL='http://schemas.openxmlformats.org/package/2006/relationships'
for prefix,uri in NS.items():ET.register_namespace(prefix,uri)
ET.register_namespace('',REL)

def route(title):
    t=title.casefold()
    if 'inicializ' in t or 'create_all' in t or 'init_database' in t or 'creación de tablas' in t:return 'init','init_database'
    if 'get_engine' in t or 'conexión' in t:return 'init','get_engine'
    if 'todoview' in t:return 'read','TodoView'
    if 'todo:' in t or 'representan una tarea' in t:return 'create','Todo'
    if 'session' in t:return 'create','concept:Session.commit'
    if 'valid' in t or '_report' in t:return 'create','validate_text'
    if 'todostate' in t:return 'create','TodoState'
    if 'todorepository' in t:return 'create','TodoRepository'
    if 'calculadas' in t or 'visible_todos' in t:return 'read','TodoState.visible_todos'
    if 'complet' in t or 'set_completed' in t:return 'completed','TodoState.toggle_complete'
    if 'elimin' in t:return 'delete','TodoState.delete_todo'
    if 'editar' in t or 'edición' in t:return 'update','TodoState.update_todo'
    if 'leer' in t or 'consultar' in t or 'sqlite a la lista' in t:return 'read','TodoState.load_todos'
    if 'crear' in t:return 'create','TodoState.add_todo'
    if 'interfaz' in t or 'index()' in t:return 'create','index'
    return 'create','TodoState.add_todo'

def main():
    assert (ROOT/'entregables/guia_crud_interactiva.html').is_file(),'Genera primero la guía HTML.'
    with zipfile.ZipFile(SOURCE) as src:
        parts={name:src.read(name) for name in src.namelist()}
    menu=None
    for path in sorted(parts):
        if re.fullmatch(r'ppt/slides/slide\d+\.xml',path):
            node=ET.fromstring(parts[path])
            for shape in node.findall('.//p:sp',NS):
                if ''.join(t.text or '' for t in shape.findall('.//a:t',NS))=='Menú':menu=deepcopy(shape);break
        if menu is not None:break
    assert menu is not None
    targets=[]
    for name in list(parts):
        if not re.fullmatch(r'ppt/slides/slide\d+\.xml',name):continue
        root=ET.fromstring(parts[name]);tree=root.find('p:cSld/p:spTree',NS);title=root.find('p:cSld',NS).attrib.get('name','')
        relation_path=name.replace('slides/','slides/_rels/')+'.rels';relations=ET.fromstring(parts[relation_path])
        existing_ids={r.attrib['Id'] for r in relations};index=1
        while 'rId'+str(index) in existing_ids:index+=1
        rid='rId'+str(index);flow,symbol=route(title);target='guia_crud_interactiva.html#'+urlencode({'flow':flow,'symbol':symbol})
        ET.SubElement(relations,f'{{{REL}}}Relationship',Id=rid,Type=NS['r']+'/hyperlink',Target=target,TargetMode='External')
        shape=deepcopy(menu);new_id=max(int(n.attrib['id']) for n in root.findall('.//p:cNvPr',NS))+1
        c=shape.find('p:nvSpPr/p:cNvPr',NS);c.set('id',str(new_id));c.set('name','Explorar código en la guía HTML')
        for h in shape.findall('.//a:hlinkClick',NS):
            h.set('{'+NS['r']+'}id',rid);h.attrib.pop('action',None);h.set('tooltip','Abrir el código navegable y su explicación')
        for text in shape.findall('.//a:t',NS):text.text='Explorar código ↗'
        transform=shape.find('p:spPr/a:xfrm',NS);transform.find('a:off',NS).set('x',str(720*9525));transform.find('a:off',NS).set('y',str(758*9525));transform.find('a:ext',NS).set('cx',str(245*9525));transform.find('a:ext',NS).set('cy',str(30*9525))
        tree.append(shape)
        parts[name]=ET.tostring(root,encoding='utf-8',xml_declaration=True);parts[relation_path]=ET.tostring(relations,encoding='utf-8',xml_declaration=True)
        targets.append((title,target))
    with zipfile.ZipFile(OUTPUT,'w',zipfile.ZIP_DEFLATED) as out:
        for name,content in parts.items():out.writestr(name,content)
    print(f'PowerPoint con {len(targets)} enlaces a la guía: {OUTPUT}')

if __name__=='__main__':main()
