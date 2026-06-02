# modelo/TablaSimbolos.py
# Módulo: Tabla de símbolos para el análisis semántico
# Responsabilidad: Gestionar el almacenamiento de variables y sus tipos

class TablaSimbolos:
    """
    Tabla de símbolos - Almacena información sobre variables declaradas
    En el patrón MVC, esto es un MODELO porque gestiona los DATOS
    """
    
    def __init__(self):
        """Inicializa una tabla de símbolos vacía"""
        self.simbolos = {}  # Diccionario: nombre -> {type, declared}
    
    def agregar(self, nombre, tipo, declarada=True):
        """
        Agrega una variable a la tabla de símbolos
        
        Parámetros:
            nombre (str): Nombre del identificador
            tipo (str): Tipo de dato (int, float, string, bool, etc.)
            declarada (bool): Si está declarada correctamente
        
        Retorna:
            bool: True si se agregó correctamente
        """
        self.simbolos[nombre] = {'type': tipo, 'declared': declarada}
        return True
    
    def obtener(self, nombre):
        """
        Obtiene la información de una variable
        
        Parámetros:
            nombre (str): Nombre del identificador
        
        Retorna:
            dict: Información de la variable o None si no existe
        """
        return self.simbolos.get(nombre)
    
    def existe(self, nombre):
        """
        Verifica si una variable existe en la tabla
        
        Parámetros:
            nombre (str): Nombre del identificador
        
        Retorna:
            bool: True si existe, False si no
        """
        return nombre in self.simbolos
    
    def obtener_tipo(self, nombre):
        """
        Obtiene el tipo de una variable
        
        Parámetros:
            nombre (str): Nombre del identificador
        
        Retorna:
            str: Tipo de la variable o None si no existe
        """
        var = self.simbolos.get(nombre)
        return var['type'] if var else None
    
    def limpiar(self):
        """Limpia todos los símbolos de la tabla"""
        self.simbolos.clear()
    
    def obtener_todos(self):
        """
        Obtiene todos los símbolos
        
        Retorna:
            dict: Diccionario con todos los símbolos
        """
        return self.simbolos.copy()
    
    def __str__(self):
        """Representación en string de la tabla de símbolos"""
        if not self.simbolos:
            return "Tabla de símbolos vacía"
        
        resultado = "Tabla de Símbolos:\n"
        for nombre, info in self.simbolos.items():
            resultado += f"  {nombre} : {info['type']}\n"
        return resultado