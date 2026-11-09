"""o10 · Laboratorio de gráficas XY vinculadas mediante estado compartido.

Referencia: https://reflex.dev/docs/getting-started/linked-charts-tutorial/
Recorrido: source_data → on_select_end → selected_ids → visible_rows → revenue_data.
El origen es fijo: nunca ordenes RECORDS sin actualizar la correspondencia índice/ID.
"""
import json
from typing import Any, TypedDict
import reflex as rx
import reflex_xy as rxy
import xy
from .selector_pedidos import OrderSelector


class Order(TypedDict):
    id: str
    city: str
    hour: float
    units: int
    revenue: float


class SourceColumns(TypedDict):
    hour: list[float]
    units: list[int]
    revenue: list[float]


class RevenueColumns(TypedDict):
    order: list[str]
    revenue: list[float]


# 1. Pequeño conjunto ficticio y estable para jugar sin cargar archivos.
RECORDS: list[Order] = [
    {'id':'pedido-a','city':'Madrid','hour':8.0,'units':2,'revenue':120.0},
    {'id':'pedido-b','city':'Barcelona','hour':9.0,'units':3,'revenue':180.0},
    {'id':'pedido-c','city':'Valencia','hour':10.0,'units':8,'revenue':450.0},
    {'id':'pedido-d','city':'Sevilla','hour':11.0,'units':5,'revenue':260.0},
    {'id':'pedido-e','city':'Bilbao','hour':12.0,'units':10,'revenue':620.0},
    {'id':'pedido-f','city':'Zaragoza','hour':13.0,'units':4,'revenue':210.0},
    {'id':'pedido-g','city':'Málaga','hour':14.0,'units':12,'revenue':780.0},
    {'id':'pedido-h','city':'Vigo','hour':15.0,'units':6,'revenue':340.0},
    {'id':'pedido-i','city':'Murcia','hour':16.0,'units':9,'revenue':540.0},
    {'id':'pedido-j','city':'Toledo','hour':17.0,'units':3,'revenue':160.0},
    {'id':'pedido-k','city':'Palma','hour':18.0,'units':7,'revenue':410.0},
    {'id':'pedido-l','city':'Granada','hour':19.0,'units':11,'revenue':690.0},
]


def selection_ids(event: dict) -> list[str] | None:
    """2. Validar el evento y traducir posiciones canónicas a IDs de aplicación.

    None significa filtro eliminado; [] significa selección válida sin resultados.
    Un evento inválido provoca ValueError: el handler conserva el filtro anterior.
    """
    if event.get('type') != 'select_end' or event.get('version') != 1:
        raise ValueError('Evento de selección no reconocido.')
    selection = event.get('selection')
    if not isinstance(selection, dict):
        raise ValueError('El evento no contiene una selección válida.')
    if selection.get('cleared') is True or selection.get('kind') == 'clear':
        return None
    if selection.get('kind') not in ('box','lasso'):
        raise ValueError('Selecciona mediante rectángulo o lazo.')
    count = selection.get('total_count')
    if type(count) is not int or count < 0:
        raise ValueError('El recuento de selección no es válido.')
    if count == 0:
        return []
    if selection.get('truncated'):
        # No usar solo el fragmento del evento: resolver la selección completa en servidor.
        resolved = rxy.resolve_selection(event)
        if resolved is None:
            raise ValueError('La selección ya no se puede resolver. Selecciona otra vez.')
        rows = resolved.rows()
    else:
        rows = selection.get('rows')
    if not isinstance(rows,list):
        raise ValueError('Faltan las posiciones de los puntos seleccionados.')
    ids: list[str] = []
    for row in rows:
        if not isinstance(row,dict) or type(row.get('trace')) is not int or row['trace'] != 0:
            raise ValueError('La selección no corresponde a la traza de origen.')
        index = row.get('index')
        if type(index) is not int or not 0 <= index < len(RECORDS):
            raise ValueError('El índice del punto no corresponde a un pedido.')
        record_id = RECORDS[index]['id']
        if record_id not in ids:
            ids.append(record_id)
    if len(ids) != count:
        raise ValueError('La selección está incompleta. Vuelve a seleccionar.')
    return ids


