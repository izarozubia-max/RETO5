# RETO5

Una persona puede contratar un seguro de protección de pagos junto con un préstamo para cubrir el riesgo de no poder hacer frente a las cuotas. En este contexto, nuestro cliente Lagun Aro necesita analizar el riesgo que asume en cada operación para poder tomar decisiones adecuadas en su actividad diaria.

## Contexto y objetivo

El objetivo principal del reto es estimar el valor presente del riesgo asumido por persona, teniendo en cuenta el sistema de amortización del préstamo y el perfil de cada cliente. Para ello, se simulará la amortización de los préstamos mediante los sistemas francés y alemán, seleccionando posteriormente uno de ellos para continuar el análisis. A partir del método elegido, se calculará el valor presente de las cuotas pendientes cuando el préstamo se encuentre a mitad de su duración. Además, se desarrollarán modelos predictivos que permitan estimar tanto el coste esperado del seguro de protección de pagos como la probabilidad de impago de cada cliente, utilizando para ello las variables que se consideren más relevantes.

## Equipo

Equipo Rojo: Markel Araguzo Salaberria, Gaizka Saiz Mimenza, Izaro Zubia Zuluaga, Laura Bailey Barriocanal, Galder Lozano Uresandi y Nicolás García de la Fuente

## Estructura del repositorio

```
├── docker_reto_5_alumnos/            # servicio de la API y carga de datos
│   ├── API/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── loader/
│       ├── load_data.py
│       └── requirements.txt
├── Preprocesamiento.ipynb
├── cuadros_amortización.ipynb
├── Valor_actual.ipynb
├── calculo_van_tir.ipynb
├── prediccion_calcular_prima.ipynb
├── prediccion_probabilidad_impago.ipynb
├── datos_para_powerBI.ipynb
├── .gitignore                        # excluye los datos del repositorio
└── README.md
```

## Datos

Los datos de partida son los de los préstamos proporcionados por la asignatura (fichero `Prestamos_Data_Alumnos_v5.xlsx`), con información de cada cliente como la edad, los ingresos, el importe inicial, el scoring crediticio, la duración y el tipo de interés del préstamo, así como la variable de impago y la prima del seguro. Para este grupo, el análisis se limita obligatoriamente a los préstamos con propósito "Educación".

Los datos no se incluyen en el repositorio (están excluidos mediante `.gitignore`).

## Notebooks

| Notebook | Qué hace |
|---|---|
| `Preprocesamiento.ipynb` | Análisis exploratorio y limpieza |
| `cuadros_amortización.ipynb` | Cálculo de cuotas a pagar de cada cliente mediante los sistemas de amortización francés y alemán |
| `Valor_actual.ipynb` | Cálculo del valor actual sobre los préstamos en la mitad del periodo de los pagos |
| `prediccion_calcular_prima.ipynb` | Predice el cálculo de la prima de cada cliente |
| `prediccion_probabilidad_impago.ipynb` | Predice la probabilidad de impago de cada cliente |
| `datos_para_powerBI.ipynb` | Prepara los datos para el informe de Power BI y para la API |
| `calculo_van_tir.ipynb` | Cálculo del VAN y TIR |


## API

Toda la información se encuentra en el README.md de la carpeta docker_reto_5_alumnos que es la carpeta en la que se encuentra la API
