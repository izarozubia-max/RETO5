# RETO5
Una persona puede contratar un seguro de protección de pagos junto con un préstamo para cubrir el riesgo de no poder hacer frente a las cuotas. En este contexto, nuestro cliente Lagun Aro necesita analizar el riesgo que asume en cada operación para poder tomar decisiones adecuadas en su actividad diaria.

## Contexto y objetivo
El objetivo principal del reto es estimar el valor presente del riesgo asumido por persona, teniendo en cuenta el sistema de amortización del préstamo y el perfil de cada cliente. Para ello, se simulará la amortización de los préstamos mediante los sistemas francés y alemán, seleccionando posteriormente uno de ellos para continuar el análisis. A partir del método elegido, se calculará el valor presente de las cuotas pendientes cuando el préstamo se encuentre a mitad de su duración. Además, se desarrollarán modelos predictivos que permitan estimar tanto el coste esperado del seguro de protección de pagos como la probabilidad de impago de cada cliente, utilizando para ello las variables que se consideren más relevantes.

## Equipo Rojo: Markel Araguzo Salaberria, Gaizka Saiz Mimenza, Izaro Zubia Zuluaga, Laura Bailey Barriocanal, Galder Lozano Uresandi y Nicolás García de la Fuente

## Estructura del repositorio

```
├── docker_reto_5_alumnos/                 # servicio de la API
│   ├── API
│   └── main.py
    └── requirements.txt
    ├── loader
    └── load_data.py
    └── requirements.txt
├── .gitignore                             # datos
├── Preprocesamiento.ipynb
├── cuadros_amortización.ipynb
├── Valor_actual.ipynb
├── predicción_calcular_prima.ipynb
├── README.md              
```

## Datos

(Origen de los datasets, qué contiene cada uno, periodo que cubren y limitaciones o consideraciones de privacidad. Si los datos no están en el repositorio, indica dónde conseguirlos.)

## Notebooks

| `Preprocesamiento.ipynb` | Análisis exploratorio y limpieza |
| `cuadros_amortizacion.ipynb` | Cálculo de cuotas a pagar de cada cliente mediante los sistemas de amortización francés y alemán |
| `predicción_calcular_prima.ipynb` | Predice el cálculo de la prima de cada cliente |
| `Valor_actual.ipynb` | Cálculo del valor actual sobre los préstamos en la mitad del periodo de los pagos |


## API
Toda la información se encuentra en el README.md de la carpeta docker_reto_5_alumnos que es la carpeta en la que se encuentra la API

## Resultados

Resume en prosa el enfoque seguido, el modelo final elegido y las métricas principales, y qué significan para el negocio.

## Gestión del proyecto

Cómo os organizasteis: sprints, issues o tablero en GitHub, convenciones de ramas y commits.

## Documentación adicional

Enlaces al informe técnico, la presentación y cualquier otro entregable.
