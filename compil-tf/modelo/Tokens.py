# modelo/Tokens.py
# Módulo: Definición de tipos de tokens y palabras reservadas
# Responsabilidad: Centralizar todas las constantes relacionadas con tokens

# ============================================================
# TOKEN TYPES - DEFINICIÓN DE TIPOS DE TOKENS
# ============================================================
TOKEN_TYPES = {
    'PALABRA_RESERVADA': 'palabra_reservada',
    'IDENTIFICADOR': 'identificador',
    'NUMERO': 'numero',
    'OPERADOR': 'operador',
    'STRING': 'string',
    'DELIMITADOR': 'delimitador'
}

# ============================================================
# PALABRAS RESERVADAS DEL LENGUAJE
# ============================================================
RESERVED_WORDS = set([
    # Tipos de datos
    "int", "float", "double", "string", "bool", "boolean", "char", "void",
    # Palabras de control
    "if", "else", "while", "for", "return", "break", "continue", "switch", 
    "case", "default", "true", "false", "null", "undefined",
    # Contexto vulnerabilidades
    "vulnerabilidad", "mitigacion", "reporte", "seguridad", "riesgo", 
    "amenaza", "parche", "ataque", "brecha", "critica", "alta", "media", 
    "baja", "critico"
])

# ============================================================
# OPERADORES VÁLIDOS
# ============================================================
OPERATORS = set(["=", "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "&", "|"])

# ============================================================
# DELIMITADORES VÁLIDOS
# ============================================================
DELIMITERS = set(["{", "}", "[", "]", "(", ")", ";", ":", ","])