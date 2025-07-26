import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import sympy as sp
from procesador_matematico import (
    limpiar_expresion,
    validar_expresion,
    formatear_expresion,
    procesar_limite,
    procesar_derivada,
    procesar_integral
)

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API key desde el entorno
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No se encontró la API key de Gemini en el archivo .env")

# Configurar Gemini con la API Key
genai.configure(api_key=GEMINI_API_KEY)

def extraer_expresion(problema):
    tipo_operacion = None
    valor_limite = None
    expr = None

    texto = problema.lower()

    if "derivar" in texto or "derivada" in texto:
        tipo_operacion = "derivada"
    elif "integrar" in texto or "integral" in texto:
        tipo_operacion = "integral"
    elif "limite" in texto or "límite" in texto:
        tipo_operacion = "limite"
        match_limite = re.search(r'x\s+tiende\s+a\s+([+-]?\d+(?:\.\d+)?|infinito|[+-]?inf|\d+/\d+|[a-zA-Z]+)', texto)
        if match_limite:
            valor = match_limite.group(1).strip()
            if valor in ["infinito", "inf"]:
                valor_limite = "sp.oo"
            elif valor in ["-infinito", "-inf"]:
                valor_limite = "-sp.oo"
            else:
                try:
                    float(valor)
                    valor_limite = valor
                except ValueError:
                    if "/" in valor:
                        numerador, denominador = valor.split("/")
                        valor_limite = f"({numerador.strip()}/{denominador.strip()})"
                    else:
                        valor_limite = valor

    match = re.search(r'f\(x\)\s*=\s*([^\n]+)', problema)
    if match:
        expr = match.group(1)
        expr = limpiar_expresion(expr)
        if not validar_expresion(expr):
            raise ValueError(f"La expresión no es válida: {expr}")
    elif not expr:
        matches = re.search(r'(?:integral|derivada|límite|limite)\s+(?:de|del|la|lo)\s+([^\n]+)', texto, re.IGNORECASE)
        if matches:
            expr_texto = matches.group(1).strip()
            expr_texto = re.split(r'\s+(?:cuando|si|para|donde)', expr_texto)[0]
            expr = limpiar_expresion(expr_texto)
            if not validar_expresion(expr):
                raise ValueError(f"La expresión no es válida: {expr}")

    return tipo_operacion, expr, valor_limite

def formatear_codigo(tipo_operacion, expresion, valor_limite=None):
    if not expresion:
        raise ValueError("No se proporcionó ninguna expresión")

    expr = limpiar_expresion(expresion)
    if not validar_expresion(expr):
        raise ValueError(f"La expresión no es válida: {expr}")

    if tipo_operacion == "derivada":
        return procesar_derivada(expr)
    elif tipo_operacion == "integral":
        return procesar_integral(expr)
    elif tipo_operacion == "limite":
        if valor_limite and not (valor_limite == "sp.oo" or valor_limite == "-sp.oo"):
            try:
                float(valor_limite)
            except ValueError:
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', valor_limite):
                    valor_limite = f"sp.sympify('{valor_limite}')"
        return procesar_limite(expr, valor_limite)
    else:
        raise ValueError("Tipo de operación no soportado")

def procesar_problema(problema):
    try:
        modelo = genai.GenerativeModel('gemini-pro')
        tipo_operacion, expr, valor_limite = extraer_expresion(problema)

        if not tipo_operacion:
            raise ValueError("No se reconoció el tipo de operación.")

        if not expr:
            prompt = f"""
Del siguiente problema matemático:
"{problema}"

Extrae SOLO la expresión matemática usando ** para potencias y * para multiplicaciones explícitas.
Ejemplos:
- x^2 + 2x → x**2 + 2*x
- x^2 sin(x) → x**2*sin(x)
- e^x cos(x) → exp(x)*cos(x)
- ln(x) + x^2 → log(x) + x**2

Respuesta:
"""
            respuesta = modelo.generate_content(prompt)
            expr = respuesta.text.strip()
            expr = limpiar_expresion(expr)
            if not validar_expresion(expr):
                raise ValueError(f"La expresión no es válida: {expr}")

        codigo = formatear_codigo(tipo_operacion, expr, valor_limite)

        explicacion = f"""
1. Tipo de operación: {tipo_operacion}
2. Expresión: {expr}
3. Se usó SymPy con: sp.{'diff' if tipo_operacion == 'derivada' else 'integrate' if tipo_operacion == 'integral' else 'limit'}
{f"4. Límite: x → {valor_limite}" if tipo_operacion == 'limite' else ''}
"""
        return codigo, explicacion

    except Exception as e:
        raise Exception(f"Error al procesar el problema: {str(e)}")
