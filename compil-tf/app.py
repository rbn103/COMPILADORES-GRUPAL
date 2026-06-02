# app.py - Punto de entrada de la aplicación MVC
# Responsabilidad: Inicializar el servidor Flask y definir las rutas

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Importar el controlador
from controllers.compilador_controller import CompiladorController

# Crear la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='views')
CORS(app)

# Instanciar el controlador (única instancia)
compilador = CompiladorController()


# ============================================================
# RUTAS DE LA API
# ============================================================

@app.route('/api/compilar', methods=['POST'])
def compilar():
    """
    Endpoint principal de compilacion
    Recibe código fuente y retorna los resultados del compilador
    """
    data = request.get_json()
    codigo = data.get('codigo', '')
    
    # Delegar la lógica al controlador
    resultado = compilador.compilar(codigo)
    
    return jsonify(resultado)


@app.route('/api/health', methods=['GET'])
def health():
    """
    Endpoint para verificar el estado del servidor
    """
    return jsonify(compilador.health_check())


@app.route('/', methods=['GET'])
def servir_index():
    """
    Sirve el archivo index.html desde la carpeta views
    """
    return send_from_directory('views', 'index.html')


# ============================================================
# INICIO DEL SERVIDOR
# ============================================================

if __name__ == '__main__':
    # Ejecutar el servidor en modo debug
    # El frontend se sirve en la misma URL que el backend
    print("=" * 50)
    print("Servidor Flask iniciado")
    print("Modo MVC activado")
    print(f"Modelos: modelo/")
    print(f"Controladores: controllers/")
    print(f"Vistas: views/")
    print("=" * 50)
    print(f"Frontend disponible en: http://localhost:5000/")
    print(f"API disponible en: http://localhost:5000/api/health")
    print("=" * 50)
    app.run(debug=True, port=5000)