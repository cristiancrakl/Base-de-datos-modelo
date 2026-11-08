# Proyecto de bases de datos

Repositorio de ejercicios y recursos de bases de datos relacionales. Incluye
un modelo de facturación de servicios públicos, datos CSV, scripts de
creación e importación y ejemplos de integridad referencial y auditoría.

## Modelo principal: ESPO

El proyecto principal modela la facturación de un servicio público. Sus tablas
incluyen barrios, conceptos tarifarios, grupos familiares, suscriptores,
predios, medidores, lecturas, facturas, detalles de factura y auditoría de
facturas.

Archivos principales:

- `CREACION_TABLAS_PROYECTO/CREACION_TABLAS.sql`: crea las tablas del esquema
  `ESPO`.
- `CREACION_TABLAS_PROYECTO/CREACION_TRIGGER DEL PROYECTO.sql`: crea un
  trigger que registra en `AUDI_FACTURA` las actualizaciones y eliminaciones
  de facturas.
- `CREACION_TABLAS_PROYECTO/IMPORTARDECSV.sql`: contiene ejemplos de carga
  desde archivos CSV. Ajusta las rutas a la ubicación de los archivos y a tu
  entorno antes de ejecutarlo.
- `CREACION_TABLAS_PROYECTO/archivosCSV/`: CSV de ejemplo y generador de datos
  sintéticos.

Los scripts usan sintaxis de PostgreSQL, incluyendo PL/pgSQL y `COPY`. Antes
de crear las tablas, asegúrate de que exista el esquema:

```sql
CREATE SCHEMA IF NOT EXISTS ESPO;
```

Ejecuta después `CREACION_TABLAS_PROYECTO/CREACION_TABLAS.sql` y, si vas a
usar auditoría, `CREACION_TABLAS_PROYECTO/CREACION_TRIGGER DEL PROYECTO.sql`.
La carga de datos debe respetar las claves foráneas: primero las tablas
referenciadas y luego las dependientes. `COPY` lee archivos desde el servidor
de PostgreSQL y puede requerir permisos; actualiza las rutas absolutas del
script para tu equipo.

## Generar datos de prueba

El generador está escrito con la biblioteca estándar de Python. Desde la raíz
del repositorio, ejecútalo en PowerShell:

```powershell
py .\CREACION_TABLAS_PROYECTO\archivosCSV\generar_csv.py
```

Por defecto crea 3.000 registros base y 4.000 facturas en
`CREACION_TABLAS_PROYECTO/archivosCSV/csv_generados/`, sin sobrescribir los
CSV originales. Para cambiar cantidades, semilla o destino:

```powershell
py .\CREACION_TABLAS_PROYECTO\archivosCSV\generar_csv.py `
  --records 500 `
  --invoices 800 `
  --seed 42 `
  --output-dir .\datos_prueba
```

La misma semilla reproduce los mismos datos. El generador produce CSV para
barrios, conceptos, detalles de factura, facturas, grupos familiares,
lecturas, medidores, predios y suscriptores. Al importar, revisa que los
nombres y el orden de las columnas coincidan con las tablas de destino: por
ejemplo, el CSV de detalle contiene `numero_factura`, `id_tarifa` y `valor`,
mientras que la tabla SQL también define `id_detalle`.

## Otros ejercicios

- `integridad referencial/`: ejemplos de claves foráneas con `CASCADE` y el
  comportamiento predeterminado `NO ACTION`.
- `Tabla de auditorias Y tigger/`: ejercicios de triggers y tablas de
  auditoría.
- `POBLAR_TABLAS/`, `INSERTAR_DESDE_ARCHIVO_CSV/` y los SQL de la raíz:
  ejemplos de carga y consultas para otros modelos, incluida una tienda de
  ropa.
- `TALLER2/`: consultas SQL de taller.
- `SupaBASE/`: manifiesto de dependencias de JavaScript con
  `@supabase/supabase-js`.

Estos materiales son scripts y ejercicios independientes; no hay una única
aplicación que los ejecute todos. Revisa cada script antes de ejecutarlo,
porque algunos contienen rutas locales, datos de ejemplo o instrucciones
específicas de un esquema.
