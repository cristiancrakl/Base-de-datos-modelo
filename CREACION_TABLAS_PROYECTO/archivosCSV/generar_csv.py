#!/usr/bin/env python3
"""Genera datos sintéticos relacionados para los CSV del proyecto."""

import argparse
import csv
import random
import string
from datetime import date, timedelta
from pathlib import Path


MESES = (
    "ENERO",
    "FEBRERO",
    "MARZO",
    "ABRIL",
    "MAYO",
    "JUNIO",
    "JULIO",
    "AGOSTO",
    "SEPTIEMBRE",
    "OCTUBRE",
    "NOVIEMBRE",
    "DICIEMBRE",
)
NOMBRES = (
    "Valentina",
    "Diana",
    "Carlos",
    "Andres",
    "Lucia",
    "Sofia",
    "Mateo",
    "Samuel",
    "Camila",
    "Daniel",
)
APELLIDOS = (
    "Hernandez",
    "Ramirez",
    "Moreno",
    "Ortiz",
    "Gomez",
    "Castro",
    "Lopez",
    "Martinez",
    "Torres",
    "Rojas",
)
TIPOS_USO = ("Residencial", "Comercial", "Industrial", "Oficial", "Especial")
CODIGOS_BARRIO = string.digits + string.ascii_uppercase + string.ascii_lowercase


