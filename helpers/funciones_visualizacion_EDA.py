import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# FUNCIONES PARA VARIABLES NUMERICAS
# Función para graficar
def plot_histograma(data, column, figsize=(6, 3), bins=15, kde=True, mvd=True, shade=True, snk=False):
    skewness = (data[column]).skew()
    kurtosis = (data[column]).kurt()
    media = (data[column]).mean()
    var = (data[column]).var()
    std = (data[column]).std()
    plt.figure(figsize=figsize)
    plt.grid(axis='y')
    sns.histplot(data[column], bins=bins, kde=kde)
    if snk:
        plt.figtext(0.7, 0.8, f'Asimetría: {skewness:.2f}', fontsize=10, color='blue')
        plt.figtext(0.715, 0.73, f'Curtosis: {kurtosis:.2f}', fontsize=10, color='blue')
        plt.axvline(media, color='red', linestyle='--', label='Media')
 

    # Sombreado
    if mvd and shade:
        plt.axvspan(media - std, media + std, alpha=0.1, color='orange', label='±1 Std')
        plt.axvline(media + std, color='orange', linestyle=':', label='+1 Std')
        plt.axvline(media - std, color='orange', linestyle=':', label='-1 Std')
        plt.figtext(0.15, 0.80, f'Media: {media:.2f}', fontsize=10, color='red')
        plt.figtext(0.15, 0.73, f'Var:   {var:.2f}',   fontsize=10, color='red')
        plt.figtext(0.15, 0.66, f'Std:   {std:.2f}',   fontsize=10, color='orange')

    

    plt.title(f'Variable: {column}')
    plt.xlabel(f'{column}')
    plt.ylabel('Frecuencia')
    plt.show()
    
    return



def plot_distribution(
    df,
    column,
    bins=30,
    kde=True,
    discrete=False,
    show_mode=True,
    show_mean=True,
    show_median=True,
    type_stat = "count",
    show_std = True,
    title=None,
    xlabel=None,
    ax=None
):
    """
    Genera un histograma para visualizar la distribución de una variable numérica,
    con opciones para agregar KDE y señalar moda, media y mediana.

    Parámetros:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna que se desea analizar.
        bins: Cantidad de intervalos del histograma (por defecto: 30).
        kde: Si es True, agrega la curva KDE.
        discrete: Si es True, ajusta el histograma para variables discretas.
        show_mode: Si es True, calcula y marca la moda.
        show_mean: Si es True, calcula y marca la media.
        show_median: Si es True, calcula y marca la mediana.
        type_stat = "count" o "density",
        title: Título personalizado del gráfico (opcional).
        xlabel: Etiqueta personalizada del eje X (opcional).
        ax: Eje de Matplotlib donde se dibujará el gráfico (opcional).
    """

    # Obtener los datos y excluir valores faltantes
    values = df[column].dropna()

    # Crear figura solo si no se proporciona un eje
    show_figure = ax is None

    if show_figure:
        fig, ax = plt.subplots(figsize=(8, 5))

    # Histograma + KDE opcional
    histplot_kwargs = {
        "x": values,
        "kde": kde,
        "stat": type_stat,
        "ax": ax,
        "color": "salmon",
        "alpha": 0.7
    }

    if discrete:
        histplot_kwargs["discrete"] = True
    else:
        histplot_kwargs["bins"] = bins

    sns.histplot(**histplot_kwargs)

    # Calcular y marcar medidas estadísticas opcionales
    if show_mode and not values.empty:
        mode = values.mode().iloc[0]
        ax.axvline(
            mode, color="yellow", linestyle="--", linewidth=2,
            label=f"Moda: {mode:.2f}"
        )

    if show_mean and not values.empty:
        mean = values.mean()
        ax.axvline(
            mean, color="red", linestyle="--", linewidth=2,
            label=f"Media: {mean:.2f}"
        )

    if show_median and not values.empty:
        median = values.median()
        ax.axvline(
            median, color="green", linestyle="--", linewidth=2,
            label=f"Mediana: {median:.2f}"
        )


    # Desvío estándar: intervalo media ± 1 std
    if show_std and not values.empty:
        mean = values.mean()
        std = values.std()

        ax.axvline(
            mean - std, color="blue", linestyle=":", linewidth=2,
            label=f"Media - 1 std: {mean - std:.2f}"
        )
        ax.axvline(
            mean + std, color="blue", linestyle=":", linewidth=2,
            label=f"Media + 1 std: {mean + std:.2f}"
        )

    # Títulos y etiquetas
    if type_stat == 'count':
        string_ylabel = "Frecuencia"
    else:
        string_ylabel = "Density"
    ax.set_title(title if title else f"Distribución de {column}")
    ax.set_xlabel(xlabel if xlabel else column)
    ax.set_ylabel(string_ylabel)

    # Mostrar leyenda solo si hay medidas estadísticas
    if show_mode or show_mean or show_median:
        ax.legend()

    # Mostrar figura solo si la función la creó
    if show_figure:
        plt.tight_layout()
        plt.show()

    return ax


