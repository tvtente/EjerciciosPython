import re
import unicodedata

import SinClasificar.Utilitario as Utilitario


# Datos fijos del catálogo.
frutas = {
	"Plátano": {"codigo": "01", "precio": 1.35, "disponibilidad": 10.0, "ventaxunidad": False},
	"Manzana": {"codigo": "02", "precio": 0.80, "disponibilidad": 8.0,  "ventaxunidad": False},
	"Pera":    {"codigo": "03", "precio": 0.85, "disponibilidad": 6.0,  "ventaxunidad": False},
	"Naranja": {"codigo": "04", "precio": 0.70, "disponibilidad": 12.0, "ventaxunidad": False},
	"Melón":   {"codigo": "05", "precio": 2.00, "disponibilidad": 5,    "ventaxunidad": True},
	"Sandía":  {"codigo": "06", "precio": 1.80, "disponibilidad": 7,    "ventaxunidad": True},
	"Durian":  {"codigo": "07", "precio": 5.00, "disponibilidad": 5,    "ventaxunidad": True}
}
emojis = {
	"Plátano": "🍌",
	"Manzana": "🍎",
	"Pera": "🍐",
	"Naranja": "🍊",
    "Melón": "🍈",
    "Sandía": "🍉",
    "Durian": "🥭",
	"Bolsa": "👜",
}

patron_kilos = r"^\d+(?:[,.]\d+)?$"
carrito = {}
salir = ""


while salir != "s":
	# PASO 1: mostrar el catálogo y el estado actual del carrito.
	Utilitario.borro()

	print("\nPASO 1: consultar el catálogo y el carrito")
	print("=" * 52)
	print("🛒 FRUTAS DISPONIBLES")
	print("+--------+----------------+-------------+-------------+-----------------+")
	print("| Código | Fruta          | Precio/kg   | Disponible  | Venta x Unidad  |")
	print("+--------+----------------+-------------+-------------+-----------------+")

	for nombre, datos in frutas.items():
		etiqueta = f"{emojis[nombre]} {nombre}"
		print(
			f"| {datos['codigo']:^6} | {etiqueta:<13} | "
			f"{datos['precio']:>6.2f} €/kg | "
			f"{datos['disponibilidad']:>7.2f} kg | "
			f"{'Sí' if datos['ventaxunidad'] else 'No':^15} |"
		)

	print("+--------+----------------+-------------+-------------+-----------------+")
	print("\n🛒 CARRITO DE COMPRA")

	if carrito:
		print("+--------+----------------+--------+------------+-------------+-----------------+")
		print("| Código | Producto       | Cant.  | Precio     | Subtotal    | Venta x Unidad  |")
		print("+--------+----------------+--------+------------+-------------+-----------------+")

		for nombre, datos in carrito.items():
			etiqueta = f"{emojis[nombre]} {nombre}"
			print(
				f"| {datos['codigo']:^6} | {etiqueta:<13} | "
				f"{datos['kg']:>6.2f} | {datos['precio']:>8.2f} € | "
				f"{datos['subtotal']:>9.2f} € | "
				f"{'Sí' if datos['ventaxunidad'] else 'No':^15} |"
			)

		total = sum(
			datos["subtotal"]
			for datos in carrito.values()
		)
		print("+--------------------------------------+-------------+")
		print(f"| {'Total a pagar':<36} | {total:>9.2f} € |")
		print("+--------------------------------------+-------------+")
	else:
		print("+----------------------------------------------------+")
		print(f"| {'El carrito está vacío.':^52} |")
		print("+----------------------------------------------------+")

	# PASO 2: pedir una fruta válida o buscar una coincidencia.
	print("\nPASO 2: elegir una fruta")
	while True:
		texto_fruta = input("¿Qué fruta quieres? ").strip()
		fruta = texto_fruta.title()

		if fruta in frutas:
			if frutas[fruta]["disponibilidad"] > 0:
				break

			print(f"⚠️ Ya no queda {fruta} disponible.")
			continue

		texto_busqueda = texto_fruta.casefold()
		texto_busqueda = unicodedata.normalize("NFD", texto_busqueda)
		texto_busqueda = "".join(
			caracter
			for caracter in texto_busqueda
			if unicodedata.category(caracter) != "Mn"
		)
		coincidencias = []

		for nombre in frutas:
			nombre_busqueda = nombre.casefold()
			nombre_busqueda = unicodedata.normalize("NFD", nombre_busqueda)
			nombre_busqueda = "".join(
				caracter
				for caracter in nombre_busqueda
				if unicodedata.category(caracter) != "Mn"
			)

			if (
				len(texto_busqueda) >= 3
				and texto_busqueda in nombre_busqueda
			):
				coincidencias.append(nombre)

		if len(coincidencias) == 1:
			sugerencia = coincidencias[0]
			confirmar = input(
				f"¿Quizás te referías a {sugerencia}? 🤔 (S/N): "
			).strip().lower()

			while confirmar not in ("s", "n"):
				confirmar = input(
					"⚠️ Escribe S para sí o N para no: "
				).strip().lower()

			if confirmar == "s":
				fruta = sugerencia
				break
		else:
			print("⚠️ No encuentro esa fruta. Inténtalo de nuevo.")

	# Si la fruta ya existe, la nueva cantidad reemplaza la anterior.
	if fruta in carrito:
		print(
			f"\n🛒 Ya tienes {carrito[fruta]['kg']:.2f} kg de {fruta}."
		)
		print("La nueva cantidad reemplazará a la anterior.")

	cantidad_anterior = carrito.get(fruta, {}).get("kg", 0)
	kilos_disponibles = frutas[fruta]["disponibilidad"] + cantidad_anterior

	# PASO 3: pedir y validar la cantidad de kilos.
	print("\nPASO 3: indicar la cantidad")
	kg_texto = input("¿Cuántos kilos quieres? ").strip()

	while (
		not re.fullmatch(patron_kilos, kg_texto)
		or float(kg_texto.replace(",", ".")) <= 0
		or float(kg_texto.replace(",", ".")) > kilos_disponibles
	):
		if re.fullmatch(patron_kilos, kg_texto):
			print(
				f"⚠️ No puedes superar los {kilos_disponibles:.2f} kg "
				"disponibles."
			)
		else:
			print("⚠️ Escribe una cantidad válida mayor que cero.")

		kg_texto = input("¿Cuántos kilos quieres? ").strip()

	kg = float(kg_texto.replace(",", "."))

	# PASO 4: guardar la fruta y calcular su subtotal.
	print("\nPASO 4: guardar la compra en el carrito")
	precio = frutas[fruta]["precio"]
	subtotal = precio * kg
	frutas[fruta]["disponibilidad"] = kilos_disponibles - kg
	carrito[fruta] = {
		"codigo": frutas[fruta]["codigo"],
		"kg": kg,
		"precio": precio,
		"subtotal": subtotal,
		"ventaxunidad": frutas[fruta]["ventaxunidad"],
	}

	print(
		f"✅ Se han guardado {kg:.2f} kg de {fruta} "
		f"por {subtotal:.2f} €."
	)

	salir = input(
		"\nPulsa Enter para otra compra o S para salir: "
	).strip().lower()

	while salir not in ("", "s"):
		salir = input(
			"⚠️ Pulsa Enter o escribe S para salir: "
		).strip().lower()