def escribir_csv(ruta: Path, columnas: list[str], filas: list[dict[str, object]]) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def generar(output_dir: Path, registros: int, facturas: int, seed: int) -> None:
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    grupos = [
        {
            "id_grupo": f"G{i:06d}",
            "nombre_grupo": (
                f"Familia {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)} {i}"
            ),
        }
        for i in range(1, registros + 1)
    ]
    ids_grupo = [fila["id_grupo"] for fila in grupos]

    suscriptores = []
    for i in range(1, registros + 1):
        nombre = rng.choice(NOMBRES)
        apellido = rng.choice(APELLIDOS)
        suscriptores.append(
            {
                "id_suscriptor": f"S{i:09d}",
                "nombres": nombre,
                "apellidos": apellido,
                "telefono": f"3{rng.randint(0, 999999999):09d}",
                "email": f"{nombre.lower()}.{apellido.lower()}{i}@correo.com",
                "id_grupo": rng.choice(ids_grupo),
            }
        )
    ids_suscriptor = [fila["id_suscriptor"] for fila in suscriptores]

    barrios = [
        {"cod_barrio": codigo, "nombre_barrio": f"Barrio {i}"}
        for i, codigo in enumerate(CODIGOS_BARRIO, start=1)
    ]
    predios = []
    medidores = []
    lecturas = []
    for i in range(1, registros + 1):
        numero_matricula = f"M{i:05d}"
        numero_medidor = f"MED{i:09d}"
        fecha_lectura = date(
            rng.randint(2021, 2025), rng.randint(1, 12), rng.randint(1, 28)
        )
        predios.append(
            {
                "numero_matricula": numero_matricula,
                "direccion": (
                    f"Calle {rng.randint(1, 150)} # "
                    f"{rng.randint(1, 99)}-{rng.randint(1, 99)}"
                ),
                "estrato_socioeconomico": rng.randint(1, 6),
                "tipo_uso": rng.choice(TIPOS_USO),
                "id_suscriptor": ids_suscriptor[i - 1],
                "cod_barrio": rng.choice(CODIGOS_BARRIO),
            }
        )
        medidores.append({"numero_medidor": numero_medidor})
        lecturas.append(
            {
                "numero_matricula": numero_matricula,
                "numero_medidor": numero_medidor,
                "fecha": fecha_lectura.isoformat(),
                "valor": rng.randint(1_000, 100_000),
                "mes": MESES[fecha_lectura.month - 1],
                "aÃ±o": fecha_lectura.year,
            }
        )

    conceptos = []
    for i in range(1, registros + 1):
        conceptos.append(
            {
                "id_tarifa": f"T{i:05d}",
                "periodo_vigencia": (
                    f"{rng.randint(2021, 2025)}-{rng.randint(1, 12):02d}"
                ),
                "estrato": rng.randint(1, 6),
                "valor_cargo_fijo": f"{rng.uniform(4_000, 25_000):.2f}",
                "valor_m3_agua": f"{rng.uniform(1_000, 10_000):.2f}",
                "tasa_alcantarillado": f"{rng.uniform(10, 40):.2f}",
                "porc_subsidio_contrib": f"{rng.uniform(-35, 30):.2f}",
            }
        )

    facturas_csv = []
    detalles = []
    ids_predio = [fila["numero_matricula"] for fila in predios]
    ids_tarifa = [fila["id_tarifa"] for fila in conceptos]
    conceptos_por_id = {fila["id_tarifa"]: fila for fila in conceptos}
    for i in range(1, facturas + 1):
        periodo_anio = rng.randint(2021, 2025)
        periodo_mes = rng.randint(1, 12)
        fecha_emision = date(periodo_anio, periodo_mes, rng.randint(1, 28))
        fecha_limite = fecha_emision + timedelta(days=15)
        estado = rng.choice(("N", "P", "S"))
        fecha_suspension = (
            (fecha_limite + timedelta(days=30)).isoformat() if estado == "S" else ""
        )
        lectura_anterior = rng.randint(1_000, 100_000)
        lectura_actual = lectura_anterior + rng.randint(1, 100)
        id_tarifa = rng.choice(ids_tarifa)
        tarifa = conceptos_por_id[id_tarifa]
        consumo = lectura_actual - lectura_anterior
        subtotal = float(tarifa["valor_cargo_fijo"]) + (
            consumo
            * float(tarifa["valor_m3_agua"])
            * (1 + float(tarifa["tasa_alcantarillado"]) / 100)
        )
        total = round(
            subtotal * (1 - float(tarifa["porc_subsidio_contrib"]) / 100), 2
        )
        numero_factura = f"F{i:05d}"
        facturas_csv.append(
            {
                "numero_factura": numero_factura,
                "numero_matricula": rng.choice(ids_predio),
                "fecha_emision": fecha_emision.isoformat(),
                "periodo_facturado": f"{periodo_anio}-{periodo_mes:02d}",
                "fecha_limite_pago": fecha_limite.isoformat(),
                "fecha_suspension": fecha_suspension,
                "estado": estado,
                "lectura_anterior": lectura_anterior,
                "lectura_actual": lectura_actual,
                "total": f"{total:.2f}",
            }
        )
        detalles.append(
            {
                "numero_factura": numero_factura,
                "id_tarifa": id_tarifa,
                "valor": f"{total:.2f}",
            }
        )

    archivos = {
        "barrio.csv": (
            ["cod_barrio", "nombre_barrio"],
            barrios,
        ),
        "concepto.csv": (
            [
                "id_tarifa",
                "periodo_vigencia",
                "estrato",
                "valor_cargo_fijo",
                "valor_m3_agua",
                "tasa_alcantarillado",
                "porc_subsidio_contrib",
            ],
            conceptos,
        ),
        "detalle_factura.csv": (
            ["numero_factura", "id_tarifa", "valor"],
            detalles,
        ),
        "factura.csv": (
            [
                "numero_factura",
                "numero_matricula",
                "fecha_emision",
                "periodo_facturado",
                "fecha_limite_pago",
                "fecha_suspension",
                "estado",
                "lectura_anterior",
                "lectura_actual",
                "total",
            ],
            facturas_csv,
        ),
        "grupo_familiar.csv": (["id_grupo", "nombre_grupo"], grupos),
        "lectura.csv": (
            [
                "numero_matricula",
                "numero_medidor",
                "fecha",
                "valor",
                "mes",
                "aÃ±o",
            ],
            lecturas,
        ),
        "medidor.csv": (["numero_medidor"], medidores),
        "predio.csv": (
            [
                "numero_matricula",
                "direccion",
                "estrato_socioeconomico",
                "tipo_uso",
                "id_suscriptor",
                "cod_barrio",
            ],
            predios,
        ),
        "suscriptor.csv": (
            ["id_suscriptor", "nombres", "apellidos", "telefono", "email", "id_grupo"],
            suscriptores,
        ),
    }

    for nombre, (columnas, filas) in archivos.items():
        escribir_csv(output_dir / nombre, columnas, filas)
        print(f"{nombre}: {len(filas)} registros")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera los CSV del proyecto con datos sintéticos relacionados."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "csv_generados",
        help="Carpeta destino (por defecto: ./csv_generados).",
    )
    parser.add_argument(
        "--records",
        type=int,
        default=3000,
        help="Cantidad base de grupos, suscriptores, predios, lecturas y tarifas.",
    )
    parser.add_argument(
        "--invoices",
        type=int,
        default=4000,
        help="Cantidad de facturas y detalles de factura.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Semilla aleatoria para poder repetir la generación.",
    )
    args = parser.parse_args()
    if args.records < 1:
        parser.error("--records debe ser mayor que cero.")
    if args.invoices < 1:
        parser.error("--invoices debe ser mayor que cero.")

    generar(args.output_dir, args.records, args.invoices, args.seed)


if __name__ == "__main__":
    main()