def plot_boxplot(
    df,
    column,
    orient="v",
    showfliers=True,
    show_details=False,
    title=None,
    xlabel=None,
    ylabel=None,
    color="lightblue",
    ax=None
):
    """
    Genera un boxplot para visualizar la distribución de una variable numérica,
    con opciones para mostrar los cuartiles y los límites teóricos de outliers.

    Parámetros:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna que se desea analizar.
        orient: Orientación del boxplot ('v' vertical o 'h' horizontal).
        showfliers: Si es True, muestra los posibles outliers.
        show_details: Si es True, agrega líneas de referencia para Q1,
                      mediana, Q3 y límites teóricos de outliers.
        title: Título personalizado del gráfico (opcional).
        xlabel: Etiqueta personalizada del eje X (opcional).
        ylabel: Etiqueta personalizada del eje Y (opcional).
        color: Color del boxplot.
        ax: Eje de Matplotlib donde se dibujará el gráfico (opcional).
    """

    # Obtener los datos y excluir valores faltantes
    values = df[column].dropna()

    # Crear figura solo si no se proporciona un eje
    show_figure = ax is None

    if show_figure:
        fig, ax = plt.subplots(figsize=(6, 5))

    # Calcular cuartiles y rango intercuartílico
    Q1 = values.quantile(0.25)
    Q2 = values.median()
    Q3 = values.quantile(0.75)
    IQR = Q3 - Q1

    # Calcular límites teóricos para detectar outliers
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Crear boxplot
    if orient == "v":
        sns.boxplot(
            y=values,
            color=color,
            showfliers=showfliers,
            ax=ax
        )
    elif orient == "h":
        sns.boxplot(
            x=values,
            color=color,
            showfliers=showfliers,
            ax=ax
        )
    else:
        raise ValueError("orient debe ser 'v' o 'h'.")

    # Agregar líneas de referencia opcionales
    if show_details:

        reference_lines = [
            (Q1, "blue", "Q1"),
            (Q2, "red", "Mediana"),
            (Q3, "green", "Q3"),
            (lower_limit, "purple", "Límite inferior"),
            (upper_limit, "brown", "Límite superior")
        ]

        for value, line_color, label in reference_lines:

            if orient == "v":
                ax.axhline(
                    value,
                    color=line_color,
                    linestyle="--" if label in ["Q1", "Mediana", "Q3"] else ":",
                    linewidth=1,
                    label=f"{label}: {value:.2f}"
                )
            else:
                ax.axvline(
                    value,
                    color=line_color,
                    linestyle="--" if label in ["Q1", "Mediana", "Q3"] else ":",
                    linewidth=1,
                    label=f"{label}: {value:.2f}"
                )

        ax.legend(fontsize=8)

    # Títulos y etiquetas
    ax.set_title(title if title else f"Boxplot de {column}")

    if orient == "v":
        ax.set_xlabel(xlabel if xlabel else "")
        ax.set_ylabel(ylabel if ylabel else column)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
    else:
        ax.set_xlabel(xlabel if xlabel else column)
        ax.set_ylabel(ylabel if ylabel else "")
        ax.grid(axis="x", linestyle="--", alpha=0.5)

    # Mostrar figura solo si la función la creó
    if show_figure:
        plt.tight_layout()
        plt.show()

    return ax


