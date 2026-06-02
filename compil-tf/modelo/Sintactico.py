# modelo/Sintactico.py
# Módulo: Análisis Sintáctico (Parser)
# Responsabilidad: Construir el Árbol de Sintaxis Abstracta (ATS)

from .Tokens import TOKEN_TYPES

class ParserATS:
    """
    Analizador Sintáctico - Construye el ATS a partir de tokens
    
    En el patrón MVC, esto es un MODELO porque procesa los datos
    y genera una estructura (el AST)
    """
    
    def __init__(self, tokens):
        """
        Inicializa el parser con una lista de tokens
        
        Parámetros:
            tokens (list): Lista de tokens del análisis léxico
        """
        self.tokens = tokens
        self.pos = 0
        self.ast = {'type': 'Programa', 'children': []}

    def current(self):
        """
        Obtiene el token actual
        
        Retorna:
            dict: Token actual o None si no hay más
        """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        """
        Consume el token actual si coincide con el tipo esperado
        
        Parámetros:
            expected_type (str, opcional): Tipo de token esperado
        
        Retorna:
            dict: Token consumido o None si no coincide
        """
        token = self.current()
        if token and (expected_type is None or token['tipo'] == expected_type):
            self.pos += 1
            return token
        return None

    def parse(self):
        """
        Inicia el análisis sintáctico
        
        Retorna:
            dict: Árbol de Sintaxis Abstracta (ATS)
        """
        while self.current():
            stmt = self.parse_statement()
            if stmt:
                self.ast['children'].append(stmt)
            else:
                break
        return self.ast

    def parse_statement(self):
        """
        Analiza una sentencia
        
        Retorna:
            dict: Nodo del AST representando la sentencia
        """
        token = self.current()
        if not token:
            return None

        # Declaracion de variable
        if token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and token['lexema'].lower() in ["int", "float", "double", "string", "bool", "boolean", "char", "void"]:
            return self.parse_declaration()

        # Asignacion
        if token['tipo'] == TOKEN_TYPES['IDENTIFICADOR']:
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token['tipo'] == TOKEN_TYPES['OPERADOR'] and next_token['lexema'] == "=":
                return self.parse_assignment()

        # If statement
        if token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and token['lexema'].lower() == "if":
            return self.parse_if()

        # While statement
        if token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and token['lexema'].lower() == "while":
            return self.parse_while()

        # Return statement
        if token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and token['lexema'].lower() == "return":
            return self.parse_return()

        self.pos += 1
        return {'type': 'Unknown', 'value': token['lexema']}

    def parse_declaration(self):
        """
        Analiza una declaración de variable
        
        Retorna:
            dict: Nodo Declaration del AST
        """
        type_token = self.consume(TOKEN_TYPES['PALABRA_RESERVADA'])
        id_token = self.consume(TOKEN_TYPES['IDENTIFICADOR'])
        if not id_token:
            return None

        declaration = {
            'type': 'Declaration',
            'dataType': type_token['lexema'],
            'identifier': id_token['lexema'],
            'value': None
        }

        assign_op = self.consume(TOKEN_TYPES['OPERADOR'])
        if assign_op and assign_op['lexema'] == "=":
            expr = self.parse_expression()
            declaration['value'] = expr

        self.consume(TOKEN_TYPES['DELIMITADOR'])
        return declaration

    def parse_assignment(self):
        """
        Analiza una asignación de variable
        
        Retorna:
            dict: Nodo Assignment del AST
        """
        id_token = self.consume(TOKEN_TYPES['IDENTIFICADOR'])
        self.consume(TOKEN_TYPES['OPERADOR'])
        expr = self.parse_expression()
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        return {
            'type': 'Assignment',
            'identifier': id_token['lexema'],
            'value': expr
        }

    def parse_expression(self):
        """
        Analiza una expresión (operaciones binarias)
        
        Retorna:
            dict: Nodo de expresión del AST
        """
        left = self.parse_primary()
        token = self.current()
        if token and token['tipo'] == TOKEN_TYPES['OPERADOR']:
            op = self.consume(TOKEN_TYPES['OPERADOR'])
            right = self.parse_primary()
            return {
                'type': 'BinaryOperation',
                'operator': op['lexema'],
                'left': left,
                'right': right
            }
        return left

    def parse_primary(self):
        """
        Analiza un elemento primario (literal, identificador, etc.)
        
        Retorna:
            dict: Nodo primario del AST
        """
        token = self.current()
        if not token:
            return None

        if token['tipo'] == TOKEN_TYPES['NUMERO']:
            self.pos += 1
            return {'type': 'NumberLiteral', 'value': token['lexema']}
        if token['tipo'] == TOKEN_TYPES['STRING']:
            self.pos += 1
            return {'type': 'StringLiteral', 'value': token['lexema']}
        if token['tipo'] == TOKEN_TYPES['IDENTIFICADOR']:
            self.pos += 1
            return {'type': 'Identifier', 'name': token['lexema']}
        if token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and token['lexema'] in ("true", "false"):
            self.pos += 1
            return {'type': 'BooleanLiteral', 'value': token['lexema']}

        return None

    def parse_if(self):
        """
        Analiza una sentencia if-else
        
        Retorna:
            dict: Nodo IfStatement del AST
        """
        self.consume(TOKEN_TYPES['PALABRA_RESERVADA'])
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        condition = self.parse_expression()
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        then_branch = self.parse_block()
        else_branch = None

        next_token = self.current()
        if next_token and next_token['tipo'] == TOKEN_TYPES['PALABRA_RESERVADA'] and next_token['lexema'].lower() == "else":
            self.consume(TOKEN_TYPES['PALABRA_RESERVADA'])
            else_branch = self.parse_block()

        return {'type': 'IfStatement', 'condition': condition, 'thenBranch': then_branch, 'elseBranch': else_branch}

    def parse_while(self):
        """
        Analiza una sentencia while
        
        Retorna:
            dict: Nodo WhileStatement del AST
        """
        self.consume(TOKEN_TYPES['PALABRA_RESERVADA'])
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        condition = self.parse_expression()
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        body = self.parse_block()
        return {'type': 'WhileStatement', 'condition': condition, 'body': body}

    def parse_return(self):
        """
        Analiza una sentencia return
        
        Retorna:
            dict: Nodo ReturnStatement del AST
        """
        self.consume(TOKEN_TYPES['PALABRA_RESERVADA'])
        value = self.parse_expression()
        self.consume(TOKEN_TYPES['DELIMITADOR'])
        return {'type': 'ReturnStatement', 'value': value}

    def parse_block(self):
        """
        Analiza un bloque de código entre llaves
        
        Retorna:
            dict: Nodo Block del AST
        """
        block = {'type': 'Block', 'statements': []}
        if self.current() and self.current()['tipo'] == TOKEN_TYPES['DELIMITADOR'] and self.current()['lexema'] == "{":
            self.consume(TOKEN_TYPES['DELIMITADOR'])
            while self.current() and not (self.current()['tipo'] == TOKEN_TYPES['DELIMITADOR'] and self.current()['lexema'] == "}"):
                stmt = self.parse_statement()
                if stmt:
                    block['statements'].append(stmt)
                else:
                    break
            self.consume(TOKEN_TYPES['DELIMITADOR'])
        else:
            stmt = self.parse_statement()
            if stmt:
                block['statements'].append(stmt)
        return block