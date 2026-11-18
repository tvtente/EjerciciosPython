"""Superstore interactivo: notebook → filtros de State → agregaciones → Recharts."""
import asyncio
import math
from typing import Any
import pandas as pd
import reflex as rx
from .superstore_analysis import load_superstore, filtrar_superstore

CATEGORIES = {
    'region': 'Regiones', 'country': 'Países', 'state': 'Comunidades autónomas', 'city': 'Ciudades',
    'segment': 'Segmentos', 'ship_mode': 'Modos de envío', 'category': 'Categorías',
    'sub-category': 'Subcategorías',
    'year': 'Años', 'month': 'Meses (1–12)', 'weekday': 'Días (0=lunes, 6=domingo)',
}
TEXTS = {'customer_name': 'Cliente', 'product_name': 'Producto', 'customer_id': 'ID de cliente',
         'product_id': 'ID de producto', 'order_id': 'ID de pedido', 'postal_code': 'Código postal'}
RANGES = {'sales':'Ventas', 'profit':'Beneficio', 'quantity':'Cantidad', 'discount':'Descuento (0–1)'}
PAGE_SIZE = 25


def filter_config(fields: dict[str, str], selected: dict[str, list[str]]) -> dict:
    """Convierte los controles web al mismo diccionario del notebook (secciones filtros)."""
    config: dict[str, Any] = {'categorias': {}, 'textos': {}, 'rangos': {}, 'fechas': {}}
    for key in CATEGORIES:
        values = selected.get(key, [])
        if key in ('year', 'month', 'weekday'):
            config[{'year':'años','month':'meses','weekday':'dias'}[key]] = [int(v) for v in values]
        else:
            config['categorias'][key] = values
    config['textos'] = {key: fields.get(key, '') for key in TEXTS}
    for key in RANGES:
        lower, upper = fields.get(key+'_min', '').strip(), fields.get(key+'_max', '').strip()
        if not lower and not upper:
            continue
        lo, hi = float(lower) if lower else -math.inf, float(upper) if upper else math.inf
        if (lower and not math.isfinite(lo)) or (upper and not math.isfinite(hi)) or lo > hi:
            raise ValueError(f'Rango no válido para {RANGES[key]}.')
        config['rangos'][key] = (lo, hi)
    for key in ('order_date', 'ship_date'):
        start, end = fields.get(key+'_from',''), fields.get(key+'_to','')
        a = pd.to_datetime(start, format='%Y-%m-%d').date() if start else None
        b = pd.to_datetime(end, format='%Y-%m-%d').date() if end else None
        if a and b and a > b:
            raise ValueError('La fecha inicial no puede ser posterior a la final.')
        config['fechas'][key] = (a,b)
    config['rentabilidad'] = fields.get('rentabilidad', 'Todas')
    config.update({key: fields.get(key,'false') == 'true' for key in ('sin_descuento','limite_5000','quitar_duplicados')})
    return config


