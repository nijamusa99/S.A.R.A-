# S.A.R.A-
S.A.R.A. — Sistema Autónomo de Remuneración Artística. Motor de liquidación y auditoría de nómina para artes escénicas, 100% self-hosted con IA local (Llama 3.1 + RAG). Cero costo en APIs externas, soberanía total de datos.

Sistema de liquidación de nómina para artes escénicas con IA local, arquitectura hexagonal y procesamiento de PDFs.

## Características principales
- Extracción de datos de contratos desde PDF usando Ollama (Llama 3.1)
- Cálculo de pagos con retenciones (ReteFuente 11%)
- Arquitectura limpia (hexagonal) para fácil mantenimiento
- API REST documentada con OpenAPI (Swagger)

## Stack tecnológico
- **Backend**: FastAPI + Python 3.11
- **IA Local**: Ollama + Llama 3.1 8B
- **Arquitectura**: Hexagonal (Clean Architecture)
- **PDF**: pdfplumber

## Instalación rápida
bash
# Clonar
git clone https://github.com/nijamusa99/S.A.R.A-.git
cd Payroll_mvp

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
