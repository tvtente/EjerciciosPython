"""o03 · Panel de clientes: dataclass → State → formulario → tabla → gráfica.

Adaptación didáctica del Dashboard Tutorial de Reflex. Datos ficticios por sesión.
https://reflex.dev/docs/getting-started/dashboard-tutorial/
"""
from collections import Counter
from dataclasses import dataclass, replace
import re
import reflex as rx

GENEROS = ['Mujer', 'Hombre', 'Prefiero no indicar']
CIUDADES = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Zaragoza']


# 1. Cada fila es un objeto con campos tipados, no una lista de posiciones.
@dataclass
class Cliente:
    id: int
    nombre: str
    email: str
    genero: str
    ciudad: str


def clientes_ejemplo() -> list[Cliente]:
    return [
        Cliente(1,'Lucía García','lucia@example.com','Mujer','Madrid'),
        Cliente(2,'Pablo Martín','pablo@example.com','Hombre','Barcelona'),
        Cliente(3,'Elena Ruiz','elena@example.com','Mujer','Valencia'),
        Cliente(4,'Alex López','alex@example.com','Prefiero no indicar','Sevilla'),
        Cliente(5,'Javier Torres','javier@example.com','Hombre','Madrid'),
        Cliente(6,'Nuria Sánchez','nuria@example.com','Mujer','Bilbao'),
    ]