def train_exploratory(frame: pd.DataFrame) -> dict[str, Any]:
    """Modelo exploratorio, no pronóstico temporal; sin profit ni precio derivado como entrada."""
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    if len(frame) < 30 or frame['sales'].nunique() < 2:
        raise ValueError('El modelo necesita al menos 30 filas y ventas con distintos valores.')
    cats = ['category','sub-category','segment','region','ship_mode']
    nums = ['discount','quantity']
    x_train,x_test,y_train,y_test = train_test_split(frame[cats+nums], frame['sales'], test_size=.2, random_state=42)
    model=Pipeline([('prepare',ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),cats)],remainder='passthrough')),
                    ('forest',RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=1))])
    model.fit(x_train,y_train)
    pred=model.predict(x_test)
    # Las métricas se calculan con TODAS las filas reservadas para validación.
    mae = mean_absolute_error(y_test, pred)
    baseline_mae = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))
    r2 = r2_score(y_test, pred) if y_test.nunique() > 1 else None
    metrics = {'MAE': f'{mae:.2f} €',
               'RMSE': f'{math.sqrt(mean_squared_error(y_test,pred)):.2f} €',
               'R²': f'{r2:.3f}' if r2 is not None else 'No definido',
               'Entrenamiento': f'{len(y_train)} filas',
               'Validación': f'{len(y_test)} filas',
               'MAE de referencia': f'{baseline_mae:.2f} €'}
    # Comparamos contra una regla sencilla: predecir la media del entrenamiento.
    comparison = [
        {'modelo': 'Bosque aleatorio', 'mae': round(mae,2)},
        {'modelo': 'Media del entrenamiento', 'mae': round(baseline_mae,2)},
    ]
    evaluation = pd.DataFrame({'real': y_test.to_numpy(), 'predicha': pred})
    evaluation['error'] = evaluation['predicha'] - evaluation['real']
    points = evaluation.sample(n=min(500,len(evaluation)),random_state=42)
    low = float(min(evaluation.real.min(), evaluation.predicha.min(), 0))
    high = float(max(evaluation.real.max(), evaluation.predicha.max(), 1))
    # Correlación solo en entrenamiento. Profit NO es una entrada del modelo.
    correlation_frame = x_train[nums].copy()
    correlation_frame['sales'] = y_train
    corr = correlation_frame.corr(method='pearson')
    labels = {'discount':'Descuento', 'quantity':'Cantidad', 'sales':'Ventas'}
    heatmap = []
    for row in corr.index:
        for col in corr.columns:
            value = corr.loc[row,col]
            valid = pd.notna(value)
            # Azul: relación positiva; rojo: negativa; gris: no calculable.
            strength = abs(float(value)) if valid else 0
            target = (37,99,235) if valid and value >= 0 else (220,38,38)
            color = '#e2e8f0' if not valid else '#%02x%02x%02x' % tuple(round(255+(c-255)*strength) for c in target)
            heatmap.append({'row':labels[row], 'column':labels[col],
                            'label':f'{value:.2f}' if valid else 'N/D',
                            'background':color, 'foreground':'white' if strength>.6 else '#0f172a'})
    interpretation = ('El bosque tiene menor MAE que la referencia en esta validación.' if mae < baseline_mae
                      else 'El bosque no mejora el MAE de la referencia en esta validación.')
    return {'metrics': metrics, 'points': points.round(2).to_dict('records'),
            'diagonal': [{'real':low,'predicha':low},{'real':high,'predicha':high}],
            'comparison': comparison, 'heatmap': heatmap, 'interpretation':interpretation}



