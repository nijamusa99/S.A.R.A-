from datetime import datetime
from typing import Dict, Any, Optional
from ..domain.value_objects import Genero

class InputNormalizer:
    """
    Normaliza datos de entrada desde diferentes fuentes (usuario manual, API, etc.)
    """
    
    @staticmethod
    def normalize(raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte cualquier entrada a un formato estándar.
        """
        # 1. Normalizar obra
        obra_raw = raw_input.get('obra', {})
        obra = {
            'nombre': obra_raw.get('nombre', 'Obra sin nombre'),
            'genero': InputNormalizer._normalize_genero(obra_raw.get('genero')),
            'popularidad_elenco': float(obra_raw.get('popularidad_elenco', 5.0)),
            'tiene_premios': bool(obra_raw.get('tiene_premios', False))
        }
        
        # 2. Normalizar temporada
        temp_raw = raw_input.get('temporada', {})
        fecha = InputNormalizer._normalize_fecha(temp_raw.get('fecha_funcion'))
        temporada = {
            'total_funciones_programadas': int(temp_raw.get('total_funciones_programadas', 10)),
            'numero_funcion_actual': int(temp_raw.get('numero_funcion_actual', 1)),
            'fecha_funcion': fecha.isoformat() if fecha else datetime.now().isoformat()
        }
        
        # 3. Normalizar contexto (ventas)
        ctx_raw = raw_input.get('contexto_actual', {})
        contexto = {
            'boletas_vendidas_hoy': int(ctx_raw.get('boletas_vendidas_hoy', 0)),
            'aforo_total_sala': int(ctx_raw.get('aforo_total_sala', 100))
        }
        
        return {
            'obra': obra,
            'temporada': temporada,
            'contexto_actual': contexto
        }
    
    @staticmethod
    def _normalize_genero(value: Any) -> str:
        """Convierte cualquier string a un Genero válido"""
        if value is None:
            return 'Drama'
        
        # Si es string, lo limpiamos y mapeamos
        if isinstance(value, str):
            genero_map = {
                'comedia': 'Comedia',
                'comedy': 'Comedia',
                'drama': 'Drama',
                'musical': 'Musical',
                'musicales': 'Musical',
                'infantil': 'Infantil',
                'kids': 'Infantil',
                'standup': 'Stand-up',
                'stand up': 'Stand-up',
                'stand-up': 'Stand-up',
                'clasico': 'Clasico',
                'classic': 'Clasico',
                'clásico': 'Clasico'
            }
            normalized = value.lower().strip()
            return genero_map.get(normalized, 'Drama')
        
        # Si ya es un enum, lo convertimos a string
        if hasattr(value, 'value'):
            return value.value
        
        return 'Drama'
    
    @staticmethod
    def _normalize_fecha(value: Any) -> Optional[datetime]:
        """Convierte varios formatos de fecha a datetime"""
        if value is None:
            return None
        
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            # Intentar varios formatos comunes
            formats = [
                "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO con Z
                "%Y-%m-%dT%H:%M:%S",       # ISO sin Z
                "%Y-%m-%dT%H:%M:%S.%f",    # ISO con microsegundos
                "%Y-%m-%d %H:%M:%S",       # Con espacio
                "%Y-%m-%d",                # Solo fecha
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            
            # Intentar con fromisoformat como fallback
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                pass
            
            raise ValueError(f"Formato de fecha no reconocido: {value}")
        
        raise ValueError(f"Tipo de fecha no soportado: {type(value)}")