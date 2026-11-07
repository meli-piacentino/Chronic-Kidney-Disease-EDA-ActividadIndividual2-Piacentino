from pathlib import Path
import math
import csv
import re


def read_arff_header(file_path):
    """
    Lee y devuelve el encabezado de un archivo ARFF,
    incluyendo toda la información anterior a @data.
    """
    file_path = Path(file_path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    for i, line in enumerate(lines):
        if line.strip().lower() == "@data":
            return "\n".join(lines[:i + 1])

    raise ValueError("No se encontró la declaración @data en el archivo.")


def find_inconsistent_rows(file_path, expected_fields=25):
    """
    Identifica registros que no tienen la cantidad de campos esperada.

    Devuelve una lista de diccionarios con:
    - Número de línea del archivo.
    - Cantidad de campos encontrados.
    - Contenido original del registro.
    """
    file_path = Path(file_path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    data_index = next(
        (i for i, line in enumerate(lines)
         if line.strip().lower() == "@data"),
        None
    )

    if data_index is None:
        raise ValueError("No se encontró la declaración @data.")

    inconsistent_rows = []

    for line_number, line in enumerate(
        lines[data_index + 1:],
        start=data_index + 2
    ):
        if not line.strip() or line.strip().startswith("%"):
            continue

        fields = next(csv.reader([line]))

        if len(fields) != expected_fields:
            inconsistent_rows.append({
                "line_number": line_number,
                "field_count": len(fields),
                "content": line
            })

    return inconsistent_rows




def read_arff_attributes(file_path):
    """
    Extrae los atributos declarados en el encabezado de un archivo ARFF.

    Devuelve una lista de diccionarios con:
    - name: nombre del atributo.
    - type: tipo de dato declarado.
    - allowed_values: valores permitidos si es un atributo nominal.
    """

    file_path = Path(file_path)
    lines = file_path.read_text(encoding="utf-8").splitlines()

    attributes = []

    for line in lines:
        stripped = line.strip()

        if stripped.lower().startswith("@data"):
            break

        if stripped.lower().startswith("@attribute"):
            match = re.match(
                r"@attribute\s+(?:'([^']+)'|\"([^\"]+)\"|(\S+))\s+(.+)",
                stripped,
                re.IGNORECASE
            )

            if match is None:
                continue

            name = match.group(1) or match.group(2) or match.group(3)
            data_type = match.group(4).strip()

            # Si el tipo está definido mediante un conjunto de valores
            if data_type.startswith("{") and data_type.endswith("}"):
                allowed_values = [
                    value.strip().strip("'\"")
                    for value in data_type[1:-1].split(",")
                ]
                attribute_type = "nominal"

            else:
                allowed_values = None
                attribute_type = data_type

            attributes.append({
                "name": name,
                "type": attribute_type,
                "allowed_values": allowed_values
            })

    return attributes





def correct_arff_format_line_215_218_515(input_path, output_path, expected_fields=25):
    """
    Corrige inconsistencias de formato previamente identificadas
    en el archivo ARFF.

    Correcciones:
    - Líneas 215 y 218: elimina la coma sobrante al final.
    - Línea 515: elimina la coma adicional entre dos valores consecutivos.

    Verifica que todos los registros tengan la cantidad esperada
    de campos antes de guardar el archivo corregido.
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    # Leer el archivo original
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Identificar el comienzo de los datos
    data_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().lower() == "@data"
        ),
        None
    )

    if data_index is None:
        raise ValueError("No se encontró la declaración @data.")

    # Correcciones de formato
    corrections = {
        215: "trailing_comma",
        218: "trailing_comma",
        515: "extra_comma"
    }

    for line_number, correction in corrections.items():

        index = line_number - 1

        if index <= data_index or index >= len(lines):
            raise ValueError(
                f"La línea {line_number} no corresponde a una línea de datos."
            )

        # Separar el contenido del salto de línea
        original_line = lines[index]
        line = original_line.rstrip("\r\n")
        newline = original_line[len(line):]

        if correction == "trailing_comma":

            if not line.endswith(","):
                raise ValueError(
                    f"No se encontró la coma final esperada "
                    f"en la línea {line_number}."
                )

            line = line[:-1]

        elif correction == "extra_comma":

            original = "no,,no,no,good,no,no,notckd"
            corrected = "no,no,no,good,no,no,notckd"

            if original not in line:
                raise ValueError(
                    f"No se encontró el patrón esperado "
                    f"en la línea {line_number}."
                )

            line = line.replace(original, corrected, 1)

        lines[index] = line + newline

    # Verificar la cantidad de campos de todos los registros
    inconsistent_rows = []

    for line_number, line in enumerate(
        lines[data_index + 1:],
        start=data_index + 2
    ):

        if not line.strip() or line.strip().startswith("%"):
            continue

        fields = next(csv.reader([line]))

        if len(fields) != expected_fields:
            inconsistent_rows.append({
                "line_number": line_number,
                "field_count": len(fields),
                "content": line.strip()
            })

    # No guardar si todavía existen inconsistencias
    if inconsistent_rows:
        raise ValueError(
            f"Se encontraron registros con una cantidad inesperada "
            f"de campos: {inconsistent_rows}"
        )

    # Guardar el archivo corregido
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        file.writelines(lines)

    print("Correcciones aplicadas correctamente.")
    print(f"Registros verificados: todos tienen {expected_fields} campos.")
    print(f"Archivo guardado en: {output_path}")



def validate_categorical_values(file_path):
    """
    Verifica que los valores de los atributos categóricos
    pertenezcan a los valores permitidos declarados en el
    encabezado del archivo ARFF.

    Los valores faltantes representados por '?' se excluyen
    de la validación.

    Devuelve una lista de diccionarios con las inconsistencias
    encontradas.
    """

    file_path = Path(file_path)

    # Obtener los metadatos de los atributos
    attributes = read_arff_attributes(file_path)

    # Identificar atributos categóricos
    categorical_attributes = {
        attribute["name"]: set(attribute["allowed_values"])
        for attribute in attributes
        if attribute["type"] == "nominal"
    }

    # Encontrar el comienzo de los datos
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().lower() == "@data"
        ),
        None
    )

    if data_index is None:
        raise ValueError("No se encontró la declaración @data.")

    inconsistencies = []

    # Recorrer los registros
    for line_number, line in enumerate(
        lines[data_index + 1:],
        start=data_index + 2
    ):

        if not line.strip() or line.strip().startswith("%"):
            continue

        fields = next(csv.reader([line]))

        if len(fields) != len(attributes):
            raise ValueError(
                f"La línea {line_number} tiene {len(fields)} campos; "
                f"se esperaban {len(attributes)}."
            )

        # Revisar cada atributo categórico
        for index, attribute in enumerate(attributes):

            name = attribute["name"]

            if name not in categorical_attributes:
                continue

            value = fields[index].strip()

            # Ignorar valores faltantes
            if value == "?":
                continue

            allowed_values = categorical_attributes[name]

            if value not in allowed_values:
                inconsistencies.append({
                    "line_number": line_number,
                    "attribute": name,
                    "value_found": value,
                    "allowed_values": sorted(allowed_values)
                })

    return inconsistencies


def validate_numeric_values(file_path):
    """
    Verifica que los valores de los atributos numéricos
    puedan interpretarse correctamente como números.

    Los valores faltantes representados por '?' se excluyen
    de la validación.

    Para atributos declarados como integer, también verifica
    que los valores sean enteros.

    Devuelve una lista de diccionarios con las inconsistencias
    encontradas.
    """

    file_path = Path(file_path)

    # Obtener los metadatos de los atributos
    attributes = read_arff_attributes(file_path)

    numeric_types = {"numeric", "real", "integer"}

    numeric_attributes = {
        attribute["name"]: attribute["type"].lower()
        for attribute in attributes
        if attribute["type"].lower() in numeric_types
    } # dictionary comprehension

    # Encontrar el comienzo de los datos
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().lower() == "@data"
        ),
        None
    )

    if data_index is None:
        raise ValueError("No se encontró la declaración @data.")

    inconsistencies = []

    # Recorrer los registros
    for line_number, line in enumerate(
        lines[data_index + 1:],
        start=data_index + 2
    ):

        if not line.strip() or line.strip().startswith("%"):
            continue

        fields = next(csv.reader([line]))

        if len(fields) != len(attributes):
            raise ValueError(
                f"La línea {line_number} tiene {len(fields)} campos; "
                f"se esperaban {len(attributes)}."
            )

        # Revisar cada atributo numérico
        for index, attribute in enumerate(attributes):

            name = attribute["name"]

            if name not in numeric_attributes:
                continue

            value = fields[index].strip()

            # Ignorar valores faltantes
            if value == "?":
                continue

            # Verificar que el campo no esté vacío
            if value == "":
                inconsistencies.append({
                    "line_number": line_number,
                    "attribute": name,
                    "value_found": value,
                    "issue": "Campo vacío"
                })
                continue

            # Verificar que el valor sea numérico
            try:
                numeric_value = float(value)

            except ValueError:
                inconsistencies.append({
                    "line_number": line_number,
                    "attribute": name,
                    "value_found": value,
                    "issue": "Valor no numérico"
                })
                continue

            # Verificar que el valor sea finito
            if not math.isfinite(numeric_value):
                inconsistencies.append({
                    "line_number": line_number,
                    "attribute": name,
                    "value_found": value,
                    "issue": "Valor no finito"
                })
                continue

            # Verificar valores enteros cuando corresponda
            if (
                numeric_attributes[name] == "integer"
                and not numeric_value.is_integer()
            ):
                inconsistencies.append({
                    "line_number": line_number,
                    "attribute": name,
                    "value_found": value,
                    "issue": "Se esperaba un valor entero"
                })

    return inconsistencies


def count_arff_records(file_path):
    """
    Cuenta los registros de un archivo ARFF y verifica
    cuántos campos tiene cada registro.

    Excluye líneas vacías y comentarios.

    Returns:
        dict: Cantidad de registros y cantidades de campos encontradas.
    """
    file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Buscar el inicio de los datos
    data_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().lower() == "@data"
        ),
        None
    )

    if data_index is None:
        raise ValueError("No se encontró la sección @data en el archivo.")

    # Obtener los registros, excluyendo líneas vacías y comentarios
    records = [
        row
        for row in csv.reader(lines[data_index + 1:])
        if row
        and any(value.strip() for value in row)
        and not row[0].strip().startswith("%")
    ]

    # Calcular la cantidad de campos por registro
    field_counts = {len(row) for row in records}

    return {
        "record_count": len(records),
        "field_counts": field_counts
    }