class SuperstoreState(rx.State):
    # Los DataFrames quedan en el backend: al navegador solo enviamos resúmenes y una página.
    _base: pd.DataFrame = pd.DataFrame()
    _filtered: pd.DataFrame = pd.DataFrame()
    fields: dict[str, str] = {'rentabilidad':'Todas','quitar_duplicados':'true'}
    selected: dict[str, list[str]] = {}
    options: dict[str, list[str]] = {}
    applied: dict[str, list[str]] = {}
    rows: list[dict[str, str]] = []
    monthly: list[dict[str, Any]] = []
    regions: list[dict[str, Any]] = []
    categories: list[dict[str, Any]] = []
    scatter: list[dict[str, float]] = []
    count: int = 0
    loaded_count: int = 0
    order_count: int = 0
    sales: str = '0.00'
    profit: str = '0.00'
    margin: str = '0.0 %'
    page: int = 1
    total_pages: int = 1
    loaded: bool = False
    error: str = ''
    pending: bool = False
    training: bool = False
    model_metrics: dict[str,str] = {}
    model_error: str = ''
    model_points: list[dict[str, float]] = []
    model_diagonal: list[dict[str, float]] = []
    model_comparison: list[dict[str, Any]] = []
    model_heatmap: list[dict[str, str]] = []
    model_interpretation: str = ''

    @rx.event
    def load_data(self):
        if self.loaded:
            return
        try:
            self._base = load_superstore()
            self.loaded_count=len(self._base)
            self.options={key: sorted(self._base[key].dropna().astype(str).unique().tolist())
                          for key in CATEGORIES if key not in ('year','month','weekday')}
            self.options.update({'year': sorted(self._base.order_date.dt.year.astype(str).unique().tolist()),
                                 'month': [str(i) for i in range(1,13)], 'weekday': [str(i) for i in range(7)]})
            self.loaded=True
            self.apply()
        except (OSError, ValueError, KeyError) as exc:
            self.error=f'No se pudo cargar data/superstore.csv: {exc}'

    @rx.event
    def reload_data(self):
        """Vuelve a leer el archivo después de regenerarlo y limpia selecciones antiguas."""
        if self.training:
            return
        self.loaded = False
        self.fields = {'rentabilidad': 'Todas', 'quitar_duplicados': 'true'}
        self.selected = {}
        self.load_data()

    @rx.event
    def set_field(self, key: str, value: str):
        self.fields={**self.fields,key:value}
        self.pending=True

    @rx.event
    def set_flag(self, key: str, value: bool):
        self.fields={**self.fields,key:'true' if value else 'false'}
        self.pending=True

    @rx.event
    def toggle_choice(self, key: str, value: str, checked: bool):
        values=list(self.selected.get(key,[]))
        if checked and value not in values:
            values.append(value)
        elif not checked and value in values:
            values.remove(value)
        self.selected={**self.selected,key:values}
        self.pending=True

    @rx.event
    def apply(self):
        if not self.loaded or self.training:
            return
        try:
            config=filter_config(self.fields,self.selected)
            filtered=filtrar_superstore(self._base,config)
        except (ValueError, TypeError) as exc:
            self.error=f'Revisa los filtros: {exc}'
            return
        self._filtered=filtered
        self.count=len(filtered)
        self.order_count=int(filtered.order_id.nunique())
        self.sales=f'{filtered.sales.sum():,.2f}'
        self.profit=f'{filtered.profit.sum():,.2f}'
        self.margin=f'{100*filtered.profit.sum()/filtered.sales.sum():.1f} %' if filtered.sales.sum() else '0.0 %'
        # Mismo groupby del notebook. Los totales incluyen todas las coincidencias.
        monthly=filtered.groupby(filtered.order_date.dt.to_period('M'))[['sales','profit']].sum().round(2).reset_index()
        monthly['month']=monthly.order_date.astype(str)
        self.monthly=monthly[['month','sales','profit']].to_dict('records')
        self.regions=filtered.groupby('region',as_index=False)[['sales','profit']].sum().round(2).to_dict('records')
        self.categories=filtered.groupby('category',as_index=False)[['sales','profit']].sum().round(2).to_dict('records')
        # Dispersión acotada para no enviar miles de puntos al navegador.
        points=filtered.sample(n=min(1500,len(filtered)),random_state=42)
        self.scatter=points[['discount','profit']].to_dict('records')
        self.applied={key:[str(v) for v in values] for key,values in self.selected.items() if values}
        self.applied.update({key:[value] for key,value in self.fields.items()
                             if value and value not in ('false','Todas')})
        self.page=1
        self.total_pages=max(1,math.ceil(self.count/PAGE_SIZE))
        self._show_page()
        self.pending=False
        self.error=''
        self.model_metrics={}
        self.model_points=[]
        self.model_diagonal=[]
        self.model_comparison=[]
        self.model_heatmap=[]
        self.model_interpretation='' 
        self.model_error=''

    def _show_page(self):
        columns=['order_id','order_date','customer_name','region','category','sales','profit','discount']
        view=self._filtered.iloc[(self.page-1)*PAGE_SIZE:self.page*PAGE_SIZE][columns].copy()
        view['order_date']=view.order_date.dt.strftime('%Y-%m-%d')
        for key in ['sales','profit']:
            view[key]=view[key].map(lambda x:f'{x:,.2f}')
        view['discount']=view.discount.map(lambda x:f'{100*x:.0f} %')
        self.rows=view.astype(str).to_dict('records')

    @rx.event
    def change_page(self, step: int):
        if not self.loaded:
            return
        self.page=max(1,min(self.total_pages,self.page+step))
        self._show_page()

    @rx.event
    def reset_filters(self):
        if self.training:
            return
        self.fields={'rentabilidad':'Todas','quitar_duplicados':'true'}
        self.selected={}
        self.apply()

    @rx.event
    def download(self):
        if self.loaded:
            return rx.download(data=self._filtered.to_csv(index=False),filename='superstore-filtrado.csv',mime_type='text/csv')

    @rx.event
    async def train(self):
        if self.training or not self.loaded:
            return
        if self.pending:
            self.model_error='Aplica los filtros pendientes antes de entrenar.'
            return
        self.training=True
        self.model_metrics={}
        self.model_points=[]
        self.model_diagonal=[]
        self.model_comparison=[]
        self.model_heatmap=[]
        self.model_interpretation='' 
        self.model_error=''
        yield
        try:
            result=await asyncio.to_thread(train_exploratory,self._filtered.copy())
            self.model_metrics=result['metrics']
            self.model_points=result['points']
            self.model_diagonal=result['diagonal']
            self.model_comparison=result['comparison']
            self.model_heatmap=result['heatmap']
            self.model_interpretation=result['interpretation']
        except (ValueError, ImportError) as exc:
            self.model_error=str(exc)
        finally:
            self.training=False


