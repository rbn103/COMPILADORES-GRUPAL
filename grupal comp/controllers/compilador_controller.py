# controllers/compilador_controller.py
# Módulo: Controlador del Compilador
# Responsabilidad: Coordinar los modelos y preparar respuestas

import re
from modelo.Lexico import lexer_analisis
from modelo.Sintactico import ParserATS
from modelo.Semantico import SemanticAnalyzer
from modelo.Tokens import TOKEN_TYPES

class CompiladorController:
    """
    Controlador del Compilador - Orquesta el flujo de compilación
    
    En el patrón MVC, esto es un CONTROLADOR porque:
    - Recibe peticiones (código fuente)
    - Coordina los modelos (Léxico, Sintáctico, Semántico)
    - Prepara la respuesta (datos para la vista)
    """
    
    def __init__(self):
        """Inicializa el controlador"""
        pass
    
    def compilar(self, codigo):
        """
        Ejecuta el proceso completo de compilación
        
        Parámetros:
            codigo (str): Código fuente a compilar
        
        Retorna:
            dict: Resultados de la compilación (tokens, AST, semántica, vulnerabilidades)
        """
        # ============================================================
        # FASE 1: ANÁLISIS LÉXICO
        # ============================================================
        tokens = lexer_analisis(codigo)
        
        # ============================================================
        # FASE 2: ANÁLISIS SINTÁCTICO
        # ============================================================
        parser = ParserATS(tokens)
        ast = parser.parse()
        
        # ============================================================
        # FASE 3: ANÁLISIS SEMÁNTICO
        # ============================================================
        semantic = SemanticAnalyzer()
        semantic_result = semantic.analyze(ast)
        
        # ============================================================
        # FASE 4: EXTRACCIÓN DE VULNERABILIDADES
        # ============================================================
        vulnerabilidades = self.extract_vulnerabilities(tokens, codigo)
        
        # ============================================================
        # FASE 5: GENERACIÓN DE ACCIONES Y RESUMEN
        # ============================================================
        acciones_unicas = self.generar_acciones_unicas(vulnerabilidades)
        resumen = self.generar_resumen(vulnerabilidades, semantic_result)
        
        return {
            'tokens': tokens,
            'ast': ast,
            'semanticResult': semantic_result,
            'vulnerabilidades': vulnerabilidades,
            'resumen': resumen,
            'accionesUnicas': acciones_unicas
        }
    
    def extract_vulnerabilities(self, tokens, codigo):
        """
        Extrae vulnerabilidades del código basado en patrones CVE
        
        Parámetros:
            tokens (list): Lista de tokens
            codigo (str): Código fuente original
        
        Retorna:
            list: Lista de vulnerabilidades encontradas
        """
        vulnerabilidades = []
        cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}', re.IGNORECASE)
        i = 0

        while i < len(tokens):
            token = tokens[i]
            cve_match = cve_pattern.search(token['lexema'])
            if cve_match:
                cve_id = cve_match.group(0)
                cvss_value = 5.0

                # Buscar CVSS en tokens cercanos
                for j in range(max(0, i - 5), min(len(tokens), i + 8)):
                    if tokens[j]['tipo'] == TOKEN_TYPES['NUMERO']:
                        try:
                            num = float(tokens[j]['lexema'])
                            if 0 <= num <= 10:
                                cvss_value = num
                                break
                        except ValueError:
                            pass

                # Determinar nivel de riesgo
                if cvss_value >= 9.0:
                    nivel = "critica"
                    tiempo_respuesta = "inmediato (< 4h)"
                    acciones = ["Aislar sistema inmediatamente", "Aplicar parche de emergencia", "Notificar a CISO"]
                elif cvss_value >= 7.0:
                    nivel = "alta"
                    tiempo_respuesta = "24 horas"
                    acciones = ["Programar parche en 24h", "Monitoreo intensivo", "Revision de logs"]
                elif cvss_value >= 4.0:
                    nivel = "media"
                    tiempo_respuesta = "7 dias"
                    acciones = ["Planificar actualizacion", "Documentar vulnerabilidad", "Evaluar impacto"]
                else:
                    nivel = "baja"
                    tiempo_respuesta = "30 dias"
                    acciones = ["Registrar en backlog", "Revisar en proximo ciclo", "Sin accion inmediata"]

                vulnerabilidades.append({
                    'id': cve_id,
                    'cvss': cvss_value,
                    'nivel_riesgo': nivel,
                    'tiempo_respuesta': tiempo_respuesta,
                    'acciones': acciones
                })
            i += 1

        return vulnerabilidades
    
    def generar_acciones_unicas(self, vulnerabilidades):
        """
        Genera una lista única de acciones de mitigación
        
        Parámetros:
            vulnerabilidades (list): Lista de vulnerabilidades
        
        Retorna:
            list: Lista de acciones únicas
        """
        todas_acciones = []
        for v in vulnerabilidades:
            todas_acciones.extend(v['acciones'])
        return list(set(todas_acciones))
    
    def generar_resumen(self, vulnerabilidades, semantic_result):
        """
        Genera un resumen ejecutivo de la compilación
        
        Parámetros:
            vulnerabilidades (list): Lista de vulnerabilidades
            semantic_result (dict): Resultados del análisis semántico
        
        Retorna:
            dict: Resumen ejecutivo
        """
        criticas = len([v for v in vulnerabilidades if v['nivel_riesgo'] == 'critica'])
        
        return {
            'total_vulnerabilidades': len(vulnerabilidades),
            'criticas': criticas,
            'errores_semanticos': len(semantic_result['errors']),
            'advertencias_semanticas': len(semantic_result['warnings']),
            'recomendacion_general': "Ejecutar acciones de mitigacion priorizadas URGENTE" if criticas > 0 else "Monitoreo regular y planificacion"
        }
    
    def health_check(self):
        """
        Verifica que el controlador esté funcionando
        
        Retorna:
            dict: Estado del controlador
        """
        return {'status': 'ok', 'message': 'Compilador funcionando correctamente'}