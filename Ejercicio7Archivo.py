import json
import os

FRUTAS_DISPONIBLES={
    "🍌 Plátano":{"codigo":"01","tipo":"peso","precio_kg":1.35,"stock":10.0},
    "🍎 Manzana":{"codigo":"02","tipo":"peso","precio_kg":0.80,"stock":8.0},
    "🍐 Pera":{"codigo":"03","tipo":"peso","precio_kg":0.85,"stock":6.0},
    "🍊 Naranja":{"codigo":"04","tipo":"peso","precio_kg":0.70,"stock":12.0},
    "🍓 Fresa":{"codigo":"05","tipo":"peso","precio_kg":1.70,"stock":5.0},
    "🍒 Cereza":{"codigo":"06","tipo":"peso","precio_kg":2.20,"stock":5.0},
    "🍑 Durazno":{"codigo":"07","tipo":"peso","precio_kg":1.95,"stock":8.0},
    "🍈 Melón":{"codigo":"08","tipo":"unidad","precio_kg":2.54,"pesos":[0.850,1.250]},
    "🍍 Piña":{"codigo":"09","tipo":"unidad","precio_kg":1.54,"pesos":[0.800,0.750,1.300]},
    "🍉 Sandía":{"codigo":"10","tipo":"unidad","precio_kg":1.44,"pesos":[1.800,1.550,1.400]},
    "🌴 Papaya":{"codigo":"11","tipo":"unidad","precio_kg":1.64,"pesos":[0.800, 0.650, 1.040]},
    "🌰 Durian":{"codigo":"12","tipo":"unidad","precio_kg":5.00,"pesos":[1.800,2.000,2.200,1.950,2.100]},
    "🍇 Uva":{"codigo":"13","tipo":"peso","precio_kg":1.80,"stock":2.0},
    "🥝 Kiwi":{"codigo":"14","tipo":"peso","precio_kg":2.20,"stock":6.0},
    "🥭 Mango":{"codigo":"15","tipo":"peso","precio_kg":2.00,"stock":7.0},
    "🍋 Limón":{"codigo":"16","tipo":"peso","precio_kg":1.40,"stock":10.0},
    "🥥 Coco":{"codigo":"17","tipo":"unidad","precio_kg":3.14,"pesos":[0.860,0.615,0.704]}
}

with open('frutas.json', 'w', encoding='utf-8') as archivo:
    json.dump(FRUTAS_DISPONIBLES, archivo, indent=4, ensure_ascii=False)

if os.path.exists('frutas.json'):
    with open('frutas.json', 'r', encoding='utf-8') as archivo:
        diccionario_cargado = json.load(archivo)
    print(diccionario_cargado)
else:
    print('El diccionario no se ha guardado correctamente.')