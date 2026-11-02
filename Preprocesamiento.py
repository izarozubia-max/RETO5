# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
diccionario = pd.read_excel('data/Diccionario_Variables_Alumnos.xlsx')
diccionario.head(19)

# %%
diccionario.shape

# %%
prestamos = pd.read_excel('data/Prestamos_Data_Alumnos_v5.xlsx')
prestamos.head()

# %% [markdown]
# # Limpieza y análisis descriptivo

# %%
prestamos = prestamos[prestamos["Proposito"] == "Educación"].copy()

print("Dimensiones de la muestra:", prestamos.shape)

# %%
prestamos = prestamos.drop(columns=["Proposito"]) # la variable ya no aporta información nueva

# %%
prestamos.head()

# %%
prestamos.shape

# %%
prestamos.info()

# %%
prestamos.describe()

# %% [markdown]
# ## Tipos de columnas

# %%
# las columnas 'Posesion_Hipoteca', 'Personas_Cargo' y 'Fiador' están en float y hay que pasarlas a int porque son categorías binarias, es decir, es 0 o 1.
prestamos['Posesion_Hipoteca'] = prestamos['Posesion_Hipoteca'].astype(int)
prestamos['Personas_Cargo'] = prestamos['Personas_Cargo'].astype(int)
prestamos['Fiador'] = prestamos['Fiador'].astype(int)

# %%
# las columna 'Duracion' y 'Meses_Empleo' también hay que pasarla a int porque la duración está en meses, y no tiene decimales
prestamos['Duracion'] = prestamos['Duracion'].astype(int)
prestamos['Meses_Empleo'] = prestamos['Meses_Empleo'].astype(int)

# %%
# La columna 'Ingresos' también hay que ponerla en int porque no tiene decimales
prestamos['Ingresos'] = prestamos['Ingresos'].astype(int)

# %%
prestamos.head()

# %%
prestamos.dtypes

# %% [markdown]
# ## Nulos y duplicados

# %%
prestamos.isna().sum() # solo hay dos nulos en todo el dataset. El dataset es muy grande, por lo tanto, hemos decidido borrar las filas que contienen los nulos ya que el impacto de eliminarlas es muy pequeño.

# %%
prestamos = prestamos.dropna()

# %%
print("Número de filas:", len(prestamos))
print("Número de ID únicos:", prestamos["ID"].nunique())
print("ID duplicados:", prestamos["ID"].duplicated().sum())    # no hay ningún id duplicado, todos son únicos

# %%
prestamos.duplicated().sum() # solo hay un duplicado, por lo que eliminamos la fila tambien

# %%
prestamos = prestamos.drop_duplicates()

# %% [markdown]
# # EDA

# %%
# Histogramas de varibales numéricas
columnas_numericas = [
    "Edad",
    "Ingresos",
    "Monto_Inicial",
    "Scoring_Crediticio",
    "Meses_Empleo",
    "Num_Creditos",
    "Ratio_Interes",
    "Duracion",
    "Ratio_Deuda_Ingresos",
    "Prima"
]

fig, axes = plt.subplots(
    nrows=5,
    ncols=2,
    figsize=(15, 22)
)

axes = axes.flatten()

for i, columna in enumerate(columnas_numericas):
    sns.histplot(
        data=prestamos,
        x=columna,
        bins=30,
        kde=True,
        ax=axes[i],
        color="steelblue"
    )

    axes[i].set_title(f"Distribución de {columna}")
    axes[i].set_xlabel(columna)
    axes[i].set_ylabel("Frecuencia")

plt.tight_layout()
plt.show()

# %%
# Boxplots para observar valores atípicos
fig, axes = plt.subplots(
    nrows=5,
    ncols=2,
    figsize=(15, 20)
)

axes = axes.flatten()

for i, columna in enumerate(columnas_numericas):
    sns.boxplot(
        data=prestamos,
        x=columna,
        ax=axes[i],
        color="lightblue"
    )

    axes[i].set_title(f"Boxplot de {columna}")
    axes[i].set_xlabel(columna)

plt.tight_layout()
plt.show()