# 2. Estado: los eventos modifican clientes; las propiedades calculadas actualizan las vistas.
class PanelControlState(rx.State):
    clientes: list[Cliente] = clientes_ejemplo()
    siguiente_id: int = 7
    busqueda: str = ''
    filtro_genero: str = 'Todos'
    dialogo_abierto: bool = False
    editando_id: int = 0
    formulario_version: int = 0
    nombre_inicial: str = ''
    email_inicial: str = ''
    genero_inicial: str = 'Prefiero no indicar'
    ciudad_inicial: str = 'Madrid'
    error: str = ''
    borrar_id: int = 0
    borrar_nombre: str = ''
    confirmar_borrado: bool = False

    @rx.var
    def clientes_visibles(self) -> list[Cliente]:
        texto = self.busqueda.strip().casefold()
        return sorted([cliente for cliente in self.clientes
                       if (not texto or texto in f'{cliente.nombre} {cliente.email} {cliente.ciudad}'.casefold())
                       and (self.filtro_genero == 'Todos' or cliente.genero == self.filtro_genero)],
                      key=lambda cliente: cliente.nombre.casefold())

    @rx.var
    def total(self) -> int:
        return len(self.clientes)

    @rx.var
    def visibles(self) -> int:
        return len(self.clientes_visibles)

    @rx.var
    def ciudades_visibles(self) -> int:
        return len({cliente.ciudad for cliente in self.clientes_visibles})

    @rx.var
    def users_for_graph(self) -> list[dict[str, str | int]]:
        # 3. Counter transforma los mismos clientes de la tabla en puntos de la gráfica.
        # A diferencia del tutorial, @rx.var evita tener que refrescar la gráfica a mano.
        counts = Counter(cliente.genero for cliente in self.clientes_visibles)
        return [{'name':genero,'value':counts[genero]} for genero in GENEROS]

    @rx.var
    def ciudades_para_grafica(self) -> list[dict[str, str | int]]:
        counts = Counter(cliente.ciudad for cliente in self.clientes_visibles)
        return [{'name':ciudad,'value':counts[ciudad]} for ciudad in CIUDADES]

    @rx.event
    def buscar(self, texto: str):
        self.busqueda = texto

    @rx.event
    def filtrar_genero(self, genero: str):
        if genero in ['Todos', *GENEROS]:
            self.filtro_genero = genero

    @rx.event
    def limpiar_filtros(self):
        self.busqueda = ''
        self.filtro_genero = 'Todos'

    @rx.event
    def cambiar_dialogo(self, abierto: bool):
        self.dialogo_abierto = abierto

    @rx.event
    def nuevo_cliente(self):
        self.editando_id = 0
        self.nombre_inicial = ''
        self.email_inicial = ''
        self.genero_inicial = 'Prefiero no indicar'
        self.ciudad_inicial = 'Madrid'
        self.error = ''
        self.formulario_version += 1
        self.dialogo_abierto = True

    @rx.event
    def editar_cliente(self, cliente_id: int):
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        if cliente is None:
            return
        self.editando_id = cliente.id
        self.nombre_inicial, self.email_inicial = cliente.nombre, cliente.email
        self.genero_inicial, self.ciudad_inicial = cliente.genero, cliente.ciudad
        self.error = ''
        self.formulario_version += 1
        self.dialogo_abierto = True

    @rx.event
    def guardar_cliente(self, datos: dict):
        # 4. Los atributos name de los controles son las claves de este diccionario.
        nombre = str(datos.get('nombre','')).strip()
        email = str(datos.get('email','')).strip().lower()
        genero = str(datos.get('genero',''))
        ciudad = str(datos.get('ciudad',''))
        if not 2 <= len(nombre) <= 80:
            self.error = 'El nombre debe tener entre 2 y 80 caracteres.'
            return
        if len(email)>254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            self.error = 'Introduce un correo electrónico válido.'
            return
        if genero not in GENEROS or ciudad not in CIUDADES:
            self.error = 'Selecciona un género y una ciudad de la lista.'
            return
        if any(c.email.casefold() == email.casefold() and c.id != self.editando_id for c in self.clientes):
            self.error = 'Ya existe un cliente con ese correo.'
            return
        if self.editando_id:
            self.clientes = [replace(c,nombre=nombre,email=email,genero=genero,ciudad=ciudad)
                             if c.id == self.editando_id else c for c in self.clientes]
        else:
            self.clientes = [*self.clientes,Cliente(self.siguiente_id,nombre,email,genero,ciudad)]
            self.siguiente_id += 1
        self.error = ''
        self.dialogo_abierto = False  # Solo cerrar tras validar y guardar.
        return rx.toast.success('Cliente guardado. Tabla y gráficas actualizadas.')

    @rx.event
    def pedir_borrado(self, cliente_id: int):
        cliente = next((c for c in self.clientes if c.id == cliente_id),None)
        if cliente:
            self.borrar_id, self.borrar_nombre = cliente.id, cliente.nombre
            self.confirmar_borrado = True

    @rx.event
    def cambiar_confirmacion(self, abierto: bool):
        self.confirmar_borrado = abierto

    @rx.event
    def eliminar_cliente(self):
        if not self.confirmar_borrado:
            return
        self.clientes = [c for c in self.clientes if c.id != self.borrar_id]
        self.confirmar_borrado = False
        self.borrar_id = 0
        self.borrar_nombre = ''
        return rx.toast.info('Cliente eliminado de esta sesión.')

    @rx.event
    def restaurar_ejemplos(self):
        self.clientes = clientes_ejemplo()
        self.siguiente_id = 7
        self.limpiar_filtros()
        self.dialogo_abierto = False
        self.confirmar_borrado = False
        self.error = ''
        return rx.toast.info('Ejemplos restaurados.')


# 5. Componentes reutilizables: formulario modal, fila, tabla y gráficas.
def formulario_cliente():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(rx.cond(PanelControlState.editando_id == 0,'Añadir cliente','Editar cliente')),
            rx.dialog.description('Completa los datos. Este ejemplo no envía correos ni guarda información en una base de datos.'),
            rx.form(
                rx.vstack(
                    rx.text('Nombre',weight='bold',size='2'),
                    rx.input(name='nombre',default_value=PanelControlState.nombre_inicial,required=True,
                             min_length=2,max_length=80,placeholder='Nombre y apellidos',aria_label='Nombre'),
                    rx.text('Correo electrónico',weight='bold',size='2'),
                    rx.input(name='email',type='email',default_value=PanelControlState.email_inicial,
                             required=True,max_length=254,placeholder='nombre@example.com',aria_label='Correo electrónico'),
                    rx.text('Género',weight='bold',size='2'),
                    rx.select(GENEROS,name='genero',default_value=PanelControlState.genero_inicial,aria_label='Género'),
                    rx.text('Ciudad',weight='bold',size='2'),
                    rx.select(CIUDADES,name='ciudad',default_value=PanelControlState.ciudad_inicial,aria_label='Ciudad'),
                    rx.cond(PanelControlState.error!='',rx.callout(PanelControlState.error,color_scheme='red',role='alert')),
                    rx.flex(rx.dialog.close(rx.button('Cancelar',type='button',variant='soft',color_scheme='gray')),
                            rx.button('Guardar cliente',type='submit'),justify='end',gap='12px',margin_top='12px'),
                    align='stretch',gap='10px',margin_top='20px'),
                key=PanelControlState.formulario_version.to_string(),on_submit=PanelControlState.guardar_cliente,
                reset_on_submit=False),max_width='470px'),
        open=PanelControlState.dialogo_abierto,on_open_change=PanelControlState.cambiar_dialogo)


