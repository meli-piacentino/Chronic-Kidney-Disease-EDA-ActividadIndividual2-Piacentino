# Chronic Kidney Disease Analysis

## Descripción del proyecto

Proyecto académico desarrollado en el marco de la materia **Análisis de Datos** de la Especialización en Inteligencia Artificial (CEIA) de la Facultad de Ingeniería de la Universidad de Buenos Aires (FIUBA).

El trabajo se basa en el análisis de registros clínicos de pacientes evaluados por enfermedad renal crónica, provenientes de un contexto clínico asociado al Apollo Hospitals, en Karaikudi, India. Los datos fueron documentados en julio de 2015.

El dataset contiene **400 registros y 25 variables**: 24 características clínicas y una variable objetivo. Incluye información demográfica, mediciones clínicas y resultados de análisis de laboratorio, con variables numéricas y categóricas.

El objetivo del proyecto es realizar un análisis exploratorio de los datos (EDA), caracterizar las variables, evaluar la calidad de la información, identificar patrones y relaciones entre las características clínicas y la presencia de enfermedad renal crónica, y aplicar técnicas de visualización.

## Dataset

**Nombre:** Chronic Kidney Disease

**Fuente:** UCI Machine Learning Repository

**Enlace:** https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease

### Características principales

| Característica | Descripción |
|---|---|
| Cantidad de registros | 400 |
| Cantidad de variables | 25 (24 features + 1 target) |
| Variables numéricas | 11 |
| Variables categóricas | 13 |
| Dominio | Salud / Medicina |
| Contexto clínico | Apollo Hospitals, Karaikudi, India |
| Fecha de documentación | Julio de 2015 |
| Problema de ML | Clasificación supervisada |

Las variables incluyen características de los pacientes, como la edad, mediciones clínicas, como la presión arterial, y resultados de laboratorio, como los niveles de glucosa en sangre, entre otros indicadores relacionados con la función renal.

La variable objetivo (`class`) identifica la presencia o ausencia de enfermedad renal crónica, mediante dos categorías: `ckd` (con enfermedad renal crónica) y `notckd` (sin enfermedad renal crónica).

**Selección del archivo:** La descarga del dataset desde UCI ofrece distintos archivos. Luego de comparar los registros, se verificó que el archivo `chronic_kidney_disease_full.arff` contiene los mismos registros que el archivo común. Por este motivo, se seleccionó la versión completa en un único archivo para realizar el análisis.

## Estructura del repositorio

```text
chronic-kidney-disease-eda/
│
├── data/
│   ├── raw/
│   │   └── chronic_kidney_disease_full.arff
│   │
│   └── processed/
│
├── helpers/
│   ├── __init__.py
│   └── arff_utils.py
│
├── notebooks/
│   └── 01_acondicionamiento_dataset.ipynb
│
├── .vscode/
│   └── settings.json
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Tecnologías y herramientas

El proyecto se desarrolla utilizando Python y Jupyter Notebook.

Principales librerías previstas:

- **NumPy:** operaciones numéricas y procesamiento de datos.
- **Pandas:** manipulación y análisis de datos.
- **Matplotlib:** generación de visualizaciones.
- **Seaborn:** visualización y análisis estadístico.
- **Missingno:** exploración y visualización de valores faltantes.
- **SciPy:** herramientas de análisis científico y estadístico.
- **Scikit-learn:** aplicación de técnicas de aprendizaje automático.

Las dependencias y sus versiones se encuentran especificadas en `requirements.txt`.

## Configuración del entorno

Para reproducir el entorno de trabajo, se recomienda utilizar Python 3.11.

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

2. Ingresar al directorio del proyecto:

```bash
cd chronic-kidney-disease-eda
```

3. Crear y activar un entorno virtual:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

4. Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

5. Seleccionar el entorno virtual como intérprete de Python y kernel de Jupyter en VS Code.

## Objetivos del análisis

- Caracterizar el dataset mediante el análisis de sus dimensiones, variables y tipos de datos.
- Explorar las distribuciones de las variables clínicas y de laboratorio.
- Identificar valores faltantes, anomalías, inconsistencias y posibles outliers.
- Analizar patrones y relaciones entre las variables y la presencia de enfermedad renal crónica.
- Aplicar técnicas de visualización e interpretar los resultados.

## Estado del proyecto

En desarrollo.

---

**Proyecto académico – CEIA | FIUBA**
