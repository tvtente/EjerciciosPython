#!/usr/bin/env python3
"""Genera una guía HTML autónoma desde el código real, sin ejecutar la aplicación.

Uso: python3 scripts/generar_guia_crud.py
Solo utiliza la biblioteca estándar. No lee ni modifica la base de datos.
"""
from __future__ import annotations
import ast
import base64
from datetime import datetime
import hashlib
import html
import io
import json
import keyword
from pathlib import Path
import tokenize
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
FILES = ['todo_app/models.py', 'todo_app/database.py', 'todo_app/repository.py', 'todo_app/todo_app.py', 'rxconfig.py']
TEMPLATE = ROOT / 'docs/guia_crud.template.html'
OUTPUT = ROOT / 'entregables/guia_crud_interactiva.html'

# Explanations describe this implementation. Source and line ranges come from AST.
EXPLANATIONS = {
'Todo': ('Modelo de tabla', 'Cada objeto representa una tarea. table=True registra su tabla y __tablename__ fija el nombre todos.', 'El repositorio usa este modelo en las operaciones del CRUD. El id identifica una fila y created_at se calcula para cada instancia.'),
'utc_now': ('Fecha de creación', 'Devuelve la fecha actual con zona UTC.', 'default_factory=utc_now hace que cada nueva tarea reciba su propia fecha, cuando se construye el objeto.'),
'TodoView': ('Datos para la interfaz', 'Esta dataclass describe los datos que el repositorio devuelve a la pantalla.', 'No define una tabla. Permite usar los datos después de cerrar la sesión e incluye una fecha formateada.'),
'as_view': ('Conversión de una fila', 'Convierte un Todo en TodoView y prepara los textos y las fechas.', 'Trata la fecha sin zona como UTC, la muestra en Europe/Madrid y convierte una descripción ausente en una cadena vacía.'),
'get_engine': ('Conexión a los datos', 'Obtiene el motor que usarán las sesiones. Lee TODO_DATABASE_URL o prepara data/todos.db.', 'La ruta parte de la carpeta del proyecto. lru_cache reutiliza el motor. Preparar el motor no equivale a crear las tablas.'),
'init_database': ('Creación de tablas', 'Importa Todo para registrar la tabla y llama a SQLModel.metadata.create_all().', 'Crea las tablas faltantes y conserva los datos. No aplica automáticamente cambios de columnas a una tabla existente.'),
'TodoRepository': ('Acceso a SQLite', 'Agrupa las operaciones de persistencia y recibe un motor opcional.', 'Cada operación abre su propia Session. Esta clase concentra las escrituras y consultas que solicitan los eventos.'),
'TodoRepository.__init__': ('Construcción del repositorio', 'Conserva el motor recibido o llama a get_engine() si no hay uno.', 'Crear TodoRepository() prepara el acceso. initialize() es quien solicita después la creación de tablas.'),
'TodoRepository.initialize': ('Inicialización del repositorio', 'Delega en init_database(self.engine).', 'load_todos() la ejecuta antes de consultar. La definición de las tablas queda en los modelos.'),
'TodoRepository.list_all': ('R · Consultar tareas', 'Consulta todos los Todo y los ordena por fecha descendente y después por id descendente.', 'Transforma cada fila con as_view() y devuelve una lista de TodoView al estado.'),
'TodoRepository.create': ('C · Crear una tarea', 'Valida el texto, construye Todo y ejecuta add(), commit() y refresh().', 'Devuelve as_view(todo). add_todo() no utiliza ese valor devuelto: vuelve a consultar la lista después de guardar.'),
'TodoRepository.edit': ('U · Editar textos', 'Valida el texto y busca la tarea por su clave primaria con session.get().', 'Si existe, cambia título y descripción y confirma con commit(). Conserva el id, la fecha y completed.'),
'TodoRepository.set_completed': ('U · Completar una tarea', 'Actualiza únicamente completed para el id recibido.', 'Guarda el valor de la casilla, comprueba que rowcount sea 1 y confirma la operación. Informa si la fila ya no existe.'),
'TodoRepository.delete': ('D · Eliminar una tarea', 'Busca la fila por su id, la marca con session.delete() y confirma con commit().', 'Si la tarea ya no existe, lanza ValueError. La confirmación visual ocurre antes, en dialogs().'),
'validate_text': ('Reglas de entrada', 'Elimina espacios de los extremos y exige un título no vacío.', 'Los máximos son 160 caracteres en el título y 3000 en la descripción. Devuelve None si la descripción queda vacía. Se usa al crear y al editar.'),
'TodoState': ('Estado de la pantalla', 'Mantiene las tareas cargadas, los campos del formulario, los filtros y los diálogos.', 'Sus eventos coordinan la interfaz y el repositorio. Las tareas persistentes viven en SQLite.'),
'TodoState.load_todos': ('R · Cargar y actualizar', 'Crea un repositorio, lo inicializa y asigna repo.list_all() a self.todos.', 'on_load, el botón Actualizar y los eventos de escritura usan este método. Si falla, coloca un mensaje en self.error.'),
'TodoState.add_todo': ('C · Evento de alta', 'Envía new_title y new_description al repositorio mediante create().', 'Si guarda correctamente, vacía los campos, llama a load_todos() y muestra un aviso. Si falla create(), conserva los campos.'),
'TodoState.toggle_complete': ('U · Evento de la casilla', 'Recibe el id y el valor marcado y llama a set_completed().', 'Tras guardar, ejecuta load_todos(). Recibe el valor deseado, en vez de invertir una copia antigua del estado.'),
'TodoState.start_edit': ('Abrir el diálogo de edición', 'Busca la tarea entre las cargadas y copia su id y sus textos a los campos de edición.', 'Abre edit_open. Todavía no modifica la base de datos. Guardar cambios dispara update_todo().'),
'TodoState.update_todo': ('U · Guardar una edición', 'Envía editing_id, edit_title y edit_description a TodoRepository.edit().', 'Tras el éxito cierra el diálogo y recarga. Si edit() falla, deja el mensaje en edit_error y conserva la edición.'),
'TodoState.ask_delete': ('Preparar la confirmación', 'Guarda el id y el título de la tarea y abre delete_open.', 'Todavía no borra la fila. El botón Sí, eliminar dispara delete_todo().'),
'TodoState.delete_todo': ('D · Confirmar el borrado', 'Envía delete_id a TodoRepository.delete().', 'Después cierra el diálogo, reinicia delete_id, llama a load_todos() y devuelve el aviso de eliminación.'),
'TodoState.visible_todos': ('Filtro calculado', '@rx.var obtiene una vista filtrada de self.todos por texto y estado.', 'strip() limpia la búsqueda y casefold() permite comparar sin distinguir mayúsculas. Filtrar no modifica SQLite.'),
'TodoState.total': ('Contador de tareas', 'Devuelve len(self.todos).', 'Cuenta todas las tareas cargadas, aunque el filtro solo muestre una parte.'),
'TodoState.completed_count': ('Contador de completadas', 'Suma los valores completed de todas las tareas cargadas.', 'En Python, True suma 1 y False suma 0. Este contador tampoco depende del filtro visible.'),
'TodoState._report': ('Errores comprensibles', 'Devuelve el texto de ValueError para que el usuario pueda corregir la acción.', 'Para otros errores registra el detalle con logger.exception() y devuelve un mensaje general.'),
'TodoState.set_filter': ('Cambiar el filtro', 'Acepta únicamente Todas, Pendientes o Completadas.', 'Modifica status_filter. visible_todos utiliza ese valor para calcular qué tareas aparecen.'),
'todo_item': ('Una tarea en pantalla', 'Construye la casilla, los textos, la fecha y los botones de una tarea.', 'Conecta la casilla con toggle_complete(), Editar con start_edit() y Eliminar con ask_delete().'),
'todo_form': ('Formulario de creación', 'Enlaza los controles con new_title y new_description y sus setters.', 'El envío llama a add_todo(). El código utiliza los valores del estado, no el diccionario del formulario.'),
'todo_list': ('Representación de la lista', 'rx.cond elige entre mostrar tareas o el mensaje de vista vacía.', 'rx.foreach crea un todo_item() por cada elemento de visible_todos.'),
'dialogs': ('Edición y confirmación', 'Construye el formulario de edición y el diálogo de eliminación.', 'Guardar cambios llama a update_todo(). Sí, eliminar llama a delete_todo(). Los campos open se enlazan con el estado.'),
'index': ('Composición de la página', 'Reúne el formulario, la lista, los filtros, los contadores y los diálogos.', 'Al final del archivo, app.add_page() registra esta página con on_load=TodoState.load_todos.'),
'rxconfig': ('Configuración del proyecto', 'Declara el nombre de la aplicación, el tema y sus puertos.', 'El frontend usa 3001 y el backend 8001. La conexión propia a SQLite se configura en database.py.'),
}
CONCEPTS = {
'Session': ('Session', 'Una sesión organiza las consultas y escrituras contra el motor.', 'El bloque with cierra la sesión al terminar la operación. Este símbolo pertenece a SQLModel, fuera del código del proyecto.'),
'Session.add': ('session.add()', 'Registra un objeto en la sesión.', 'commit() confirma la transacción. En este proyecto aparece al crear y al editar.'),
'Session.commit': ('session.commit()', 'Confirma la transacción en la base de datos.', 'Las operaciones de escritura del repositorio la ejecutan antes de terminar.'),
'Session.refresh': ('session.refresh()', 'Vuelve a leer el registro y actualiza el objeto con los valores de la base.', 'create() la usa después de commit(), antes de construir el TodoView.'),
'Session.get': ('session.get()', 'Obtiene una fila por la clave primaria de su modelo.', 'edit() y delete() comprueban si devuelve None para detectar una tarea inexistente.'),
'Session.exec': ('session.exec()', 'Ejecuta una consulta o una sentencia dentro de la sesión.', 'list_all() ejecuta un select. set_completed() ejecuta un update.'),
'Session.delete': ('session.delete()', 'Marca la instancia para su eliminación.', 'El repositorio confirma después el borrado mediante commit().'),
'select': ('select()', 'Construye la consulta que recupera las tareas.', 'order_by() establece el orden y all() materializa la colección de resultados.'),
'update': ('update()', 'Construye una sentencia de actualización.', 'where() limita la tarea por id. values() especifica el nuevo valor de completed.'),
'create_engine': ('create_engine()', 'Prepara un motor a partir de una URL de base de datos.', 'get_engine() define la ruta SQLite y sus opciones de conexión.'),
'SQLModel.metadata.create_all': ('metadata.create_all()', 'Crea las tablas registradas que todavía no existen.', 'No transforma las columnas de una tabla existente. Por eso este proyecto distingue creación inicial y migraciones.'),
'rx.event': ('@rx.event', 'Marca un método del estado como manejador de eventos de Reflex.', 'Los componentes lo conectan a acciones como on_change, on_submit u on_click.'),
'rx.var': ('@rx.var', 'Declara una variable calculada a partir del estado.', 'El proyecto lo utiliza para visible_todos, total y completed_count.'),
'rx.foreach': ('rx.foreach()', 'Describe cómo representar cada elemento de una colección reactiva.', 'todo_list() lo conecta con visible_todos y todo_item().'),
'rx.cond': ('rx.cond()', 'Elige un componente o valor según una condición reactiva.', 'Aparece en el estado vacío, los errores y la presentación de tareas completadas.'),
'SQLModel': ('SQLModel', 'Combina modelos Python con el acceso a tablas relacionales.', 'Todo hereda de esta clase y declara table=True.'),
'Field': ('Field()', 'Añade propiedades a los campos de un modelo.', 'En Todo define la clave primaria, límites y valores por defecto.'),
}
CONCEPT_DOCS = {'Session':'https://sqlmodel.tiangolo.com/tutorial/insert/','rx':'https://reflex.dev/docs/events/events-overview/','SQLModel':'https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/'}