# Cada helper construye un control. Su valor vive en State y se conserva al restablecer.
def text_filter(key: str, label: str, kind: str='text'):
    return rx.vstack(rx.text(label,size='2',weight='medium'),
        rx.input(value=SuperstoreState.fields.get(key,''), on_change=lambda value: SuperstoreState.set_field(key,value),
                 type=kind, placeholder='Sin límite' if kind=='number' else 'Todos', width='100%',
                 disabled=SuperstoreState.training),align='stretch',gap='6px')


def category_filter(key: str, label: str):
    return rx.vstack(rx.text(label,size='2',weight='medium'),
        rx.scroll_area(rx.vstack(rx.foreach(SuperstoreState.options.get(key,[]),
            lambda value: rx.checkbox(value, checked=SuperstoreState.selected.get(key,[]).contains(value),
                on_change=lambda checked: SuperstoreState.toggle_choice(key,value,checked),
                disabled=SuperstoreState.training)),align='start',gap='8px',padding='8px'),
                height='145px',width='100%',type='auto'),
        rx.text('Sin selección = todos',size='1',color='#64748b'),
        padding='12px',border='1px solid #e2e8f0',border_radius='10px',width='100%')


def section(title: str, *children):
    return rx.box(rx.heading(title,size='5',margin_bottom='18px'),*children,
                  padding=['18px','26px'],background_color='white',border_radius='18px',
                  border='1px solid #e2e8f0',width='100%',min_width='0')


def chart_card(title, description, chart):
    return section(title,rx.text(description,size='2',color='#64748b',margin_bottom='16px'),chart)


def charts():
    return rx.grid(
        chart_card('Evolución mensual','Ventas y beneficio, agregados por mes. Importes en euros (EUR), sin impuestos adicionales.',
            rx.recharts.line_chart(rx.recharts.cartesian_grid(stroke_dasharray='3 3'),
                rx.recharts.x_axis(data_key='month'),rx.recharts.y_axis(),rx.recharts.tooltip(),rx.recharts.legend(),
                rx.recharts.line(data_key='sales',name='Ventas',stroke='#6366f1',dot=False,stroke_width=2),
                rx.recharts.line(data_key='profit',name='Beneficio',stroke='#10b981',dot=False,stroke_width=2),
                data=SuperstoreState.monthly,width='100%',height=300)),
        chart_card('Ventas por región','Comparación de ventas y beneficio: la misma agregación groupby del notebook.',
            rx.recharts.bar_chart(rx.recharts.x_axis(data_key='region'),rx.recharts.y_axis(),rx.recharts.tooltip(),rx.recharts.legend(),
                rx.recharts.bar(data_key='sales',name='Ventas',fill='#6366f1'),
                rx.recharts.bar(data_key='profit',name='Beneficio',fill='#10b981'),
                data=SuperstoreState.regions,width='100%',height=300)),
        chart_card('Beneficio por categoría','Las barras negativas representan pérdidas en la selección actual.',
            rx.recharts.bar_chart(rx.recharts.x_axis(data_key='category'),rx.recharts.y_axis(),rx.recharts.tooltip(),
                rx.recharts.reference_line(y=0,stroke='#64748b'),
                rx.recharts.bar(data_key='profit',name='Beneficio',fill='#10b981'),
                data=SuperstoreState.categories,width='100%',height=280)),
        chart_card('Descuento y beneficio','Muestra reproducible de hasta 1.500 filas. Los indicadores y otras gráficas incluyen toda la selección; correlación no implica causalidad.',
            rx.recharts.scatter_chart(
                rx.recharts.x_axis(data_key='discount',type_='number',name='Descuento',domain=[0,1]),
                rx.recharts.y_axis(data_key='profit',type_='number',name='Beneficio'),rx.recharts.tooltip(),
                rx.recharts.scatter(data=SuperstoreState.scatter,fill='#f59e0b',name='Operaciones'),
                width='100%',height=280)),
        columns=rx.breakpoints(initial='1',lg='2'),gap='20px',width='100%',
    )


