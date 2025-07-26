import sympy as sp
import re

def limpiar_expresion(expr):
    """
    Limpia y formatea una expresión matemática para asegurar que sea válida en Python/SymPy.
    
    Args:
        expr (str): Expresión matemática a limpiar
        
    Returns:
        str: Expresión limpia y válida para SymPy
    """
    # Eliminar espacios
    expr = expr.replace(' ', '')
    
    # Convertir ^ a **
    expr = expr.replace('^', '**')
    
    # Convertir funciones trigonométricas a formato SymPy
    expr = re.sub(r'sin\(', 'sin(', expr)
    expr = re.sub(r'cos\(', 'cos(', expr)
    expr = re.sub(r'tan\(', 'tan(', expr)
    
    # Manejar exponencial e^x apropiadamente
    expr = re.sub(r'e\^([^(])', r'exp(\1)', expr)  # e^x -> exp(x)
    expr = re.sub(r'e\^(\([^)]+\))', r'exp\1', expr)  # e^(x+1) -> exp(x+1)
    expr = re.sub(r'e\*\*([^(])', r'exp(\1)', expr)  # e**x -> exp(x)
    expr = re.sub(r'e\*\*(\([^)]+\))', r'exp\1', expr)  # e**(x+1) -> exp(x+1)
    
    # Convertir otras funciones a formato SymPy
    expr = re.sub(r'exp\(', 'exp(', expr)
    expr = re.sub(r'log\(', 'log(', expr)
    
    # Asegurar multiplicaciones explícitas solo entre números y variables
    expr = re.sub(r'(\d+)([a-z])', r'\1*\2', expr)  # 2x → 2*x
    expr = re.sub(r'\)([a-z])', r')*\1', expr)      # )x → )*x
    expr = re.sub(r'(\d+)\(', r'\1*(', expr)        # 2( → 2*(
    
    # Convertir constantes matemáticas
    expr = re.sub(r'pi', 'pi', expr)
    expr = re.sub(r'^e$', 'E', expr)  # Para la constante e sola
    
    return expr

def validar_expresion(expr):
    """
    Valida una expresión matemática usando SymPy.
    
    Args:
        expr (str): Expresión matemática a validar
        
    Returns:
        bool: True si la expresión es válida, False en caso contrario
    """
    try:
        # Intentar evaluar la expresión
        expr = expr.replace('sp.', '')  # Remover el prefijo sp. para la validación
        sp.sympify(expr)
        return True
    except Exception as e:
        print(f"Error de validación: {str(e)}")
        return False

def formatear_expresion(expr):
    """
    Formatea una expresión matemática para que sea más legible.
    
    Args:
        expr (str): Expresión matemática a formatear
        
    Returns:
        str: Expresión formateada y legible
    """
    # Asegurar que las funciones trigonométricas estén en minúsculas
    expr = re.sub(r'(?i)sin', 'sin', expr)
    expr = re.sub(r'(?i)cos', 'cos', expr)
    expr = re.sub(r'(?i)tan', 'tan', expr)
    expr = re.sub(r'(?i)asin', 'asin', expr)
    expr = re.sub(r'(?i)acos', 'acos', expr)
    expr = re.sub(r'(?i)atan', 'atan', expr)
    
    # Asegurar que las constantes estén en minúsculas
    expr = re.sub(r'(?i)pi', 'pi', expr)
    expr = re.sub(r'(?i)e', 'e', expr)
    
    return expr

def procesar_limite(expr, valor_limite):
    """
    Procesa una expresión para calcular su límite.
    
    Args:
        expr (str): Expresión matemática
        valor_limite (str): Valor al que tiende x
        
    Returns:
        str: Código Python para calcular el límite
    """
    # Manejar casos especiales
    if valor_limite is None:
        valor_limite = "oo"
    elif valor_limite == "sp.oo":
        valor_limite_display = "oo"
    elif valor_limite == "-sp.oo":
        valor_limite_display = "-oo"
    else:
        # Intentar convertir a número para validación
        try:
            float(valor_limite)
            valor_limite_display = valor_limite
        except (ValueError, TypeError):
            # Si no es un número, usar como está
            valor_limite_display = valor_limite
    
    # Display value for printing
    display_value = valor_limite_display if 'valor_limite_display' in locals() else valor_limite
    
    return f"""
import sympy as sp
x = sp.symbols('x')
expr = {expr}
resultado = sp.limit(expr, x, {valor_limite})
print(f"El límite de {{expr}} cuando x → {display_value} es: {{resultado}}")
"""

def procesar_derivada(expr):
    """
    Procesa una expresión para calcular su derivada.
    
    Args:
        expr (str): Expresión matemática
        
    Returns:
        str: Código Python para calcular la derivada
    """
    return f"""
import sympy as sp
x = sp.symbols('x')
expr = {expr}
resultado = sp.diff(expr, x)
print(f"La derivada de {{expr}} es: {{resultado}}")
"""

def procesar_integral(expr):
    """
    Procesa una expresión para calcular su integral.
    
    Args:
        expr (str): Expresión matemática
        
    Returns:
        str: Código Python para calcular la integral
    """
    return f"""
import sympy as sp
x = sp.symbols('x')
expr = {expr}
resultado = sp.integrate(expr, x)
print(f"La integral de {{expr}} es: {{resultado}}")
"""