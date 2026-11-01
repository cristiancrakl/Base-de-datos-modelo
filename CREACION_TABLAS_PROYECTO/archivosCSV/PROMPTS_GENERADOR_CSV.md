# Prompts posibles para solicitar el generador de CSV

Estos son ejemplos de solicitudes que podrían producir el generador incluido en
`generar_csv.py`. Los CSV originales no se modifican: por defecto, los archivos
se crean en la carpeta `csv_generados`.

## 1. Solicitud completa

> Revisa los archivos CSV de esta carpeta y crea un script de Python que genere
> archivos sintéticos con las mismas columnas. Mantén consistentes las
> relaciones entre barrios, predios, suscriptores, grupos familiares, medidores,
> lecturas, conceptos, facturas y detalles. Permite indicar la carpeta de
> salida, las cantidades de registros y una semilla aleatoria reproducible.
> No sobrescribas los CSV originales. Incluye un Markdown con otras formas en
> que podría haber pedido este trabajo.

## 2. Enfoque en integridad referencial

> Crea un generador Python para estos CSV. Los identificadores usados como
> referencias deben existir en sus tablas correspondientes; cada factura debe
> tener un detalle con el mismo total, y los valores generados deben respetar
> las columnas y formatos de fecha. Usa únicamente la biblioteca estándar y
> guarda los resultados en una carpeta nueva.

## 3. Enfoque en configuración por consola

> Escribe un programa Python ejecutable desde la terminal para generar estos
> nueve CSV. Añade opciones para configurar la carpeta destino, el número base
> de registros, el número de facturas y la semilla. Usa valores predeterminados
> razonables, valida cantidades positivas y muestra cuántas filas generó en
> cada archivo.

## 4. Enfoque en reproducibilidad

> Genera datos ficticios para estas tablas CSV mediante Python. La misma semilla
> debe producir exactamente el mismo conjunto de datos. Conserva los nombres de
> las columnas, genera claves únicas y asegura que las claves foráneas apunten
> a filas existentes. No edites los archivos de entrada.

## 5. Solicitud breve

> Hazme un generador en Python para los CSV de esta carpeta, con datos ficticios
> y relaciones válidas entre tablas. Déjalo parametrizable y crea también un
> archivo Markdown con prompts alternativos para pedirlo.

## Nota sobre el SQL adjunto

El SQL de referencia define funciones y triggers para el esquema `TIENDA_ROPA`
y tablas `ARTICULO`, `DETALLE` y `FACTURA`. No coincide con las tablas de estos
CSV, que corresponden a predios, suscriptores, lecturas y facturación de un
servicio. Por eso el generador sigue las columnas y relaciones observables de
los CSV, sin inferir estructuras del SQL ajeno.

El encabezado de año de `lectura.csv` aparece literalmente como `aÃ±o` en el
CSV existente (texto con codificación dañada); el generador lo conserva para
mantener compatibilidad con ese encabezado. Los valores nuevos son años
completos, entre 2021 y 2025.

## Ejecución

Desde esta carpeta:

```powershell
python generar_csv.py
```

Para cambiar cantidades y destino:

```powershell
python generar_csv.py --records 500 --invoices 800 --seed 42 --output-dir datos_prueba
```
