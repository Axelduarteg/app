#!/usr/bin/env python3
"""Resuelve funciones lineales y cuadráticas definidas en un archivo JSON.

Formato JSON recomendado:
{
  "secciones": [
    {
      "tipo": "lineal",
      "operaciones": [
        {"numero": 1, "expresion": "2x+3"}
      ]
    },
    {
      "tipo": "cuadratica",
      "operaciones": [
        {"numero": 1, "expresion": "x^2-4x+3"}
      ]
    }
  ]
}

También admite entradas flexibles como:
{
  "lineales": ["1. f(x) = 4x", "2. f(x) = -2x+1"],
  "cuadraticas": ["1. f(x) = x^2-4x+3"]
}

o secciones donde las operaciones son cadenas:
{"tipo": "lineal", "operaciones": ["1. f(x) = 4x", "2. 3x-8"]}
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Operacion:
    numero: int
    expresion: str


def extraer_expresion(valor: object) -> str:
    """Extrae la expresión matemática desde texto como `1. f(x) = 4x`.

    También acepta directamente expresiones como `4x-2`.
    """
    if not isinstance(valor, str):
        raise ValueError(f"Operación inválida (se esperaba texto): {valor!r}")

    txt = valor.strip()
    if not txt:
        raise ValueError("Operación vacía")

    # Quitar numeración inicial estilo: 1. , 12) , 3 -
    txt = re.sub(r"^\s*\d+\s*[\.)\-:]\s*", "", txt)

    # Quitar prefijo f(x)= o y=
    txt = re.sub(r"^(f\(x\)|y)\s*=\s*", "", txt, flags=re.IGNORECASE)

    if not txt:
        raise ValueError(f"No se pudo extraer expresión válida de: {valor!r}")

    return txt


def normalizar_expresion(expresion: str) -> str:
    expr = expresion.replace(" ", "").replace("**", "^")
    expr = expr.replace("−", "-")
    if not expr:
        raise ValueError("Expresión vacía")
    return expr


def parsear_polinomio(expr: str) -> Dict[int, float]:
    """Parsea un polinomio en x de grado <= 2, p.ej. 2x^2-3x+1."""
    expr = normalizar_expresion(expr)
    if expr[0] not in "+-":
        expr = "+" + expr

    terminos = re.findall(r"[+-][^+-]+", expr)
    coeficientes: Dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0}

    for termino in terminos:
        signo = -1.0 if termino[0] == "-" else 1.0
        cuerpo = termino[1:]

        if "x" not in cuerpo:
            coef = float(cuerpo)
            coeficientes[0] += signo * coef
            continue

        partes = cuerpo.split("x")
        parte_coef = partes[0]
        coef = 1.0 if parte_coef == "" else float(parte_coef)

        if len(partes) > 1 and partes[1]:
            if not partes[1].startswith("^"):
                raise ValueError(f"Término inválido: {termino}")
            grado = int(partes[1][1:])
        else:
            grado = 1

        if grado not in (1, 2):
            raise ValueError(
                "Solo se admiten polinomios lineales o cuadráticos (grados 1 y 2)."
            )

        coeficientes[grado] += signo * coef

    return coeficientes


def evaluar(a: float, b: float, c: float, x: float) -> float:
    return a * x * x + b * x + c


def crear_svg(nombre: str, puntos: List[Tuple[float, float]], salida: Path) -> None:
    ancho, alto = 700, 420
    margen = 30

    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    if math.isclose(min_y, max_y):
        min_y -= 2
        max_y += 2

    def to_px(x: float, y: float) -> Tuple[float, float]:
        px = margen + (x - min_x) * (ancho - 2 * margen) / (max_x - min_x)
        py = alto - margen - (y - min_y) * (alto - 2 * margen) / (max_y - min_y)
        return px, py

    polilinea = " ".join(f"{to_px(x, y)[0]:.2f},{to_px(x, y)[1]:.2f}" for x, y in puntos)

    eje_y_x, _ = to_px(0, min_y)
    _, eje_x_y = to_px(min_x, 0)

    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='{ancho}' height='{alto}'>
  <rect width='100%' height='100%' fill='white'/>
  <line x1='{margen}' y1='{eje_x_y:.2f}' x2='{ancho - margen}' y2='{eje_x_y:.2f}' stroke='#777' stroke-width='1.2'/>
  <line x1='{eje_y_x:.2f}' y1='{margen}' x2='{eje_y_x:.2f}' y2='{alto - margen}' stroke='#777' stroke-width='1.2'/>
  <polyline points='{polilinea}' fill='none' stroke='#1565c0' stroke-width='2.4'/>
  <text x='15' y='20' font-size='14' fill='#111'>{nombre}</text>
</svg>"""

    salida.write_text(svg, encoding="utf-8")


