"""Genera Superstore ficticio de España. No representa ventas ni personas reales.

Uso: python generar_superstore_es.py --seed 20261104 --rows 9994
Conserva una copia del CSV anterior antes de sustituirlo. Precios y costes en EUR.
El esquema, codificación y formato de fechas conservan compatibilidad con el notebook.
"""
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import argparse
import csv
import random
import shutil

# Ciudad, comunidad/ciudad autónoma, código postal de ejemplo y región comercial.
LOCATIONS = [
 ('Madrid','Comunidad de Madrid','28013','Centro'),
 ('Barcelona','Cataluña','08002','Este'), ('Girona','Cataluña','17001','Este'),
 ('Valencia','Comunidad Valenciana','46001','Este'),('Alicante','Comunidad Valenciana','03001','Este'),
 ('Sevilla','Andalucía','41001','Sur'),('Málaga','Andalucía','29001','Sur'),('Granada','Andalucía','18001','Sur'),
 ('Zaragoza','Aragón','50001','Noreste'),('Huesca','Aragón','22001','Noreste'),
 ('Bilbao','País Vasco','48001','Norte'),('Vitoria-Gasteiz','País Vasco','01001','Norte'),
 ('Santander','Cantabria','39001','Norte'),('Oviedo','Principado de Asturias','33001','Norte'),
 ('A Coruña','Galicia','15001','Noroeste'),('Vigo','Galicia','36201','Noroeste'),
 ('Valladolid','Castilla y León','47001','Centro'),('Salamanca','Castilla y León','37001','Centro'),
 ('Toledo','Castilla-La Mancha','45001','Centro'),('Albacete','Castilla-La Mancha','02001','Centro'),
 ('Mérida','Extremadura','06800','Oeste'),('Cáceres','Extremadura','10001','Oeste'),
 ('Murcia','Región de Murcia','30001','Sureste'),('Pamplona','Comunidad Foral de Navarra','31001','Norte'),
 ('Logroño','La Rioja','26001','Norte'),('Palma','Islas Baleares','07001','Islas'),
 ('Las Palmas de Gran Canaria','Canarias','35001','Islas'),('Santa Cruz de Tenerife','Canarias','38001','Islas'),
 ('Ceuta','Ceuta','51001','Sur'),('Melilla','Melilla','52001','Sur'),
]
CATALOG = [
 ('Mobiliario','Sillas','Silla ergonómica',149,79),('Mobiliario','Mesas','Mesa de trabajo',249,145),
 ('Mobiliario','Estanterías','Estantería modular',119,64),('Mobiliario','Armarios','Armario de oficina',329,201),
 ('Material de oficina','Papel','Papel A4 paquete',5.9,2.8),('Material de oficina','Carpetas','Carpeta archivadora',8.5,3.6),
 ('Material de oficina','Escritura','Bolígrafos caja',12.9,5.4),('Material de oficina','Organización','Organizador de escritorio',24.9,11.2),
 ('Tecnología','Portátiles','Portátil profesional',899,670),('Tecnología','Monitores','Monitor de oficina',229,149),
 ('Tecnología','Impresoras','Impresora multifunción',319,208),('Tecnología','Accesorios','Teclado inalámbrico',49.9,22.5),
 ('Tecnología','Accesorios','Ratón inalámbrico',29.9,12.1),('Tecnología','Almacenamiento','Disco SSD',89.9,51.5),
]
FIELDS=['Row ID','Order ID','Order Date','Ship Date','Ship Mode','Customer ID','Customer Name','Segment','Country','City','State','Postal Code','Region','Product ID','Category','Sub-Category','Product Name','Sales','Quantity','Discount','Profit']


def money(value):
 return Decimal(str(value)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)


def generate(seed=20261104, count=9994):
 rng=random.Random(seed)
 first=['Lucía','Hugo','Martina','Mateo','Sofía','Daniel','Paula','Alejandro','Valeria','Pablo','Carmen','Diego','Elena','Javier','Nuria','Álvaro','Irene','Sergio','Aitana','Marcos']
 last=['García','Martínez','López','Sánchez','Pérez','Gómez','Fernández','Ruiz','Díaz','Moreno','Muñoz','Romero','Alonso','Gutiérrez','Navarro','Torres']
 customers=[]
 for i in range(450):
  customers.append((f'ES-CLI-{i+1:05}',f'{rng.choice(first)} {rng.choice(last)} {rng.choice(last)}',rng.choice(LOCATIONS),rng.choice(['Particular','Empresa','Oficina en casa'])))
 # Productos con variantes y SKU constantes; precio/coste de catálogo coherentes.
 products=[]
 for i,(cat,sub,name,price,cost) in enumerate(CATALOG):
  for variant in range(3):
   multiplier=Decimal(str(1+variant*.18))
   products.append((f'ES-PRO-{i+1:03}-{variant+1}',cat,sub,f'{name} · Serie {variant+1}',money(Decimal(str(price))*multiplier),money(Decimal(str(cost))*multiplier)))
 rows=[]; order=0; start=date(2023,1,1); end=date(2026,10,31)
 while len(rows)<count:
  order+=1
  customer_id,name,location,segment=rng.choice(customers)
  city,state,postal,region=location
  # Estacionalidad sintética: mayor probabilidad de pedidos en noviembre/diciembre.
  while True:
   ordered=start+timedelta(days=rng.randrange((end-start).days+1))
   if rng.random() < (1 if ordered.month in (11,12) else .7):break
  mode=rng.choices(['Estándar','Exprés','Entrega en el día'],weights=[70,25,5])[0]
  delay=rng.randint(3,7) if mode=='Estándar' else rng.randint(1,2) if mode=='Exprés' else 0
  shipped=ordered+timedelta(days=delay)
  order_id=f'ES-{ordered.year}-{order:06}'
  for _ in range(min(rng.randint(1,4),count-len(rows))):
   sku,cat,sub,product,price,cost=rng.choice(products)
   quantity=rng.choices([1,2,3,4,5,6,8,10],weights=[23,22,15,12,10,8,6,4])[0]
   discount=rng.choices([0,.05,.1,.15,.2,.3,.4,.5],weights=[40,10,15,10,10,7,5,3])[0]
   sales=money(price*quantity*(1-Decimal(str(discount))))
   # Beneficio bruto sintético = ventas netas - coste de compra; puede ser negativo.
   profit=money(sales-cost*quantity)
   rows.append([len(rows)+1,order_id,ordered.strftime('%m/%d/%Y'),shipped.strftime('%m/%d/%Y'),mode,customer_id,name,segment,'España',city,state,postal,region,sku,cat,sub,product,str(sales),quantity,discount,str(profit)])
 return rows


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--seed',type=int,default=20261104)
 parser.add_argument('--rows',type=int,default=9994)
 args=parser.parse_args()
 if not 1<=args.rows<=100000:parser.error('--rows debe estar entre 1 y 100000')
 target=Path(__file__).with_name('superstore.csv')
 backup=target.with_name('superstore_original.csv')
 if target.exists() and not backup.exists():shutil.copy2(target,backup)
 with target.open('w',encoding='ISO-8859-1',newline='') as f:
  writer=csv.writer(f);writer.writerow(FIELDS);writer.writerows(generate(args.seed,args.rows))
 print(f'{args.rows} filas ficticias generadas en {target}. Semilla: {args.seed}. Copia original: {backup}')


if __name__=='__main__':main()