def build():
    files={p:(ROOT/p).read_text(encoding='utf-8') for p in FILES}
    trees={p:ast.parse(s) for p,s in files.items()}
    symbols={}; node_symbols={}
    def register(node,file,parent=None):
        sid=f'{parent}.{node.name}' if parent else node.name
        start=min([node.lineno]+[d.lineno for d in getattr(node,'decorator_list',[])])
        end=node.end_lineno
        kind='class' if isinstance(node,ast.ClassDef) else ('method' if parent else 'function')
        focus_end=end
        if kind=='class':
            methods=[n for n in node.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
            if methods:focus_end=min(n.lineno for n in methods)-1
        title,desc,role=EXPLANATIONS.get(sid,('', '', ''))
        if not desc and node.name.startswith('set_'):
            target=node.name[4:]
            title='Actualizar un campo del estado';desc=f'Actualiza {target} con el valor recibido del control.';role='El evento conserva el valor que utiliza la interfaz. Esta función no escribe en SQLite.'
        symbols[sid]=dict(id=sid,name=node.name,file=file,start=start,end=end,definition=node.lineno,focusEnd=focus_end,kind=kind,parent=parent,title=title or node.name,description=desc,role=role,calls=[],references=[],usedBy=[])
        node_symbols[id(node)]=sid
        if kind=='class':
            for child in node.body:
                if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)):register(child,file,sid)
                elif isinstance(child,ast.AnnAssign) and isinstance(child.target,ast.Name):
                    field=child.target.id;fid=f'{sid}.{field}'
                    symbols[fid]=dict(id=fid,name=field,file=file,start=child.lineno,end=child.end_lineno,definition=child.lineno,focusEnd=child.end_lineno,kind='field',parent=sid,title=f'Campo {field}',description=f'{field} es un atributo de {sid}.',role=('Su valor forma parte del estado de la interfaz.' if sid=='TodoState' else 'Su anotación declara el tipo de dato que maneja el modelo.'),calls=[],references=[],usedBy=[])
    for file,tree in trees.items():
        for node in tree.body:
            if isinstance(node,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):register(node,file)
    symbols['rxconfig']=dict(id='rxconfig',name='rxconfig.py',file='rxconfig.py',start=1,end=len(files['rxconfig.py'].splitlines()),definition=1,focusEnd=len(files['rxconfig.py'].splitlines()),kind='module',parent=None,title=EXPLANATIONS['rxconfig'][0],description=EXPLANATIONS['rxconfig'][1],role=EXPLANATIONS['rxconfig'][2],calls=[],references=[],usedBy=[])
    for key,value in CONCEPTS.items():
        symbols['concept:'+key]=dict(id='concept:'+key,name=value[0],kind='concept',title=value[0],description=value[1],role=value[2],calls=[],references=[],usedBy=[],docs=CONCEPT_DOCS['rx' if key.startswith('rx.') else 'Session' if key.startswith('Session') else 'SQLModel'])
    links={f:{} for f in files}
    def charcol(file,line,byte):return len(files[file].splitlines()[line-1].encode('utf-8')[:byte].decode('utf-8'))
    def direct_name(expr):
        if isinstance(expr,ast.Name):return expr.id
        if isinstance(expr,ast.Attribute):return direct_name(expr.value)+'.'+expr.attr
        if isinstance(expr,ast.Call):return direct_name(expr.func)+'()'
        return ''
    class Resolver(ast.NodeVisitor):
        def __init__(self,file):self.file=file;self.current=None;self.owner=None
        def resolve(self,node):
            name=direct_name(node)
            key=name.replace('TodoRepository().','TodoRepository.').replace('repo.','TodoRepository.',1) if name.startswith(('repo.','TodoRepository().')) else name
            if key.startswith('self.') and self.owner:key=self.owner+key[4:]
            if key in symbols:return key
            if key.startswith('session.') and 'concept:Session.'+key[8:] in symbols:return 'concept:Session.'+key[8:]
            if 'concept:'+key in symbols:return 'concept:'+key
            return None
        def record(self,node,target):
            if not target:return
            if isinstance(node,ast.Name):line=node.lineno;col=charcol(self.file,line,node.col_offset)
            elif isinstance(node,ast.Attribute):line=node.end_lineno;col=charcol(self.file,line,node.end_col_offset)-len(node.attr)
            else:return
            links[self.file][(line,col)]=target
            if self.current and target!=self.current and target not in symbols[self.current]['references']:symbols[self.current]['references'].append(target)
        def visit_ClassDef(self,node):
            prior=self.owner,self.current;self.owner=node.name;self.current=node_symbols[id(node)];self.generic_visit(node);self.owner,self.current=prior
        def visit_FunctionDef(self,node):
            prior=self.current;self.current=node_symbols[id(node)];self.generic_visit(node);self.current=prior
        def visit_Name(self,node):self.record(node,self.resolve(node))
        def visit_Attribute(self,node):self.record(node,self.resolve(node));self.generic_visit(node)
        def visit_Call(self,node):
            target=self.resolve(node.func)
            if self.current and target and target not in symbols[self.current]['calls']:symbols[self.current]['calls'].append(target)
            self.generic_visit(node)
    for file,tree in trees.items():Resolver(file).visit(tree)
    for sid,s in list(symbols.items()):
        if s['kind']=='concept':continue
        # Definition names also work as stable links.
        line=files[s['file']].splitlines()[s['definition']-1]
        if s['kind'] not in ('module','field'):
            col=line.index(s['name'],line.index('class ')+6 if s['kind']=='class' else line.index('def ')+4)
            links[s['file']][(s['definition'],col)]=sid
        for target in s['references']:
            if sid not in symbols[target]['usedBy']:symbols[target]['usedBy'].append(sid)
    rendered={}
    for file,source in files.items():
        rows=source.splitlines();parts=[[] for _ in rows]
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type in (tokenize.ENCODING,tokenize.ENDMARKER,tokenize.INDENT,tokenize.DEDENT,tokenize.NEWLINE,tokenize.NL):continue
            sl,sc=token.start;el,ec=token.end
            style={tokenize.STRING:'str',tokenize.COMMENT:'comment',tokenize.NUMBER:'num',tokenize.OP:'op'}.get(token.type,'kw' if keyword.iskeyword(token.string) else '')
            for n in range(sl,min(el,len(rows))+1):
                a=sc if n==sl else 0;c=ec if n==el else len(rows[n-1]);value=html.escape(rows[n-1][a:c]);target=links[file].get((n,a)) if token.type==tokenize.NAME else None
                if target:value=f'<a href="#symbol={html.escape(target,quote=True)}" data-symbol="{html.escape(target,quote=True)}" class="code-ref" title="Ver {html.escape(target,quote=True)}">{value}</a>'
                elif style:value=f'<span class="tok-{style}">{value}</span>'
                parts[n-1].append((a,c,value))
        out=[]
        for n,(line,spans) in enumerate(zip(rows,parts),1):
            pos=0;frag=[]
            for a,c,v in sorted(spans):
                if a<pos:continue
                frag.extend([html.escape(line[pos:a]),v]);pos=c
            frag.append(html.escape(line[pos:]));out.append(''.join(frag))
        rendered[file]=dict(source=source,lines=out,sha256=hashlib.sha256(source.encode()).hexdigest())
    # Reuse the checked diagrams' actual message sequences and embedded screenshots.
    sequences=json.loads((ROOT/'docs/guia_recorridos.json').read_text())
    byid={d['id']:d for d in sequences}
    flow_specs={
    'create':('Crear','flow_create','TodoState.add_todo','create_code'), 'read':('Leer','flow_read','TodoState.load_todos','read_code'),
    'update':('Editar','flow_update','TodoState.start_edit','update_code'), 'completed':('Completar','flow_completed','TodoState.toggle_complete','completed_code'),
    'delete':('Eliminar','flow_delete','TodoState.ask_delete','delete_code'), 'init':('Inicializar','flow_init','TodoRepository.__init__','db_code')}
    destination={
    'create_code':'TodoRepository.create','read_code':'TodoRepository.list_all','update_code':'TodoRepository.edit','completed_code':'TodoRepository.set_completed','delete_code':'TodoRepository.delete',
    'repo_code':'TodoRepository.initialize','db_code':'init_database','model_code':'Todo','ui_code':'todo_list','state':'TodoState','repo':'TodoRepository','engine':'get_engine','init':'init_database','ui':'todo_list','view':'as_view','transaction':'concept:Session.commit','update':'TodoState.start_edit','completed':'TodoRepository.set_completed','delete':'TodoState.ask_delete','flow_read':'TodoState.load_todos','flow_init':'init_database'}
    overrides={
    'create':['TodoState.add_todo','TodoRepository.create','concept:Session.commit','TodoRepository.create','as_view','TodoState.load_todos','todo_list'],
    'read':['TodoState.load_todos','TodoRepository.initialize','TodoRepository.list_all','concept:select','as_view','TodoState.todos','todo_list'],
    'update':['TodoState.start_edit','TodoState.update_todo','TodoRepository.edit','TodoRepository.edit','TodoRepository.edit','TodoState.load_todos','todo_list'],
    'completed':['TodoState.toggle_complete','TodoRepository.set_completed','concept:update','TodoRepository.set_completed','TodoRepository.set_completed','TodoState.load_todos','todo_item'],
    'delete':['TodoState.ask_delete','TodoState.delete_todo','TodoRepository.delete','TodoRepository.delete','TodoRepository.delete','TodoState.load_todos','todo_list'],
    'init':['TodoRepository.__init__','get_engine','get_engine','TodoRepository.initialize','init_database','concept:SQLModel.metadata.create_all','init_database']}
    flows={}
    for key,(label,slide,entry,capture) in flow_specs.items():
        d=byid[slide];steps=[]
        for i,(sender,receiver,text,to,result) in enumerate(d['rows']):
            target=overrides[key][i]
            steps.append(dict(sender=sender,receiver=receiver,label=text,target=target,result=result))
        flows[key]=dict(label=label,title=d['title'].replace('Diagrama · ',''),note=d['note'],entry=entry,steps=steps,lanes=[dict(label=n,target=destination.get(t,'TodoState')) for n,t in d['lanes']],capture=capture)
    screenshots={p.stem:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (ROOT/'docs/guia_assets').glob('*.png')}
    data=dict(generated=datetime.now(ZoneInfo('Europe/Madrid')).strftime('%d/%m/%Y %H:%M'),files=rendered,symbols=symbols,flows=flows,screenshots=screenshots)
    # Keep the HTML script context safe, even if future Python comments contain closing tags.
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template=TEMPLATE.read_text();assert template.count('/*__GUIDE_DATA__*/')==1
    OUTPUT.parent.mkdir(exist_ok=True);OUTPUT.write_text(template.replace('/*__GUIDE_DATA__*/',payload),encoding='utf-8')
    print(f'Guía generada: {OUTPUT}\n{len(files)} archivos, {sum(s["kind"]!="concept" for s in symbols.values())} símbolos y {len(flows)} recorridos.')
    return data

if __name__=='__main__':build()
