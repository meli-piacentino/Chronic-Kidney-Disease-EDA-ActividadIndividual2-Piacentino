
from io import StringIO
from pathlib import Path
import numpy as np
import pandas as pd
import csv
from scipy.io import arff


def load_arff_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Carga un archivo ARFF y devuelve su contenido como un DataFrame de pandas.

    Elimina espacios sobrantes alrededor de los valores.
    Los valores faltantes representados mediante '?' se convierten en NaN.
    Los valores categóricos almacenados como bytes se decodifican a texto.
    """

    # Leer el archivo y eliminar espacios sobrantes en los campos
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data_start = next(
        i for i, line in enumerate(lines)
        if line.strip().lower() == "@data"
    )

    for i in range(data_start + 1, len(lines)):
        if not lines[i].strip() or lines[i].strip().startswith("%"):
            continue

        fields = next(csv.reader([lines[i]]))
        fields = [value.strip() for value in fields]

        lines[i] = ",".join(fields) + "\n"

    # Cargar el contenido ARFF normalizado
    data, metadata = arff.loadarff(StringIO("".join(lines)))

    df = pd.DataFrame(data)

    return df


def decode_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decodifica los valores categóricos almacenados como bytes
    y los convierte en cadenas de texto (str).

    Recibe un DataFrame y devuelve una copia con los valores
    categóricos decodificados.
    """

    df = df.copy()

    # Identificar columnas de tipo object
    categorical_columns = df.select_dtypes(include=["object"]).columns

    # Decodificar los valores almacenados como bytes
    for column in categorical_columns:
        df[column] = df[column].map(
            lambda value: value.decode("utf-8")
            if isinstance(value, bytes)
            else value
        )

    return df


def replace_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaza la representación de valores faltantes '?'
    por NaN, el formato utilizado por pandas.

    Recibe un DataFrame y devuelve una copia con los valores
    faltantes normalizados.
    """

    df = df.copy()

    # Reemplazar '?' por NaN
    df.replace("?", np.nan, inplace=True)

    return df


def set_variable_types(df: pd.DataFrame, numeric_columns, ordinal_categories, nominal_categories) -> pd.DataFrame:
    """
    Ajusta los tipos de datos del DataFrame según la naturaleza
    de las variables del dataset.

    Las variables numéricas se mantienen como float64,
    las categóricas nominales se convierten a category
    y las categóricas ordinales a category con orden definido.
    """

    df = df.copy()

    # Ajustar variables numéricas
    df[numeric_columns] = df[numeric_columns].astype("float64")

    # Ajustar variables categóricas nominales
    df[nominal_categories] = df[nominal_categories].astype("category")

    # Ajustar variables categóricas ordinales
    for column, categories in ordinal_categories.items():

        # Verificar que no existan categorías inesperadas
        unexpected_values = set(df[column].dropna().unique()) - set(categories)

        if unexpected_values:
            raise ValueError(
                f"Valores inesperados en '{column}': {unexpected_values}"
            )

        dtype = pd.CategoricalDtype(
            categories=categories,
            ordered=True
        )

        df[column] = df[column].astype(dtype)

    return df


def classify_skewness(value):
    """
    Clasifica el nivel de asimetría según el valor de skewness.
    """

    if pd.isna(value):
        return np.nan
    elif abs(value) <= 0.5:
        return "Aproximadamente simétrica"
    elif abs(value) <= 1:
        return "Asimetría moderada"
    else:
        return "Asimetría alta"


def classify_kurtosis(value, tolerance=0.1):
    """
    Clasifica la curtosis en platicúrtica, mesocúrtica o leptocúrtica.
    """

    if pd.isna(value):
        return np.nan
    elif value < -tolerance:
        return "Platicúrtica"
    elif value > tolerance:
        return "Leptocúrtica"
    else:
        return "Aproximadamente Mesocúrtica"


def calculate_shannon_entropy(df, column):
    """
    Calcula la entropía de Shannon de una variable categórica.

    Parámetros:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna categórica.

    Retorna:
        Entropía de Shannon y entropía normalizada.
    """

    values = df[column].dropna()
    probabilities = values.value_counts(normalize=True)

    entropy = -np.sum(probabilities * np.log2(probabilities))

    n_categories = len(probabilities)

    if n_categories > 1:
        normalized_entropy = entropy / np.log2(n_categories)
    else:
        normalized_entropy = 0

    return entropy, normalized_entropy