# %% [markdown]
# ##### En los boxplots se observan valores atípicos en Ingresos y Monto_Inicial. Se decide dejarlos tal cual están: son variables económicas con una distribución naturalmente asimétrica (la mayoría de personas tiene ingresos y préstamos moderados, pero un número menor de casos con valores altos es normal, no un error de los datos), y esos valores altos son precisamente los más relevantes para estimar el riesgo y el coste del seguro, que es el objetivo del reto.

# %%
# Distribución de varibales categóricas
columnas_categoricas = [
    "Estudios",
    "Tipo_Jornada_Laboral",
    "Estado_Civil",
    "Posesion_Hipoteca",
    "Personas_Cargo",
    "Fiador",
    "Impago"
]

fig, axes = plt.subplots(
    nrows=4,
    ncols=2,
    figsize=(16, 18)
)

axes = axes.flatten()

for i, columna in enumerate(columnas_categoricas):
    orden = prestamos[columna].value_counts().index

    sns.countplot(
        data=prestamos,
        x=columna,
        order=orden,
        ax=axes[i],
        color="steelblue"
    )

    axes[i].set_title(f"Distribución de {columna}")
    axes[i].set_xlabel(columna)
    axes[i].set_ylabel("Número de registros")
    axes[i].tick_params(axis="x", rotation=30)

# Ocultar el octavo espacio, porque solamente hay siete variables
axes[7].set_visible(False)

plt.tight_layout()
plt.show()

# %%
for columna in columnas_categoricas:
    resumen = pd.DataFrame({
        "Frecuencia": prestamos[columna].value_counts(),
        "Porcentaje": (
            prestamos[columna]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
        )
    })

    print(f"\n{columna}")
    display(resumen)

# %% [markdown]
# # Preprocesamiento para el modelado

# %% [markdown]
# ## Codificación de variables categóricas

# %% [markdown]
# ### Codificación ordinal

# %%
prestamos['Estudios'].unique()

# %%
# en el caso de la columna 'Educación', vamos a hacer una codificación ordinal, ya que las categorias tienen un orden educativo real. Cuanto más formación tengan, el número va a ser más alto.
orden_estudios = {
    "Escolar": 0,
    "Grado Universitario": 1,
    "Máster": 2,
    "Doctorado": 3
}

prestamos["Estudios"] = prestamos["Estudios"].str.strip()
prestamos["Estudios_encoded"] = prestamos["Estudios"].map(orden_estudios)

print(prestamos[["Estudios", "Estudios_encoded"]].value_counts())

# %% [markdown]
# ### "Estudios" ya no aporta información nueva una vez creada "Estudios_encoded" , así que se elimina.

# %%
prestamos = prestamos.drop(columns=["Estudios"])

# %%
prestamos['Estado_Civil'].unique()

# %% [markdown]
# ### Codificación one-hot

# %%
# Para que sea mas efectivo para los modelos posteriores, hemos decidido hacer un One Hot Enconding en las variable 'Estado_Civil' y 'Tipo_Jornada_Laboral' para binarizar las variabales
prestamos["Estado_Civil"] = prestamos["Estado_Civil"].str.strip().str.capitalize()
prestamos = pd.get_dummies(prestamos, columns=["Estado_Civil"], dtype=int, drop_first=True)

# %%
prestamos['Tipo_Jornada_Laboral'].unique()

# %%
prestamos["Tipo_Jornada_Laboral"] = prestamos["Tipo_Jornada_Laboral"].str.strip().str.capitalize()
prestamos = pd.get_dummies(prestamos, columns=["Tipo_Jornada_Laboral"], dtype=int, drop_first=True)

# %%
prestamos.head()

# %% [markdown]
# ### Correlación de las variables numéricas con las variables objetivo

# %%
columnas_correlacion = columnas_numericas + ["Impago"]

matriz_correlacion = prestamos[columnas_correlacion].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    matriz_correlacion[["Prima", "Impago"]],
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)
plt.title("Correlación de variables numéricas con Prima e Impago")
plt.tight_layout()
plt.show()

# %% [markdown]
# Hemos decidido crear un csv con los datos limpios para empezar con el modelo predictivo y no tener que cargarlo cada vez

# %%
prestamos.to_csv("datos_preprocesados.csv", index=False)


