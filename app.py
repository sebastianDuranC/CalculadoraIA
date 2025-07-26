from flask import Flask, render_template, request #para crear el servidor web y manejar las peticiones HTTP
from gemini_handler import procesar_problema #para procesar los problemas matemáticos
import sympy as sp #para realizar cálculos matemáticos
import sys #para manejar la salida estándar
from io import StringIO #para manejar la salida estándar
import re #para procesar y limpiar las expresiones matemáticas

app = Flask(__name__)

def a_latex(expr):
    """
    Convierte expresiones de Python a formato LaTeX para MathJax.
    
    Args:
        expr (str): Expresión en formato Python/SymPy
        
    Returns:
        str: Expresión en formato LaTeX
    """
    # Reemplazos básicos
    expr = expr.replace('**', '^')
    expr = expr.replace('*', r'\cdot ')
    
    # Reemplazos para constantes
    expr = expr.replace('e', r'\mathrm{e}')
    expr = expr.replace('pi', r'\pi')
    expr = expr.replace('oo', r'\infty')
    
    # Reemplazos para funciones trigonométricas
    expr = expr.replace('sin', r'\sin')
    expr = expr.replace('cos', r'\cos')
    expr = expr.replace('tan', r'\tan')
    expr = expr.replace('asin', r'\arcsin')
    expr = expr.replace('acos', r'\arccos')
    expr = expr.replace('atan', r'\arctan')
    
    # Reemplazos para otras funciones
    expr = expr.replace('exp', r'\exp')
    expr = expr.replace('log', r'\log')
    expr = expr.replace('sqrt', r'\sqrt')
    expr = expr.replace('Abs', r'\left|')
    
    # Formatear funciones
    expr = re.sub(r'\\([a-z]+)\(([^)]+)\)', r'\\\1{\2}', expr)
    
    # Formatear valor absoluto
    expr = re.sub(r'\\left\|([^|]+)\\right\|', r'\\left|\1\\right|', expr)
    
    return expr

def ejecutar_codigo_seguro(codigo):
    """
    Ejecuta código Python generado de forma segura y captura la salida.
    
    Args:
        codigo (str): Código Python a ejecutar
        
    Returns:
        tuple: (exito, salida)
            - exito: Booleano indicando si la ejecución fue exitosa
            - salida: Salida del código o mensaje de error
    """
    try:
        # Inicializar constantes y funciones matemáticas
        namespace = {
            'sp': sp,
            'x': sp.Symbol('x'),
            'expr': None,
            'resultado': None,
            'e': sp.E,        # Constante e
            'pi': sp.pi,      # Constante pi
            'oo': sp.oo,      # Infinito
            'sin': sp.sin,    # Función seno
            'cos': sp.cos,    # Función coseno
            'tan': sp.tan,    # Función tangente
            'exp': sp.exp,    # Función exponencial
            'log': sp.log,    # Función logaritmo natural
            'sqrt': sp.sqrt,  # Función raíz cuadrada
            'abs': sp.Abs,    # Función valor absoluto
            'asin': sp.asin,  # Arcoseno
            'acos': sp.acos,  # Arcocoseno
            'atan': sp.atan   # Arcotangente
        }

        stdout = StringIO()
        sys.stdout = stdout

        try:
            exec(codigo, namespace)
            salida = stdout.getvalue()
            return True, salida

        finally:
            sys.stdout = sys.__stdout__

    except Exception as e:
        return False, f"Error al ejecutar el código: {str(e)}"

def convertir_a_latex_desde_salida(texto):
    """
    Convierte la salida del código a formato LaTeX para MathJax.
    
    Args:
        texto (str): Salida del código Python
        
    Returns:
        str: Texto formateado en LaTeX
    """
    try:
        # Patrón para derivadas e integrales
        match = re.search(r"La (.+?) de (.+?) es: (.+)", texto)
        if match:
            operacion = match.group(1)
            expr = match.group(2)
            resultado = match.group(3)

            expr_latex = a_latex(expr)
            resultado_latex = a_latex(resultado)

            return r"La {} de \( {} \) es \( {} \)".format(operacion, expr_latex, resultado_latex)

        # Patrón para límites
        match_limite = re.search(r"El límite de (.+?) cuando x → (.+?) es: (.+)", texto)
        if match_limite:
            expr = match_limite.group(1)
            valor = match_limite.group(2)
            resultado = match_limite.group(3)

            expr_latex = a_latex(expr)
            valor_latex = a_latex(valor)
            resultado_latex = a_latex(resultado)

            return r"El límite de \( {} \) cuando \( x \to {} \) es \( {} \)".format(expr_latex, valor_latex, resultado_latex)

        return texto

    except:
        return texto

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal de la aplicación.
    Maneja las solicitudes GET y POST para resolver problemas matemáticos.
    """
    resultado = None
    codigo_generado = None
    pasos = None
    error = None

    if request.method == 'POST':
        problema = request.form.get('problema')

        try:
            codigo_generado, pasos = procesar_problema(problema)
            exito, output = ejecutar_codigo_seguro(codigo_generado)

            if not exito:
                error = output
            else:
                resultado = convertir_a_latex_desde_salida(output.strip())

        except Exception as e:
            error = f"Error al procesar la solicitud: {str(e)}"

    return render_template('index.html',
                           resultado=resultado,
                           codigo_generado=codigo_generado,
                           pasos=pasos,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)