# PASO 5: preguntar si se desea añadir una bolsa.
print("\nPASO 5: preparar el resumen final")
bolsa = input("¿Quieres una bolsa por 0,10 €? (S/N): ").strip().lower()

while bolsa not in ("s", "si", "sí", "n", "no"):
	bolsa = input(
		"⚠️ Escribe S para sí o N para no: "
	).strip().lower()

if bolsa in ("s", "si", "sí"):
	carrito["Bolsa"] = {
		"codigo": "B01",
		"kg": 1,
		"precio": 0.10,
		"subtotal": 0.10,
		"ventaxunidad": True,
	}
	print("✅ Bolsa añadida al carrito.")
else:
	print("✅ No se ha añadido ninguna bolsa.")


# PASO 6: mostrar el resumen final.
Utilitario.borro()
print("\nPASO 6: compra finalizada")
print("=" * 52)
print("🛒 CARRITO FINAL")
print("+--------+----------------+--------+------------+-------------+-----------------+")
print("| Código | Producto       | Cant.  | Precio     | Subtotal    | Venta x Unidad  |")
print("+--------+----------------+--------+------------+-------------+-----------------+")

for nombre, datos in carrito.items():
	etiqueta = f"{emojis[nombre]} {nombre}"
	print(
		f"| {datos['codigo']:^6} | {etiqueta:<13} | "
		f"{datos['kg']:>6.2f} | {datos['precio']:>8.2f} € | "
		f"{datos['subtotal']:>9.2f} € | "
		f"{'Sí' if datos['ventaxunidad'] else 'No':^15} |"
	)

total = sum(
	datos["subtotal"]
	for datos in carrito.values()
)
print("+--------------------------------------+-------------+")
print(f"| {'Total a pagar':<36} | {total:>9.2f} € |")
print("+--------------------------------------+-------------+")
print("\n👋 ¡Gracias por tu compra!")