def filters():
    return section('1 · Explora y combina filtros',
        rx.text('Se combinan con Y; dentro de cada lista se acepta cualquiera de los valores marcados. Cambia los controles y pulsa Aplicar.',size='2',color='#64748b',margin_bottom='16px'),
        rx.accordion.root(
            rx.accordion.item(header='Ubicación, productos y segmentos',content=rx.grid(
                *[category_filter(k,v) for k,v in CATEGORIES.items() if k not in ('year','month','weekday')],
                columns=rx.breakpoints(initial='1',sm='2',lg='4'),gap='12px'),value='categorias'),
            rx.accordion.item(header='Fechas y calendario',content=rx.vstack(
                rx.grid(*[text_filter(key+suffix,label+caption,'date')
                    for key,label in [('order_date','Pedido'),('ship_date','Envío')]
                    for suffix,caption in [('_from',' desde'),('_to',' hasta')]],
                    columns=rx.breakpoints(initial='1',sm='2',lg='4'),gap='12px',width='100%'),
                rx.grid(*[category_filter(k,CATEGORIES[k]) for k in ('year','month','weekday')],
                    columns=rx.breakpoints(initial='1',sm='3'),gap='12px',width='100%'),gap='16px',width='100%'),value='fechas'),
            rx.accordion.item(header='Importes y rentabilidad',content=rx.vstack(
                rx.grid(*[text_filter(key+suffix,label+caption,'number') for key,label in RANGES.items()
                    for suffix,caption in [('_min',' mínimo'),('_max',' máximo')]],
                    columns=rx.breakpoints(initial='1',sm='2',lg='4'),gap='12px',width='100%'),
                rx.select(['Todas','Con beneficio','Con pérdidas','Sin beneficio ni pérdida'],
                    value=SuperstoreState.fields.get('rentabilidad','Todas'),
                    on_change=lambda value: SuperstoreState.set_field('rentabilidad',value),disabled=SuperstoreState.training),
                *[rx.checkbox(label,checked=SuperstoreState.fields.get(key,'false')=='true',
                    on_change=lambda value,k=key: SuperstoreState.set_flag(k,value),disabled=SuperstoreState.training)
                  for key,label in [('sin_descuento','Solo operaciones sin descuento'),('limite_5000','Ventas inferiores a 5000'),('quitar_duplicados','Eliminar duplicados')]],
                align='stretch',gap='14px',width='100%'),value='importes'),
            rx.accordion.item(header='Buscar clientes, productos e identificadores',content=rx.grid(
                *[text_filter(k,v) for k,v in TEXTS.items()],columns=rx.breakpoints(initial='1',sm='2',lg='3'),gap='12px'),value='busqueda'),
            collapsible=True,width='100%',
        ),
        rx.flex(rx.button('Aplicar filtros',on_click=SuperstoreState.apply,disabled=SuperstoreState.training | ~SuperstoreState.loaded),
                rx.button('Recargar CSV',variant='outline',on_click=SuperstoreState.reload_data,disabled=SuperstoreState.training),
                rx.button('Restablecer',variant='soft',on_click=SuperstoreState.reset_filters,disabled=SuperstoreState.training),
                rx.cond(SuperstoreState.pending,rx.badge('Cambios sin aplicar',color_scheme='orange')),
                gap='12px',align='center',flex_wrap='wrap',margin_top='18px'),
        rx.cond(SuperstoreState.error!='',rx.callout(SuperstoreState.error,color_scheme='red',role='alert',margin_top='16px')),
    )


