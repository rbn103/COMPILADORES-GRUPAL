# modelo/Semantico.py
# Módulo: Análisis Semántico
# Responsabilidad: Verificar consistencia de tipos y reglas semánticas

from .TablaSimbolos import TablaSimbolos

class SemanticAnalyzer:
    """
    Analizador Semántico - Verifica tipos y consistencia
    
    En el patrón MVC, esto es un MODELO porque contiene la lógica
    de validación de datos semánticos
    """
    
    def __init__(self):
        """Inicializa el analizador semántico"""
        self.symbol_table = TablaSimbolos()
        self.errors = []
        self.warnings = []

    def analyze(self, ast):
        """
        Analiza semánticamente el AST
        
        Parámetros:
            ast (dict): Árbol de Sintaxis Abstracta
        
        Retorna:
            dict: Resultados del análisis (errores, advertencias, tabla)
        """
        self.symbol_table.limpiar()
        self.errors = []
        self.warnings = []
        self.analyze_node(ast)
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'symbolTable': self.symbol_table.obtener_todos()
        }

    def analyze_node(self, node, expected_type=None):
        """
        Analiza un nodo del AST recursivamente
        
        Parámetros:
            node (dict): Nodo del AST
            expected_type (str, opcional): Tipo esperado
        
        Retorna:
            str: Tipo del nodo o None
        """
        if not node:
            return None

        if node.get('type') == 'Programa':
            for child in node.get('children', []):
                self.analyze_node(child)

        elif node.get('type') == 'Declaration':
            declared_type = node['dataType']
            self.symbol_table.agregar(node['identifier'], declared_type)
            if node.get('value'):
                value_type = self.analyze_node(node['value'])
                if value_type and not self.is_type_compatible(declared_type, value_type):
                    self.errors.append(f"Error de tipo: No se puede asignar valor de tipo '{value_type}' a variable '{node['identifier']}' de tipo '{declared_type}'")
            return declared_type

        elif node.get('type') == 'Assignment':
            var_info = self.symbol_table.obtener(node['identifier'])
            if not var_info:
                self.errors.append(f"Error semantico: Variable '{node['identifier']}' no declarada")
                return None
            assign_type = self.analyze_node(node['value'])
            if assign_type and not self.is_type_compatible(var_info['type'], assign_type):
                self.errors.append(f"Error de tipo: Asignacion incompatible. '{node['identifier']}' es de tipo '{var_info['type']}', se intenta asignar '{assign_type}'")
            return var_info['type']

        elif node.get('type') == 'NumberLiteral':
            return 'float' if '.' in node['value'] else 'int'

        elif node.get('type') == 'StringLiteral':
            return 'string'

        elif node.get('type') == 'BooleanLiteral':
            return 'bool'

        elif node.get('type') == 'Identifier':
            info = self.symbol_table.obtener(node['name'])
            if not info:
                self.errors.append(f"Error semantico: Identificador '{node['name']}' no declarado")
                return None
            return info['type']

        elif node.get('type') == 'BinaryOperation':
            left_type = self.analyze_node(node['left'])
            right_type = self.analyze_node(node['right'])
            op = node['operator']

            if op in ['+', '-', '*', '/', '%']:
                if left_type in ('int', 'float') and right_type in ('int', 'float'):
                    return 'float' if left_type == 'float' or right_type == 'float' else 'int'
                self.errors.append(f"Error de tipo: Operador '{op}' requiere operandos numericos. Recibidos: {left_type} y {right_type}")
                return None

            if op in ['==', '!=', '<', '>', '<=', '>=']:
                if left_type and right_type and left_type != right_type:
                    self.warnings.append(f"Advertencia: Comparacion entre tipos diferentes: {left_type} y {right_type}")
                return 'bool'

            if op in ['&&', '||']:
                if left_type != 'bool' or right_type != 'bool':
                    self.errors.append(f"Error de tipo: Operador logico '{op}' requiere operandos booleanos")
                return 'bool'
            return None

        elif node.get('type') == 'IfStatement':
            cond_type = self.analyze_node(node['condition'])
            if cond_type != 'bool':
                self.warnings.append(f"Advertencia: La condicion del 'if' deberia ser booleana, se recibio: {cond_type}")
            if node.get('thenBranch'):
                self.analyze_node(node['thenBranch'])
            if node.get('elseBranch'):
                self.analyze_node(node['elseBranch'])

        elif node.get('type') == 'Block':
            for stmt in node.get('statements', []):
                self.analyze_node(stmt)

        return None

    def is_type_compatible(self, declared, assigned):
        """
        Verifica si dos tipos son compatibles
        
        Parámetros:
            declared (str): Tipo declarado
            assigned (str): Tipo asignado
        
        Retorna:
            bool: True si son compatibles
        """
        if declared == assigned:
            return True
        if declared == 'float' and assigned == 'int':
            return True
        if declared == 'double' and assigned in ('int', 'float'):
            return True
        return False