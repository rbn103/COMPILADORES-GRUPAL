# modelo/Lexico.py
# Módulo: Análisis Léxico
# Responsabilidad: Convertir código fuente en tokens

from .Tokens import TOKEN_TYPES, RESERVED_WORDS, OPERATORS, DELIMITERS

def is_dot_delimiter(codigo, pos):
    """
    Verifica si un punto es delimitador (final de oracion)
    
    Parámetros:
        codigo (str): Código fuente completo
        pos (int): Posición actual en el código
    
    Retorna:
        bool: True si el punto es delimitador, False si es parte de un número
    """
    if codigo[pos] != '.':
        return False
    if pos + 1 >= len(codigo):
        return True
    next_char = codigo[pos + 1]
    return next_char in (' ', '\n', '\r', '\t')


def lexer_analisis(codigo):
    """
    Analisis lexico - genera lista de tokens
    
    Parámetros:
        codigo (str): Código fuente a analizar
    
    Retorna:
        list: Lista de diccionarios con tokens (tipo, lexema, linea, columna)
    """
    tokens = []
    line = 1
    col = 1
    i = 0
    length = len(codigo)

    while i < length:
        ch = codigo[i]

        # Espacios en blanco
        if ch.isspace():
            if ch == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        # Comentarios de linea //
        if ch == '/' and i + 1 < length and codigo[i + 1] == '/':
            while i < length and codigo[i] != '\n':
                i += 1
            continue

        # Comentarios multilinea /* */
        if ch == '/' and i + 1 < length and codigo[i + 1] == '*':
            i += 2
            while i < length and not (codigo[i] == '*' and i + 1 < length and codigo[i + 1] == '/'):
                if codigo[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
            if i < length:
                i += 2
            continue

        # Strings con comillas dobles
        if ch == '"':
            start = i
            i += 1
            col += 1
            str_content = '"'
            while i < length and codigo[i] != '"':
                if codigo[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                str_content += codigo[i]
                i += 1
            if i < length and codigo[i] == '"':
                str_content += '"'
                i += 1
                col += 1
            tokens.append({
                'tipo': TOKEN_TYPES['STRING'],
                'lexema': str_content,
                'linea': line,
                'columna': col - len(str_content)
            })
            continue

        # Strings con comillas simples
        if ch == "'":
            start = i
            i += 1
            col += 1
            str_content = "'"
            while i < length and codigo[i] != "'":
                if codigo[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                str_content += codigo[i]
                i += 1
            if i < length and codigo[i] == "'":
                str_content += "'"
                i += 1
                col += 1
            tokens.append({
                'tipo': TOKEN_TYPES['STRING'],
                'lexema': str_content,
                'linea': line,
                'columna': col - len(str_content)
            })
            continue

        # Numeros
        if ch.isdigit():
            start = i
            lex = ""
            has_decimal = False
            while i < length and (codigo[i].isdigit() or (codigo[i] == '.' and not has_decimal and i + 1 < length and codigo[i + 1].isdigit())):
                if codigo[i] == '.':
                    has_decimal = True
                lex += codigo[i]
                i += 1
            tokens.append({
                'tipo': TOKEN_TYPES['NUMERO'],
                'lexema': lex,
                'linea': line,
                'columna': col
            })
            col += len(lex)
            continue

        # Identificadores y palabras reservadas
        if ch.isalpha() or ch == '_':
            start = i
            lex = ""
            while i < length and (codigo[i].isalnum() or codigo[i] == '_'):
                lex += codigo[i]
                i += 1
            tipo = TOKEN_TYPES['PALABRA_RESERVADA'] if lex.lower() in RESERVED_WORDS else TOKEN_TYPES['IDENTIFICADOR']
            tokens.append({
                'tipo': tipo,
                'lexema': lex,
                'linea': line,
                'columna': col
            })
            col += len(lex)
            continue

        # Operadores multicaracter
        op_matched = False
        for op in ["==", "!=", "<=", ">=", "&&", "||", "=", "+", "-", "*", "/", "%", "<", ">", "!", "&", "|"]:
            if codigo[i:i + len(op)] == op:
                tokens.append({
                    'tipo': TOKEN_TYPES['OPERADOR'],
                    'lexema': op,
                    'linea': line,
                    'columna': col
                })
                i += len(op)
                col += len(op)
                op_matched = True
                break
        if op_matched:
            continue

        # Punto como delimitador
        if is_dot_delimiter(codigo, i):
            tokens.append({
                'tipo': TOKEN_TYPES['DELIMITADOR'],
                'lexema': '.',
                'linea': line,
                'columna': col
            })
            i += 1
            col += 1
            continue

        # Otros delimitadores
        if ch in DELIMITERS:
            tokens.append({
                'tipo': TOKEN_TYPES['DELIMITADOR'],
                'lexema': ch,
                'linea': line,
                'columna': col
            })
            i += 1
            col += 1
            continue

        # Caracter no reconocido
        i += 1
        col += 1

    return tokens