def superstore_index():
    return rx.box(rx.vstack(
        rx.flex(rx.box(rx.badge('DEL NOTEBOOK A LA WEB',color_scheme='indigo'),
                rx.heading('Superstore · Explora tus ventas',size='8',margin_top='12px'),
                rx.text('España · Datos ficticios reproducibles · Importes en euros (EUR).',color='#cbd5e1',margin_top='12px')),
                rx.link('← Volver al contador',href='/',color='#c7d2fe'),justify='between',flex_wrap='wrap',gap='18px',
                background_color='#0f172a',color='white',padding='30px',border_radius='20px',width='100%'),
        filters(),
        rx.grid(*[rx.box(rx.text(label,size='2',color='#64748b'),rx.heading(value,size='6',margin_top='10px'),
                    padding='22px',background_color='white',border='1px solid #e2e8f0',border_radius='16px')
                    for label,value in [('Líneas de venta',SuperstoreState.count),('Pedidos únicos',SuperstoreState.order_count),
                        ('Ventas (€)',SuperstoreState.sales),('Beneficio (€)',SuperstoreState.profit),('Margen global',SuperstoreState.margin)]],
                    columns=rx.breakpoints(initial='1',sm='2',lg='5'),gap='12px',width='100%'),
        rx.text('Los indicadores corresponden a los últimos filtros aplicados. El margen es beneficio / ventas; importes en EUR. Los datos son sintéticos y no representan actividad comercial real.',size='2',color='#64748b'),
        rx.cond(SuperstoreState.count>0,charts(),rx.callout('No hay coincidencias. Amplía los filtros o pulsa Restablecer.',width='100%')),
        section('2 · Detalle de la selección',
            rx.flex(rx.text(SuperstoreState.count,' filas de ',SuperstoreState.loaded_count),
                    rx.button('Descargar CSV filtrado',variant='soft',on_click=SuperstoreState.download,disabled=SuperstoreState.count==0),
                    justify='between',gap='12px',flex_wrap='wrap',margin_bottom='16px'),
            rx.box(rx.table.root(
                rx.table.header(rx.table.row(*[rx.table.column_header_cell(label) for label in ['Pedido','Fecha','Cliente','Región','Categoría','Ventas (€)','Beneficio (€)','Descuento']])),
                rx.table.body(rx.foreach(SuperstoreState.rows,lambda row:rx.table.row(*[rx.table.cell(row[key]) for key in ['order_id','order_date','customer_name','region','category','sales','profit','discount']]))),
                width='100%'),overflow_x='auto',width='100%'),
            rx.flex(rx.button('Anterior',variant='soft',on_click=SuperstoreState.change_page(-1),disabled=SuperstoreState.page<=1),
                    rx.text('Página ',SuperstoreState.page,' de ',SuperstoreState.total_pages),
                    rx.button('Siguiente',variant='soft',on_click=SuperstoreState.change_page(1),disabled=SuperstoreState.page>=SuperstoreState.total_pages),
                    gap='16px',align='center',justify='center',margin_top='20px',flex_wrap='wrap')),
        section('3 · Modelo exploratorio de ventas',
            rx.text('Bosque aleatorio sobre la selección aplicada. División aleatoria 80/20; no es un pronóstico temporal ni mide causalidad. Se excluye profit para evitar utilizar el beneficio de la venta como predictor de su importe.',size='2',color='#64748b'),
            rx.button('Entrenar y evaluar',on_click=SuperstoreState.train,loading=SuperstoreState.training,
                      disabled=(SuperstoreState.count<30)|SuperstoreState.pending,margin_top='16px'),
            rx.text('Mínimo 30 filas. Si cambias los filtros, aplica la selección y vuelve a entrenar.',size='1',margin_top='10px'),
            model_explanation(),
            rx.cond(SuperstoreState.model_error!='',rx.callout(SuperstoreState.model_error,color_scheme='red',margin_top='16px'))),
        section('4 · Relación con el notebook',rx.text('load_superstore prepara el CSV. filtrar_superstore es la misma función que importa el notebook. SuperstoreState.apply equivale a ejecutar las celdas de agregaciones. Recharts sustituye a Matplotlib y los controles web sustituyen a ipywidgets.',size='2')),
        gap='22px',align='stretch',max_width='1440px',margin='0 auto'),
        background_color='#f1f5f9',min_height='100vh',padding=['16px','32px'])