def fila_cliente(cliente: rx.Var[Cliente]):
    return rx.table.row(
        rx.table.cell(rx.text(cliente.nombre,weight='medium')),
        rx.table.cell(cliente.email),
        rx.table.cell(rx.badge(cliente.genero,variant='soft',color_scheme='indigo')),
        rx.table.cell(cliente.ciudad),
        rx.table.cell(rx.flex(
            rx.button(rx.icon('pencil',size=15),'Editar',variant='soft',size='1',on_click=PanelControlState.editar_cliente(cliente.id)),
            rx.button(rx.icon('trash-2',size=15),'Borrar',variant='soft',color_scheme='red',size='1',
                      on_click=PanelControlState.pedir_borrado(cliente.id)),gap='8px',flex_wrap='wrap')))


def panel(titulo: str, descripcion: str, *contenido):
    return rx.box(rx.heading(titulo,size='5'),rx.text(descripcion,size='2',color='#475569',margin_top='8px',margin_bottom='20px'),
                  *contenido,padding=['20px','28px'],background_color='white',color='#0f172a',
                  border='1px solid #e2e8f0',border_radius='18px',width='100%',min_width='0')


def grafica(data, color: str):
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(stroke_dasharray='3 3',vertical=False),
        rx.recharts.x_axis(data_key='name',tick={'fontSize':11},interval=0),
        rx.recharts.y_axis(allow_decimals=False),rx.recharts.tooltip(),
        rx.recharts.bar(data_key='value',name='Clientes',fill=color),data=data,width='100%',height=290)