class LinkedChartsState(rx.State):
    # 3. Única fuente de verdad para el filtro. Cada sesión tiene su propio estado.
    selected_ids: list[str] | None = None
    generation: int = 0
    status: str = 'Sin filtro: se muestran los 12 pedidos.'
    event_json: str = 'Selecciona puntos para inspeccionar el evento.'
    error: str = ''

    @rxy.data(cache=False)
    def source_data(self) -> SourceColumns:
        # La dispersión siempre recibe el conjunto completo; no se filtra a sí misma.
        return {'hour':[r['hour'] for r in RECORDS],
                'units':[r['units'] for r in RECORDS],
                'revenue':[r['revenue'] for r in RECORDS]}

    @rx.var
    def visible_rows(self) -> list[Order]:
        if self.selected_ids is None:
            return list(RECORDS)
        return [row for row in RECORDS if row['id'] in self.selected_ids]

    @rxy.data(cache=False)
    def revenue_data(self) -> RevenueColumns:
        # 4. El gráfico vinculado usa exactamente las mismas filas que la tabla.
        return {'order':[r['id'] for r in self.visible_rows],
                'revenue':[r['revenue'] for r in self.visible_rows]}

    @rx.var
    def visible_count(self) -> int:
        return len(self.visible_rows)

    @rx.var
    def total_revenue(self) -> str:
        return f'{sum(r["revenue"] for r in self.visible_rows):.2f} €'

    @rx.var
    def selection_label(self) -> str:
        return 'Sin filtro (None)' if self.selected_ids is None else f'{len(self.selected_ids)} IDs seleccionados'

    @rx.event
    def select_points(self, event: dict[str, Any]):
        # 5. Solo se procesa el evento de selección terminada, no cada hover.
        self.event_json = json.dumps(event,ensure_ascii=False,indent=2)[:12000]
        try:
            chosen = selection_ids(event)
        except ValueError as exc:
            self.error = str(exc)
            return
        self.selected_ids = chosen
        self.error = ''
        self.status = ('Selección borrada: vuelven todos los pedidos.' if chosen is None
                       else f'Selección XY aplicada: {len(chosen)} pedidos.')

    @rx.event
    def select_compatible(self, ids: list[str]):
        """Misma lógica vinculada; IDs recibidos por el canal estándar de Reflex."""
        valid = {r['id'] for r in RECORDS}
        if any(not isinstance(value, str) or value not in valid for value in ids):
            self.error = 'La selección contiene un pedido desconocido.'
            return
        self.selected_ids = list(dict.fromkeys(ids))
        self.error = ''
        self.status = f'Selección compatible aplicada: {len(self.selected_ids)} pedidos.'
        self.event_json = json.dumps({'origen': 'selector SVG compatible', 'ids': self.selected_ids}, ensure_ascii=False, indent=2)

    @rx.event
    def reset_selection(self):
        self.selected_ids = None
        self.generation += 1  # Remontar la dispersión borra el resaltado y reinicia su zoom.
        self.error = ''
        self.status = 'Sin filtro: se muestran los 12 pedidos.'
        self.event_json = 'Reinicio manual: no se ha recibido un evento XY.'

    @rx.event
    def try_first_two(self):
        # Control didáctico alternativo para verificar State incluso sin dibujar selección.
        self.selected_ids = [r['id'] for r in RECORDS[:2]]
        self.generation += 1
        self.error = ''
        self.status = 'Prueba manual: primeros dos pedidos (120 € + 180 €).'
        self.event_json = 'Selección desde un botón: no es un evento XY.'

    @rx.event
    def try_empty(self):
        self.selected_ids = []
        self.generation += 1
        self.error = ''
        self.status = 'Prueba manual: selección vacía, ningún pedido.'
        self.event_json = 'Prueba de []: distinto de None; no es un evento XY.'


def card(title: str, explanation: str, *children):
    return rx.box(rx.heading(title,size='5'),
        rx.text(explanation,size='2',color='#475569',margin_top='10px',margin_bottom='20px'),
        *children,padding=['18px','26px'],background_color='white',color='#0f172a',
        border='1px solid #e2e8f0',border_radius='18px',width='100%',min_width='0')