def resolver_lineal(expresion: str, numero: int, carpeta: Path) -> str:
    coef = parsear_polinomio(expresion)
    m = coef[1]
    b = coef[0]

    if math.isclose(m, 0.0):
        raise ValueError(f"La operación {numero} no es lineal: pendiente m = 0")

    x_inter = -b / m
    crecimiento = "crece" if m > 0 else "decrece"

    xs = [i for i in range(-10, 11)]
    puntos = [(x, evaluar(0.0, m, b, x)) for x in xs]
    grafico = carpeta / f"lineal_{numero:02d}.svg"
    crear_svg(f"f(x) = {expresion}", puntos, grafico)

    return (
        f"### Lineal #{numero}\n"
        f"- Función: f(x) = {expresion}\n"
        f"- Paso 1 (identificación): forma y = mx + b, con m = {m:.4g}, b = {b:.4g}.\n"
        f"- Paso 2 (dominio): D = ℝ.\n"
        f"- Paso 3 (rango): R = ℝ (pendiente distinta de 0).\n"
        f"- Paso 4 (comportamiento): la función **{crecimiento}** porque m {'>' if m > 0 else '<'} 0.\n"
        f"- Paso 5 (intersección eje y): x = 0 ⇒ y = b = {b:.4g}, punto (0, {b:.4g}).\n"
        f"- Paso 6 (intersección eje x): y = 0 ⇒ {m:.4g}x + {b:.4g} = 0 ⇒ x = {x_inter:.4g}, punto ({x_inter:.4g}, 0).\n"
        f"- Gráfica: `{grafico.as_posix()}`.\n"
    )


def resolver_cuadratica(expresion: str, numero: int, carpeta: Path) -> str:
    coef = parsear_polinomio(expresion)
    a, b, c = coef[2], coef[1], coef[0]

    if math.isclose(a, 0.0):
        raise ValueError(f"La operación {numero} no es cuadrática: a = 0")

    xv = -b / (2 * a)
    yv = evaluar(a, b, c, xv)
    dom = "D = ℝ"
    rango = f"R = [ {yv:.4g}, +∞ )" if a > 0 else f"R = ( -∞, {yv:.4g} ]"

    x_tabla = [xv - 2, xv - 1, xv, xv + 1, xv + 2]
    tabla = [(x, evaluar(a, b, c, x)) for x in x_tabla]

    delta = b * b - 4 * a * c
    if delta < 0:
        cortes_x = "No hay intersecciones reales con el eje x."
    elif math.isclose(delta, 0.0):
        xr = -b / (2 * a)
        cortes_x = f"Una intersección real doble en ({xr:.4g}, 0)."
    else:
        rdelta = math.sqrt(delta)
        x1 = (-b - rdelta) / (2 * a)
        x2 = (-b + rdelta) / (2 * a)
        cortes_x = f"Dos intersecciones reales: ({x1:.4g}, 0) y ({x2:.4g}, 0)."

    xs = [xv - 8 + i * 0.25 for i in range(65)]
    puntos = [(x, evaluar(a, b, c, x)) for x in xs]
    grafico = carpeta / f"cuadratica_{numero:02d}.svg"
    crear_svg(f"f(x) = {expresion}", puntos, grafico)

    tabla_txt = "\n".join(f"  - x = {x:.4g} -> y = {y:.4g}" for x, y in tabla)

    return (
        f"### Cuadrática #{numero}\n"
        f"- Función: f(x) = {expresion}\n"
        f"- Paso 1 (identificación): forma ax² + bx + c, con a = {a:.4g}, b = {b:.4g}, c = {c:.4g}.\n"
        f"- Paso 2 (vértice): xᵥ = -b/(2a) = {xv:.4g}; yᵥ = f(xᵥ) = {yv:.4g}. Vértice V({xv:.4g}, {yv:.4g}).\n"
        f"- Paso 3 (dominio): {dom}.\n"
        f"- Paso 4 (rango): {rango}.\n"
        f"- Paso 5 (tabla de valores):\n{tabla_txt}\n"
        f"- Paso 6 (intersección con eje y): (0, {c:.4g}).\n"
        f"- Paso 7 (intersecciones con eje x): {cortes_x}\n"
        f"- Gráfica: `{grafico.as_posix()}`.\n"
    )