def panel_control_03():
    return rx.box(rx.vstack(
        rx.flex(rx.box(rx.badge('o03 · PANEL DE CONTROL',color_scheme='indigo'),
                rx.heading('Tus clientes, de un vistazo',size='8',margin_top='12px'),
                rx.text('Un formulario, un estado y varias vistas que se actualizan juntas.',color='#cbd5e1',margin_top='12px')),
                rx.link('← Inicio',href='/',color='#c7d2fe'),justify='between',flex_wrap='wrap',gap='20px',
                background_color='#0f172a',color='white',padding='30px',border_radius='20px',width='100%'),
        rx.callout('Laboratorio con clientes ficticios por sesión. No hay base de datos: usa datos de prueba. Restaurar ejemplos reemplaza los registros actuales.'),
        rx.grid(*[rx.box(rx.text(etiqueta,size='2',color='#475569'),rx.heading(valor,size='8',margin_top='10px'),
                        padding='24px',background_color='white',border='1px solid #e2e8f0',border_radius='16px')
                  for etiqueta,valor in [('Clientes registrados',PanelControlState.total),('Clientes visibles',PanelControlState.visibles),
                                         ('Ciudades en la selección',PanelControlState.ciudades_visibles)]],
                columns=rx.breakpoints(initial='1',sm='3'),gap='16px',width='100%'),
        panel('1 · Directorio de clientes','Busca por nombre, correo o ciudad. La tabla y las gráficas usan la misma selección.',
            rx.flex(rx.input(placeholder='Buscar cliente…',aria_label='Buscar cliente',value=PanelControlState.busqueda,
                             on_change=PanelControlState.buscar,flex='1',min_width='180px'),
                    rx.select(['Todos',*GENEROS],value=PanelControlState.filtro_genero,on_change=PanelControlState.filtrar_genero,aria_label='Filtrar género'),
                    rx.button('Limpiar filtros',variant='soft',on_click=PanelControlState.limpiar_filtros),
                    rx.button(rx.icon('plus',size=17),'Añadir cliente',on_click=PanelControlState.nuevo_cliente),
                    gap='12px',flex_wrap='wrap',margin_bottom='20px'),
            rx.cond(PanelControlState.visibles>0,
                rx.box(rx.table.root(
                    rx.table.header(rx.table.row(*[rx.table.column_header_cell(t) for t in ['Nombre','Correo','Género','Ciudad','Acciones']])),
                    rx.table.body(rx.foreach(PanelControlState.clientes_visibles,fila_cliente)),width='100%'),overflow_x='auto'),
                rx.callout('No hay clientes con estos filtros. Limpia la búsqueda o añade un cliente.')),
            rx.flex(rx.text(PanelControlState.visibles,' de ',PanelControlState.total,' clientes',size='2',color='#475569'),
                    rx.button('Restaurar ejemplos',variant='ghost',on_click=PanelControlState.restaurar_ejemplos),
                    justify='between',flex_wrap='wrap',gap='12px',margin_top='20px')),
        rx.grid(
            panel('2 · Distribución por género','Counter cuenta los clientes visibles. @rx.var recalcula las barras al añadir, editar, borrar o filtrar.',
                  rx.cond(PanelControlState.visibles>0,grafica(PanelControlState.users_for_graph,'#6366f1'),rx.text('Sin datos para representar.'))),
            panel('3 · Clientes por ciudad','Una segunda vista del mismo estado: no necesitas mantener otra lista de clientes.',
                  rx.cond(PanelControlState.visibles>0,grafica(PanelControlState.ciudades_para_grafica,'#10b981'),rx.text('Sin datos para representar.'))),
            columns=rx.breakpoints(initial='1',lg='2'),gap='20px',width='100%'),
        panel('4 · Prueba y sigue el código','Archivo o03_panel_control.py: los comentarios numerados identifican las piezas del tutorial.',
            rx.ordered_list(
                rx.list.item('Cliente: dataclass que describe cada fila.'),
                rx.list.item('PanelControlState: lista de clientes y eventos de usuario.'),
                rx.list.item('users_for_graph: Counter transforma clientes en una lista de diccionarios.'),
                rx.list.item('guardar_cliente: recibe el formulario, valida y cierra el diálogo solo al guardar.'),
                rx.list.item('rx.foreach y Recharts: presentan las mismas filas sin recargar la página.'),gap='10px'),
            rx.text('Reto: añade un cliente de Zaragoza, busca su nombre, edita su ciudad y bórralo. Observa cómo cambia cada gráfica.',weight='bold',margin_top='18px'),
            rx.link('Dashboard Tutorial de Reflex ↗',href='https://reflex.dev/docs/getting-started/dashboard-tutorial/',is_external=True,margin_top='16px')),
        formulario_cliente(),
        rx.alert_dialog.root(rx.alert_dialog.content(
            rx.alert_dialog.title('¿Borrar este cliente?'),
            rx.alert_dialog.description('Se eliminará de esta sesión: ',PanelControlState.borrar_nombre),
            rx.flex(rx.alert_dialog.cancel(rx.button('Cancelar',variant='soft',color_scheme='gray')),
                    rx.alert_dialog.action(rx.button('Sí, borrar',color_scheme='red',on_click=PanelControlState.eliminar_cliente)),
                    justify='end',gap='12px',margin_top='20px')),
            open=PanelControlState.confirmar_borrado,on_open_change=PanelControlState.cambiar_confirmacion),
        align='stretch',gap='22px',max_width='1280px',margin='0 auto'),
        background_color='#f1f5f9',color='#0f172a',min_height='100vh',padding=['16px','32px'])