def linked_charts_010():
    return rx.box(rx.vstack(
        rx.flex(rx.box(rx.badge('o10 · LABORATORIO XY',color_scheme='indigo'),
                      rx.heading('Gráficos vinculados',size='8',margin_top='12px'),
                      rx.text('Una selección, varias vistas. Experimenta con estado compartido en Python.',color='#cbd5e1',margin_top='12px')),
                rx.link('← Inicio',href='/',color='#c7d2fe'),justify='between',flex_wrap='wrap',gap='20px',
                background_color='#0f172a',color='white',padding='30px',border_radius='20px',width='100%'),
        rx.callout('Empieza arrastrando un rectángulo sobre los dos puntos de la esquina inferior izquierda: deben aparecer pedido-a y pedido-b. En el modo compatible también puedes pulsar los puntos o usar Tab y Enter. XY queda disponible en su pestaña.'),
        rx.flex(rx.button('Restablecer todos',on_click=LinkedChartsState.reset_selection),
                rx.button('Probar primeros 2',on_click=LinkedChartsState.try_first_two,variant='soft'),
                rx.button('Probar selección vacía',on_click=LinkedChartsState.try_empty,variant='outline'),
                gap='12px',flex_wrap='wrap'),
        rx.grid(*[rx.box(rx.text(label,size='2',color='#64748b'),rx.heading(value,size='6',margin_top='10px'),
                        padding='20px',background_color='white',border_radius='14px')
                  for label,value in [('Pedidos visibles',LinkedChartsState.visible_count),
                                      ('Ingresos visibles',LinkedChartsState.total_revenue),
                                      ('Estado del filtro',LinkedChartsState.selection_label)]],
                columns=rx.breakpoints(initial='1',md='3'),gap='14px',width='100%'),
        rx.text(LinkedChartsState.status,size='2',role='status'),
        rx.cond(LinkedChartsState.error!='',rx.callout(LinkedChartsState.error,color_scheme='red',role='alert')),
        rx.tabs.root(
            rx.tabs.list(rx.tabs.trigger('Compatible · Seleccionar pedidos',value='compatible'),
                         rx.tabs.trigger('XY · Tutorial original',value='xy')),
            rx.tabs.content(compatible_charts(),value='compatible',padding_top='20px'),
            rx.tabs.content(
        rx.grid(
            card('1 · Selecciona pedidos (XY)', 
                 'X: hora del pedido. Y: unidades. La dispersión conserva los 12 puntos. Al terminar la selección, on_select_end envía sus posiciones a Python.',
                 rxy.scatter_chart(data=LinkedChartsState.source_data,x='hour',y='units',
                     size=10,color='#6366f1',
                     x_axis=xy.x_axis(label='Hora del pedido'),y_axis=xy.y_axis(label='Unidades'),
                     select=True,default_drag_action='select',
                     on_select_end=LinkedChartsState.select_points,
                     key=LinkedChartsState.generation.to_string(),width='100%',height='340px')),
            card('2 · Ingresos vinculados (XY)',
                 'Las barras se reconstruyen desde visible_rows. Seleccionar en la dispersión cambia los pedidos que aparecen aquí.',
                 rx.cond(LinkedChartsState.visible_count>0,
                     rxy.bar_chart(data=LinkedChartsState.revenue_data,x='order',y='revenue',color='#10b981',
                         x_axis=xy.x_axis(label='Pedido'),y_axis=xy.y_axis(label='Ingresos (€)'),
                         width='100%',height='340px'),
                     rx.callout('Selección sin pedidos: no hay barras que representar.'))),
            columns=rx.breakpoints(initial='1',lg='2'),gap='20px',width='100%'),
            value='xy',padding_top='20px'),
            default_value='compatible',width='100%'),
        card('3 · Tabla vinculada',
             'La tabla y las barras usan visible_rows. Se guardan IDs de aplicación; los índices que devuelve XY se traducen con RECORDS.',
             rx.cond(LinkedChartsState.visible_count>0,
                 rx.box(rx.table.root(
                     rx.table.header(rx.table.row(*[rx.table.column_header_cell(h) for h in ['Pedido','Ciudad','Hora','Unidades','Ingresos (€)']])),
                     rx.table.body(rx.foreach(LinkedChartsState.visible_rows,lambda row:rx.table.row(
                         rx.table.cell(row['id']),rx.table.cell(row['city']),rx.table.cell(row['hour']),
                         rx.table.cell(row['units']),rx.table.cell(row['revenue'])))),width='100%'),overflow_x='auto'),
                 rx.callout('No hay resultados. [] significa ningún pedido; Restablecer vuelve a None, que significa todos.'))),
        card('4 · Sigue el recorrido del código',
             'Archivo: Ejercicio991Reflex/o10_graficos_vinculados.py. Los comentarios 1–5 señalan las piezas del ejemplo.',
             rx.ordered_list(
                 rx.list.item('RECORDS: datos ficticios fijos; cada fila tiene un ID estable.'),
                 rx.list.item('Modo compatible: OrderSelector dibuja SVG y envía IDs a select_compatible; XY usa source_data y @rxy.data.'),
                 rx.list.item('select_points: valida el evento y actualiza selected_ids.'),
                 rx.list.item('visible_rows: calcula qué pedidos cumplen la selección.'),
                 rx.list.item('revenue_data y la tabla: leen esas mismas filas.'),gap='10px'),
             rx.accordion.root(rx.accordion.item(header='Inspeccionar el último evento',value='event',
                 content=rx.code_block(LinkedChartsState.event_json,language='json',width='100%',overflow_x='auto')),
                 collapsible=True,width='100%',margin_top='18px')),
        card('5 · Retos para jugar',
             'Modifica el módulo, guarda y comprueba los cambios en modo desarrollo.',
             rx.unordered_list(
                 rx.list.item('Cambia el importe de pedido-a y comprueba su barra y el total.'),
                 rx.list.item('Selecciona un rectángulo sin puntos: deben desaparecer filas y barras.'),
                 rx.list.item('Compara Probar primeros 2 con una selección real de los dos primeros puntos.'),
                 rx.list.item('Añade una fila a RECORDS, manteniendo el orden e ID de las existentes; ajusta el texto de 12 pedidos.'),
                 rx.list.item('No confundas filtrar registros con link_group/link_axes: esos parámetros sincronizan el zoom de ejes compatibles.'),gap='10px'),
             rx.callout('Si XY no dibuja, prueba los botones: si cambian indicadores y tabla, el estado funciona y habrá que revisar el canal/renderizador XY. Esta página conserva XY para estudiar el tutorial.',margin_top='18px'),
             rx.link('Tutorial oficial de Reflex ↗',href='https://reflex.dev/docs/getting-started/linked-charts-tutorial/',is_external=True,margin_top='16px')),
        align='stretch',gap='22px',max_width='1350px',margin='0 auto'),
        background_color='#f1f5f9',min_height='100vh',padding=['16px','32px'])