def model_explanation():
    """Explicaciones visibles antes de entrenar; diagnósticos ligados al resultado actual."""
    explanations = [
        ('MAE · Error absoluto medio',
         'Media de |venta real − predicción|, en euros. Si el MAE fuera 50 €, el error absoluto sería de 50 € de media; no significa que cada predicción falle exactamente eso. Menor es mejor.'),
        ('RMSE · Error cuadrático medio, raíz',
         'Eleva los errores al cuadrado, calcula su media y extrae la raíz. Está en euros y penaliza más los fallos grandes. Si supera mucho al MAE, hay errores de tamaños muy desiguales. Menor es mejor.'),
        ('R² · Coeficiente de determinación',
         '1 indica ajuste perfecto; 0 equivale al error cuadrático de predecir la media de las ventas de validación; puede ser negativo. No es un porcentaje de aciertos. Si todas las ventas de validación son iguales, aparece como no definido.'),
        ('Entrenamiento y validación',
         'El modelo aprende con el 80 % y se evalúa con el 20 % restante, separado aleatoriamente. Las gráficas de predicción muestran solo validación. Con pocas filas, las métricas son más inestables.'),
        ('MAE de referencia',
         'Error de una regla sencilla: predecir siempre la media del entrenamiento. Permite comprobar si entrenar mejora esa referencia. Su MAE y el del bosque se calculan sobre las mismas filas de validación.'),
    ]
    return rx.vstack(
        rx.grid(*[rx.box(rx.text(title,weight='bold'),rx.text(text,size='2',color='#475569',margin_top='10px'),
                            padding='18px',background_color='#f8fafc',border_radius='12px')
                  for title,text in explanations],columns=rx.breakpoints(initial='1',md='2'),gap='12px',width='100%'),
        rx.cond(SuperstoreState.model_metrics.length()>0,
            rx.vstack(
                rx.flex(rx.foreach(SuperstoreState.model_metrics.items(),lambda item:rx.badge(item[0],': ',item[1],size='3')),gap='12px',flex_wrap='wrap'),
                rx.callout(SuperstoreState.model_interpretation),
                rx.grid(
                    chart_card('Ventas reales frente a predichas',
                        'Eje horizontal: venta real (€). Vertical: predicción (€). Cerca de la diagonal = poco error; encima = sobreestimación; debajo = subestimación. Se muestran hasta 500 puntos; las métricas usan toda la validación.',
                        rx.recharts.scatter_chart(
                            rx.recharts.cartesian_grid(stroke_dasharray='3 3'),
                            rx.recharts.x_axis(data_key='real',type_='number',name='Venta real (€)',domain=['dataMin','dataMax']),
                            rx.recharts.y_axis(data_key='predicha',type_='number',name='Predicción (€)',domain=['dataMin','dataMax']),
                            rx.recharts.tooltip(),
                            rx.recharts.scatter(data=SuperstoreState.model_points,name='Validación',fill='#6366f1'),
                            rx.recharts.scatter(data=SuperstoreState.model_diagonal,name='Predicción perfecta',line=True,shape='cross',fill='#ef4444'),
                            width='100%',height=320)),
                    chart_card('Error frente a una referencia sencilla',
                        'MAE en euros. Una barra más baja significa menos error absoluto medio en la misma validación. No uses umbrales universales: compara también el valor de las ventas y el coste de equivocarte.',
                        rx.recharts.bar_chart(rx.recharts.x_axis(data_key='modelo'),rx.recharts.y_axis(),rx.recharts.tooltip(),
                            rx.recharts.bar(data_key='mae',name='MAE (€)',fill='#10b981'),
                            data=SuperstoreState.model_comparison,width='100%',height=320)),
                    columns=rx.breakpoints(initial='1',lg='2'),gap='18px',width='100%'),
                section('Mapa de calor · Correlaciones en entrenamiento',
                    rx.text('Correlación de Pearson entre variables numéricas. Azul: positiva (+1); rojo: negativa (−1); blanco: cercana a cero. N/D: variable constante. No mide importancia del modelo ni causalidad, y no incluye las variables categóricas.',size='2',color='#475569'),
                    rx.box(rx.grid(
                        rx.box(),*[rx.text(label,weight='bold',text_align='center',padding='12px') for label in ['Descuento','Cantidad','Ventas']],
                        *[rx.fragment(rx.text(label,weight='bold',padding='12px'),
                            rx.foreach(SuperstoreState.model_heatmap[start:start+3],lambda cell:rx.box(
                                rx.text(cell['label'],weight='bold'),
                                title=cell['row']+' / '+cell['column'],text_align='center',padding='20px',
                                background_color=cell['background'],color=cell['foreground'],border_radius='8px')))
                          for label,start in [('Descuento',0),('Cantidad',3),('Ventas',6)]],
                        columns='4',gap='6px',min_width='440px'),overflow_x='auto',margin_top='18px',width='100%'),
                    rx.text('La diagonal vale 1 cuando la variable no es constante. Una correlación baja no descarta relaciones no lineales que un bosque pueda aprender.',size='2',color='#475569',margin_top='16px')),
                align='stretch',gap='20px',width='100%'),
        ),align='stretch',gap='20px',width='100%',margin_top='20px',
    )
