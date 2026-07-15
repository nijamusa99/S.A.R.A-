# S.A.R.A. - Módulo de ML para Boletería

## Descripción
Este módulo permite predecir la ocupación de una función teatral utilizando **Machine Learning Predictivo** (Random Forest). 
Funciona para **obras nuevas (sin historial)** y **obras en temporada (Mid-Season)** gracias a un sistema de *Factor de Momentum*.

## Arquitectura
- **Hexagonal (Clean Architecture)**: Dominio aislado, puertos y adaptadores.
- **Modelo Híbrido**: Global (Cold Start) + Momentum (Adaptación en tiempo real).
- **IA 100% On-Premise**: Corre localmente con Scikit-learn, sin costos de nube.

## Endpoints
| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/boleteria/predict` | Predice la ocupación para una función específica. |
| `POST` | `/boleteria/retrain` | Reentrena el modelo con datos históricos reales (mínimo 30 registros). |

## Instalación y Ejecución
1. Instalar dependencias: `pip install -r requirements.txt`
2. Levantar el servidor (desde la raíz del módulo):
   ```bash
   uvicorn src.api.routes:app --reload