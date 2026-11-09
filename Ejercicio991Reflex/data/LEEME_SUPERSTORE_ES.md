# Superstore España: datos sintéticos

`superstore.csv` contiene 9.994 líneas ficticias de ventas entre enero de 2023 y octubre de 2026. No contiene transacciones ni clientes reales. Los nombres pueden coincidir casualmente con personas reales.

Incluye 30 ciudades y las 17 comunidades autónomas más Ceuta y Melilla. Los códigos postales son ejemplos de cada localidad. Las regiones son agrupaciones comerciales creadas para el ejercicio, no una división estadística oficial.

Todos los importes son EUR. Ventas = precio de catálogo × cantidad × (1 − descuento). Beneficio bruto = ventas − coste sintético de compra. No se modelan IVA, portes, gastos operativos ni devoluciones. Los valores monetarios se redondean a dos decimales.

Se conservan las 21 columnas originales, la codificación ISO-8859-1 y las fechas internas MM/DD/YYYY para mantener compatibilidad. Los códigos postales deben leerse como texto para conservar sus ceros iniciales.

La copia previa está en `superstore_original.csv`. No se vuelve a sobrescribir al regenerar.

Desde Ejercicio991Reflex:

```bash
python data/generar_superstore_es.py --seed 20261104 --rows 9994
```

Una semilla diferente produce otros valores. La misma semilla reproduce el conjunto. En Reflex abre `/superstore` y pulsa **Recargar CSV**; en el notebook reinicia el kernel y ejecuta desde el principio.