# FUNCIONES PARA VARIABLES CATEGORICAS

def plot_categorical_bar_distribution(
    df,
    column,
    show_values=True,
    show_percentages=False,
    order=None,
    palette="pastel",
    title=None,
    xlabel=None,
    ylabel="Cantidad",
    ax=None
):
    """
    Genera un gráfico de barras con la distribución de frecuencias
    de una variable categórica.

    Permite mostrar cantidades absolutas y/o porcentajes.

    Parámetros:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna categórica.
        show_values: Si es True, muestra las frecuencias absolutas.
        show_percentages: Si es True, muestra los porcentajes.
        order: Orden personalizado de las categorías (opcional).
        palette: Paleta de colores del gráfico.
        title: Título personalizado (opcional).
        xlabel: Etiqueta del eje X (opcional).
        ylabel: Etiqueta del eje Y (opcional).
        ax: Eje de Matplotlib donde se dibujará el gráfico (opcional).
    """

    values = df[column].dropna()

    if order is None:
        order = values.value_counts().index.tolist()

    counts = values.value_counts().reindex(order, fill_value=0)
    percentages = counts / len(values) * 100

    # Crear figura solo si no se proporciona un eje
    show_figure = ax is None

    if show_figure:
        fig, ax = plt.subplots(figsize=(8, 5))

    sns.countplot(
        x=column,
        data=df,
        order=order,
        hue=column,
        palette=palette,
        legend=False,
        ax=ax
    )

    if show_values or show_percentages:
        for i, count in enumerate(counts):
            label = []

            if show_values:
                label.append(f"{count}")

            if show_percentages:
                label.append(f"{percentages.iloc[i]:.1f}%")

            ax.text(
                i,
                count,
                "\n".join(label),
                ha="center",
                va="bottom"
            )

    ax.set_title(title if title else f"Distribución de {column}")
    ax.set_xlabel(xlabel if xlabel else column)
    ax.set_ylabel(ylabel)

    # Mostrar figura solo si la función la creó
    if show_figure:
        plt.tight_layout()
        plt.show()

    return ax



def plot_categorical_pie(
    df,
    column,
    show_values=False,
    show_percentages=True,
    palette="pastel",
    startangle=90,
    title=None,
    order=None,
    ax=None
):
    """
    Genera un gráfico de torta para visualizar la proporción
    de cada categoría de una variable.

    Parámetros:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna categórica.
        show_values: Si es True, muestra las frecuencias absolutas.
        show_percentages: Si es True, muestra los porcentajes.
        palette: Paleta de colores del gráfico.
        startangle: Ángulo inicial del gráfico.
        title: Título personalizado (opcional).
        order: Orden personalizado de las categorías (opcional).
        ax: Eje de Matplotlib donde se dibujará el gráfico (opcional).
    """

    values = df[column].dropna()

    if order is None:
        if isinstance(values.dtype, pd.CategoricalDtype) and values.dtype.ordered:
            order = values.cat.categories.tolist()
        else:
            order = values.value_counts().index.tolist()

    counts = values.value_counts().reindex(order, fill_value=0)
    counts = counts[counts > 0]

    colors = sns.color_palette(palette, n_colors=len(counts))

    def format_label(pct):
        label = []

        if show_percentages:
            label.append(f"{pct:.1f}%")

        if show_values:
            count = int(round(pct / 100 * counts.sum()))
            label.append(f"{count}")

        return "\n".join(label)

    # Crear figura solo si no se proporciona un eje
    show_figure = ax is None

    if show_figure:
        fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        counts,
        labels=counts.index,
        colors=colors,
        autopct=format_label if (show_values or show_percentages) else None,
        startangle=startangle
    )

    ax.set_title(title if title else f"Distribución de {column}")

    ax.axis("equal")

    # Mostrar figura solo si la función la creó
    if show_figure:
        plt.tight_layout()
        plt.show()

    return ax