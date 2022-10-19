"""
Clase para el algoritmo de enfriamiento simulado
"""
from math import exp
from typing import List
from copy import deepcopy
from time import perf_counter
from random import random
from loguru import logger

from coating_mod_2d.block import Block
from simulated_annealing.solution import Solution

class SimulatedAnnealing:
    def __init__(
        self,
        space_width: int,
        blocks: List[Block],
        type_update: str,
        T_init: float,
        T_end: float,
        k: float,
        type_stop: str,
        iterations: int,
        compute_time: int,
        n_jobs: int,
    ) -> None:
        self.space_width = space_width
        self.blocks = blocks
        self.type_update = type_update
        self.T_init = T_init
        self.T_end = T_end
        self.T = deepcopy(self.T_init)
        self.i = 0
        self.k = k
        self.type_stop = type_stop
        self.iterations = iterations
        self.compute_time = compute_time
        self.n_jobs = n_jobs

        self.actual_solution: Solution = None
        self.actual_fitness = 0

        self.best_solution: Solution = None
        self.best_fitness = 0

        self.actual_fitnesses = []
        self.Ts = []

        self.start = perf_counter()

    def run(self) -> None:
        """
        Funcion para ejecutar el algoritmo de enfriamiento simulado
        """
        logger.info("Iniciando algoritmo de enfriamiento simulado")
        self.best_solution = Solution(self.space_width, deepcopy(self.blocks)) 
        self.best_fitness = self.best_solution.fitness
        self.actual_solution = self.best_solution
        self.actual_fitness = self.best_fitness
        logger.info(f"Fitness inicial: {self.best_fitness}")
        self.simulated_annealing()

    def simulated_annealing(self) -> None:
        """
        Funcion para ejecutar el algoritmo de enfriamiento simulado
        """
        self.T = self.T_init
        while True:
            new_solution = self.mutate(self.actual_solution)
            new_fitness = new_solution.fitness
            if new_fitness < self.best_fitness:
                self.best_solution = new_solution
                self.best_fitness = new_fitness
                self.actual_solution = new_solution
                self.actual_fitness = new_fitness
            else:
                if random() < self.acceptance_probability(new_fitness):
                    self.actual_solution = new_solution
                    self.actual_fitness = new_fitness

            self.info()
            self.actual_fitnesses.append(self.actual_fitness)
            self.Ts.append(self.T)
            
            self.T = self.update_T()
            self.i += 1

            if self.stop_condition():
                break

    def stop_condition(self) -> bool:
        """
        Funcion para calcular la condicion de parada
        """
        if self.type_stop == "iterations":
            return self.i >= self.iterations
        elif self.type_stop == "compute_time":
            return self.compute_time <= perf_counter() - self.start

    def update_T(self) -> float:
        """
        Funcion para actualizar la temperatura
        """
        if self.type_update == "linear":
            T_new = self.alfa_lineal()
        elif self.type_update == "exp":
            T_new = self.alfa_exp()
        elif self.type_update == "div":
            T_new = self.alfa_div()
        if T_new <= self.T_end:
            return self.T_end
        else:
            return T_new

    def alfa_lineal(self) -> float:
        """
        Funcion para calcular el alfa lineal
        """
        return self.T_init - self.k * self.i

    def alfa_exp(self) -> float:
        """
        Funcion para calcular el alfa exponencial
        """
        return self.k * self.T

    def alfa_div(self) -> float:
        """
        Funcion para calcular el alfa
        """
        return self.T / (1 + self.k * self.T)

    def acceptance_probability(self, new_fitness: float) -> float:
        """
        Funcion para calcular la probabilidad de aceptacion
        """
        if new_fitness < self.best_fitness:
            return 1.0
        return self.probability(self.best_fitness, new_fitness, self.T)

    def probability(self, fitness: float, new_fitness: float, T: float) -> float:
        """
        Funcion para calcular la probabilidad
        """
        return exp((fitness - new_fitness) / T)

    def mutate(self, solution: Solution) -> Solution:
        """
        Funcion para mutar una solucion
        """
        return solution.mutate()

    def info(self) -> None:
        """
        Funcion para imprimir informacion
        """
        logger.info(f"Actual Fitness: {self.actual_fitness}")
        logger.info(f"Best Fitness: {self.best_fitness}")
        logger.info(f"Tiempo: {perf_counter() - self.start}")
        logger.info(f"Temperatura: {self.T}")
        logger.info(f"Iteracion: {self.i}")

    
