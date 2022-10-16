"""
Clase del algoritmo genetico
"""
from typing import List
from copy import deepcopy
from loguru import logger
from time import perf_counter

from coating_mod_2d.block import Block
from genetic.population import Population
from genetic.individual import Individual


class Genetic(object):
    def __init__(
        self,
        space_width: int,
        # area_factor: float,
        blocks: List[Block],
        num_individuals: int = None,
        population: List[Individual] = None,
        K: int = 2,
        per_child_choose: float = 0.5,
        gen_to_final_judgment: int = 10,
        survivors: int = 1,
        mutation_rate: float = 0.1,
        type_stop: str = "generations",
        generations: int = 100,
        compute_time: int = 60,
        n_jobs: int = 1,
    ) -> None:
        self.space_width = space_width
        # self.area_factor = area_factor
        self.blocks = blocks
        self.n_jobs = n_jobs
        self.population = Population(
            space_width=space_width, 
            # area_factor=area_factor,
            blocks=deepcopy(blocks),
            num_individuals=num_individuals,
            n_jobs=n_jobs
        )
        self.time_computing = 0
        self.best_individual = self.population.best_individual
        self.worst_individual = self.population.worst_individual
        self.average_fitness = self.population.average_fitness
        self.median_fitness = self.population.median_fitness
        self.best_individuals = [self.best_individual.fitness]
        self.worst_individuals = [self.worst_individual.fitness]
        self.average_fitnesses = [self.average_fitness]
        self.median_fitnesses = [self.median_fitness]

        self.K = K
        self.per_child_choose = per_child_choose
        self.gen_to_final_judgment = gen_to_final_judgment
        self.survivors = survivors
        self.same_best_individual = 0
        self.mutation_rate = mutation_rate

        self.type_stop = type_stop
        self.generations = generations
        self.compute_time = compute_time
        self.start = perf_counter()
        self.generation = 0

        self.start_info()

    def run(self) -> None:
        while self.stop(self.type_stop):
            # Seleccion
            logger.debug(f"Seleccion")
            tic = perf_counter()
            parents = self.population.selection_tournament(self.K, self.per_child_choose)
            toc = perf_counter()
            logger.debug(f"Seleccion: {round(toc - tic, 6)}")

            # Cruza
            logger.debug(f"Cruza")
            tic = perf_counter()
            children = self.population.crossover(parents, per_children=self.per_child_choose)
            toc = perf_counter()
            logger.debug(f"Cruza: {round(toc - tic, 6)}")

            # Mutacion
            logger.debug(f"Mutacion")
            tic = perf_counter()
            children_mutated = self.population.mutation(children, mutation_rate=self.mutation_rate)
            toc = perf_counter()
            logger.debug(f"Mutacion: {round(toc - tic, 6)}")

            # Reemplazo
            logger.debug(f"Reemplazo")
            tic = perf_counter()
            if self.same_best_individual == self.gen_to_final_judgment:
                logger.info("Juicio final")
                next_generation = self.population.replacement_final_judgment(survivors=self.survivors)
                self.same_best_individual = 0
            else:
                next_generation = self.population.replacement_gap(children_mutated)
            self.population = Population(
                self.space_width,
                # deepcopy(self.area_factor),
                self.blocks,
                population=next_generation,
                n_jobs=self.n_jobs,
            )
            toc = perf_counter()
            logger.debug(f"Reemplazo: {round(toc - tic, 6)}")

            # Actualizacion de estadisticas
            logger.debug(f"Actualizacion de estadisticas")
            tic = perf_counter()
            self.best_individual = self.population.best_individual
            self.worst_individual = self.population.worst_individual
            self.average_fitness = self.population.average_fitness
            self.median_fitness = self.population.median_fitness
            self.best_individuals.append(self.best_individual.fitness)
            self.worst_individuals.append(self.worst_individual.fitness)
            self.average_fitnesses.append(self.average_fitness)
            self.median_fitnesses.append(self.median_fitness)
            toc = perf_counter()
            self.time_computing = round(perf_counter() - self.start, 6)
            logger.debug(f"Actualizacion de estadisticas: {round(toc - tic, 6)}")

            # Comprobacion de juicio final
            if self.best_individuals[-1] == self.best_individuals[-2]:
                self.same_best_individual += 1
            else:
                self.same_best_individual = 0

            # Actualizacion de generacion
            self.generation += 1

            # Imprimir informacion
            self.info()

    def stop(self, type_stop: str) -> None:
        """
        Comprueba si se debe detener el algoritmo genetico
        """
        if type_stop == "generations":
            return self.generations > self.generation
        elif type_stop == "compute_time":
            return self.compute_time > perf_counter() - self.start
        else:
            raise ValueError("type_stop debe ser 'generations' o 'compute_time'")

    def start_info(self) -> None:
        """
        Imprime informacion del algoritmo genetico
        """
        logger.info(f"Inicio de algoritmo genetico")
        logger.info(f"Tipo parada: {self.type_stop}")
        if self.type_stop == "generations":
            logger.info(f"Generaciones: {self.generations}")
        elif self.type_stop == "compute_time":
            logger.info(f"Tiempo de computo: {self.compute_time}")
        logger.info(f"Numero de individuos: {self.population.num_individuals}")

    def info(self) -> None:
        """
        Imprime informacion del algoritmo genetico
        """
        logger.info(f"Generacion: {self.generation}")
        logger.info(f"Mejor individuo: {self.best_individual.fitness}")
        logger.info(f"Peor individuo: {self.worst_individual.fitness}")
        logger.info(f"Fitness promedio: {self.average_fitness}")
        logger.info(f"Fitness mediana: {self.median_fitness}")
        logger.info(f"Tiempo de computo: {perf_counter() - self.start}")