def _tipo_normalizado(tipo: str) -> str:
    tipo_n = tipo.strip().lower()
    if tipo_n in {"lineal", "lineales"}:
        return "lineal"
    if tipo_n in {"cuadratica", "cuadrático", "cuadratica", "cuadraticas", "cuadráticas"}:
        return "cuadratica"
    return tipo_n


def _mapear_operaciones(ops: object) -> List[Operacion]:
    if not isinstance(ops, list):
        raise ValueError("El campo 'operaciones' debe ser una lista.")

    salida: List[Operacion] = []
    for idx, op in enumerate(ops, start=1):
        if isinstance(op, dict):
            numero = int(op.get("numero", idx))
            expresion = extraer_expresion(op.get("expresion", ""))
        else:
            numero = idx
            expresion = extraer_expresion(op)
        salida.append(Operacion(numero=numero, expresion=expresion))
    return salida


def cargar_operaciones(ruta: Path) -> List[Tuple[str, List[Operacion]]]:
    data = json.loads(ruta.read_text(encoding="utf-8"))

    resultado: List[Tuple[str, List[Operacion]]] = []

    if isinstance(data, dict) and isinstance(data.get("secciones"), list):
        for seccion in data["secciones"]:
            tipo = _tipo_normalizado(str(seccion.get("tipo", "")))
            if tipo not in {"lineal", "cuadratica"}:
                raise ValueError(f"Tipo no soportado: {tipo}")
            resultado.append((tipo, _mapear_operaciones(seccion.get("operaciones", []))))
        if resultado:
            return resultado

    # Formato alternativo: claves de bloque en raíz
    if isinstance(data, dict):
        for clave in ("lineales", "lineal"):
            if clave in data:
                resultado.append(("lineal", _mapear_operaciones(data[clave])))
                break
        for clave in ("cuadraticas", "cuadráticas", "cuadratica", "cuadrática"):
            if clave in data:
                resultado.append(("cuadratica", _mapear_operaciones(data[clave])))
                break

    if not resultado:
        raise ValueError(
            "JSON no válido. Usa 'secciones' o claves raíz 'lineales'/'cuadraticas'."
        )

    return resultado



def descubrir_json_en_carpeta_programa() -> Path:
    """Busca un archivo JSON en la misma carpeta donde vive este script."""
    carpeta = Path(__file__).resolve().parent
    preferido = carpeta / "archivo.json"
    if preferido.exists():
        return preferido

    candidatos = sorted(carpeta.glob("*.json"))
    if len(candidatos) == 1:
        return candidatos[0]

    if not candidatos:
        raise FileNotFoundError(
            f"No se encontró ningún .json en la carpeta del programa: {carpeta}"
        )

    nombres = ", ".join(c.name for c in candidatos)
    raise FileExistsError(
        "Hay múltiples JSON en la carpeta del programa. "
        "Indica uno explícitamente con el argumento 'json'. "
        f"Detectados: {nombres}"
    )

def resolver_archivo(ruta_json: Path, salida: Path) -> Path:
    salida.mkdir(parents=True, exist_ok=True)
    bloques = cargar_operaciones(ruta_json)

    reporte_partes = [f"# Resolución automática\n\nArchivo fuente: `{ruta_json.as_posix()}`\n"]

    for tipo, operaciones in bloques:
        encabezado = "## Bloque de funciones lineales\n" if tipo == "lineal" else "## Bloque de funciones cuadráticas\n"
        reporte_partes.append(encabezado)

        for op in operaciones:
            if tipo == "lineal":
                reporte_partes.append(resolver_lineal(op.expresion, op.numero, salida))
            else:
                reporte_partes.append(resolver_cuadratica(op.expresion, op.numero, salida))

    reporte = salida / "reporte.md"
    reporte.write_text("\n".join(reporte_partes), encoding="utf-8")
    return reporte


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resuelve funciones lineales (primer bloque) y cuadráticas (bloques siguientes) desde JSON."
    )
    parser.add_argument("json", nargs="?", type=Path, help="Ruta del archivo JSON con las operaciones (opcional). Si se omite, se busca en la carpeta del programa.")
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("salida_resolucion"),
        help="Carpeta donde se guardarán reporte y gráficas",
    )
    args = parser.parse_args()

    ruta_json = args.json if args.json is not None else descubrir_json_en_carpeta_programa()
    reporte = resolver_archivo(ruta_json, args.salida)
    print(f"Resolución completada. Reporte: {reporte}")


if __name__ == "__main__":
    main()
