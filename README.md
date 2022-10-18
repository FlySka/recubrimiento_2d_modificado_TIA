# Recubrimiento 2D modificado

## Descripción

Este es el problema de recubrimiento 2D tipico de la literatura. Se trata de encontrar el recubrimiento de menor costo que cubra un conjunto de puntos dados. El costo de un recubrimiento es la suma de los costos de los puntos que no estan cubiertos. Salvo que en este caso de modifica para que el costo sea la altura de la solución y el ancho maximo se considera fijo.

## Ejecución

Antes de ejecutar el programa deben instalarse las dependencias. Para esto se debe ejecutar el siguiente comando:

```bash
pip install -r requirements.txt
```

Para ejecutar el programa se debe ejecutar el archivo `__main__.py` con el siguiente comando:

```bash
python __main__.py
```
Para verificar los argumentos del programa:

```bash
python __main__.py -h
```

## Configuración

El archivo `config/init.toml` contiene la configuración del programa. Los parametros que se pueden modificar son:

```
[CoatingMod2D]
type_algorithm = "genetic" # genetic or simulated_annealing
space_width = 9
num_blocks = 20


[GeneticAlgorithm]
type_stop = "generations" # generations or compute_time
num_generations = 4000
compute_time = 60
population_size = 500
gen_to_final_judgment = 60
survivors = 2
K = 5
mutation_rate = 0.7
per_children_choose = 0.9


[SimulatedAnnealing]
type_stop = "iterations" # iterations or compute_time
num_iterations = 1000
compute_time = 60
T_init = 100
T_end = 0.000000001
type_update = "div" # linear or exp or div
k = 0.00002 
```