def compatible_charts():
    """Vista funcional sin el canal binario XY; comparte filtro, métricas y tabla."""
    return rx.grid(
        card('1 · Selecciona pedidos',
             'Arrastra un rectángulo desde un espacio vacío para seleccionar puntos. Un clic selecciona un pedido; los siguientes clics añaden o quitan pedidos. También admite Tab y Enter.',
             OrderSelector.create(data=RECORDS,selected=LinkedChartsState.selected_ids,
                 on_pick=LinkedChartsState.select_compatible,
                 key=LinkedChartsState.generation.to_string())),
        card('2 · Ingresos vinculados',
             'Estas barras Recharts leen exactamente las mismas filas que la tabla y los indicadores.',
             rx.cond(LinkedChartsState.visible_count>0,
                 rx.recharts.bar_chart(
                     rx.recharts.cartesian_grid(stroke_dasharray='3 3',vertical=False),
                     rx.recharts.x_axis(data_key='id'),rx.recharts.y_axis(),rx.recharts.tooltip(),
                     rx.recharts.bar(data_key='revenue',name='Ingresos (€)',fill='#10b981'),
                     data=LinkedChartsState.visible_rows,width='100%',height=320),
                 rx.callout('Selección sin pedidos. Pulsa Restablecer para recuperar todos.'))),
        columns=rx.breakpoints(initial='1',lg='2'),gap='20px',width='100%',
    )
