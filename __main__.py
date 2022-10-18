"""
Codigo main para problema de recubrimiento 2D modificado
"""
from random import seed
from json import dump
from os import makedirs
from os.path import isdir
from copy import deepcopy

from config.config import Config
from loguru import logger
from config.logger import log_config
logger.configure(**log_config)

from coating_mod_2d.coating_mod_2d import CoatingMod2D
from genetic.genetic import Genetic
from simulated_annealing.simulated_annealing import SimulatedAnnealing

def main():
    seed(2022)

    config = Config()

    cm2d = CoatingMod2D(config.name, config.num_blocks, config.space_width)

    try:
        if config.type_algorithm == "genetic":
            genetic = Genetic(
                space_width=config.space_width,
                # area_factor=config.area_factor,
                blocks=deepcopy(cm2d.blocks),
                num_individuals=config.population_size,
                K=config.K,
                per_child_choose=config.per_children_choose,
                gen_to_final_judgment=config.gen_to_final_judgment,
                survivors=config.survivors,
                mutation_rate=config.mutation_rate,
                type_stop=config.type_stop,
                generations=config.generations,
                compute_time=config.compute_time,
                n_jobs=config.n_jobs,
            )
            genetic.run()
            results = {
                'mejores_individuos': genetic.best_individuals,
                'peores_individuos': genetic.worst_individuals,
                'fitness_promedio': genetic.average_fitnesses,
                'fitness_mediana': genetic.median_fitnesses,
                'num_individuos': config.population_size,
                'k': config.K,
                'gen_to_final_judgment': config.gen_to_final_judgment,
                'survivors': config.survivors,
                'mutation_rate': config.mutation_rate,
                'compute_time': config.compute_time,
            }
            if not isdir("resultados_genetico"):
                makedirs("resultados_genetico")
            with open(f"resultados_genetico/{config.name}.json", "w") as f:
                dump(results, f, indent=4)

        elif config.type_algorithm == "simulated_annealing":
            simulated_annealing = SimulatedAnnealing(
                space_width=config.space_width,
                blocks=deepcopy(cm2d.blocks),
                type_update=config.type_update,
                T_init=config.T_init,
                T_end=config.T_end,
                k=config.k,
                type_stop=config.type_stop,
                iterations=config.iterations,
                compute_time=config.compute_time,
                n_jobs=config.n_jobs,
            )
            simulated_annealing.run()
            results = {
                'soluciones': simulated_annealing.actual_fitnesses,
                'temperaturas': simulated_annealing.Ts,
                'mejor_solucion': simulated_annealing.best_solution.fitness,
                'T_init': config.T_init,
                'T_end': config.T_end,
                'k': config.k,
                'type_update': config.type_update,
                'compute_time': config.compute_time,
            }
            if not isdir("resultados_enfriamiento_simulado"):
                makedirs("resultados_enfriamiento_simulado")
            with open(f"resultados_enfriamiento_simulado/{config.name}.json", "w") as f:
                dump(results, f, indent=4)

        else:
            raise ValueError("No se ha especificado un algoritmo valido")

    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    main()