# Calculadora Matemática con Gemini AI

Una aplicación web que utiliza la API de Gemini para resolver problemas matemáticos, incluyendo derivadas, integrales y límites.

## Características

- Interfaz web intuitiva
- Soporte para problemas matemáticos
- Integración con la API de Gemini
- Cálculos simbólicos usando SymPy
- Procesamiento de expresiones matemáticas

## Estructura del Proyecto

```
ProyectoWebPython/
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   │   └── styles.css       # Estilos de la aplicación
│   └── js/
│       └── script.js        # Funcionalidad del frontend
│
├── templates/               # Plantillas HTML
│   └── index.html          # Página principal de la aplicación
│
├── .env                    # Variables de entorno (API keys)
├── .gitignore             # Archivos ignorados por Git
├── app.py                 # Aplicación principal Flask
├── gemini_handler.py      # Manejador de la API de Gemini
├── procesador_matematico.py # Procesamiento de expresiones matemáticas
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Documentación del proyecto
```

### Explicación de los Componentes

- **static/**: Contiene todos los archivos estáticos necesarios para el 

- **templates/**: Contiene las plantillas HTML
  - `index.html`: La página principal con el formulario y los resultados

- **app.py**: El corazón de la aplicación
  - Configura el servidor Flask
  - Maneja las rutas y peticiones HTTP
  - Procesa los resultados matemáticos

- **gemini_handler.py**: Gestiona la comunicación con Gemini AI
  - Extrae expresiones matemáticas del texto
  - Genera código Python para los cálculos
  - Maneja errores y validaciones

- **procesador_matematico.py**: Procesa expresiones matemáticas
  - Limpia y valida expresiones
  - Convierte notación matemática a código Python
  - Maneja funciones especiales (trigonométricas, exponenciales, etc.)

## __pycache__

La carpeta `__pycache__` es creada automáticamente por Python para almacenar archivos compilados (bytecode) de los módulos Python. Esto mejora el rendimiento al evitar recompilar el código cada vez que se ejecuta.

  - Acelera la carga de módulos Python
  - Reduce el tiempo de inicio de la aplicación
  - Es una optimización automática de Python

## Requisitos

- Python 3.8+
- Flask
- python-dotenv
- google-generativeai
- sympy

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear archivo `.env` con tu API key de Gemini:
   ```
   GOOGLE_API_KEY=tu_api_key_aquí
   ```

## Uso

1. Iniciar el servidor: `python app.py`
2. Abrir el navegador en `http://localhost:5000`
3. Ingresar el problema matemático
4. Obtener la solución paso a paso

## Ejemplos de Uso

- Derivadas: "Calcular derivada de f(x) = x^3 + 2*sin(x)"
- Integrales: "Calcular integral de f(x) = e^x * cos(x)"
- Límites: "Calcular límite de f(x) = (x^2 - 1)/(x - 1) cuando x tiende a 1"

## Archivo ejecutable
- Se instala pyinstaller para crear un ejecutable que contenga todo lo necesario para usar este proyecto, con el siguiente comando:
```
pip install pyinstaller
```
Luego de esto usamos el siguiente comando:
```
pyinstaller --name CalculateAI --onefile --add-data "templates;templates" --add-data "static;static" --hidden-import=flask --hidden-import=sympy --hidden-import=google.generativeai --hidden-import=dotenv app.py
```
Este comando de PyInstaller crea un solo archivo ejecutable (CalculateAI) a partir de app.py, incluyendo:

Los directorios templates y static (con su contenido) dentro del ejecutable.
Las librerías flask, sympy, google.generativeai y dotenv, forzándolas a ser incluidas aunque PyInstaller no las detecte automáticamente.