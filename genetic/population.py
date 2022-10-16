"""
Clase de la poblacion o conjunto de individuos
"""
from typing import List, Tuple
from copy import deepcopy
from random import random, shuffle
from multiprocessing import Process, Lock, Queue

from loguru import logger

from coating_mod_2d.block import Block
from genetic.individual import Individual

class Population(object):
    def __init__(
        self,
        space_width: int,
        # area_factor: float,
        blocks: List[Block],
        num_individuals: int = None,
        population: List[Individual] = None,
        n_jobs: int = 1,
    ) -> None:
        self.space_width = space_width
        # self.area_factor = area_factor
        self.blocks = deepcopy(blocks)
        self.n_jobs = n_jobs
        self.lock = Lock()
        if population is None:
            self.num_individuals = num_individuals
            self.population = self.generate_population(num_individuals)
        else:
            self.num_individuals = len(population)
            self.population = population
    
    @property
    def best_individual(self) -> Individual:
        """
        Devuelve el individuo mas apto de la poblacion
        """
        fittest = self.population[0]
        for individual in self.population:
            if individual.fitness < fittest.fitness:
                fittest = individual
        return fittest

    @property
    def worst_individual(self) -> Individual:
        """
        Devuelve el individuo menos apto de la poblacion
        """
        worst = self.population[0]
        for individual in self.population:
            if individual.fitness > worst.fitness:
                worst = individual
        return worst

    @property
    def average_fitness(self) -> float:
        """
        Devuelve el promedio de aptitud de la poblacion
        """
        total = 0
        for individual in self.population:
            total += individual.fitness
        return round(total / len(self.population), 9)

    @property
    def median_fitness(self) -> float:
        """
        Devuelve la media de la aptitud de la poblacion
        """
        fitness = [individual.fitness for individual in self.population]
        fitness.sort()
        if len(fitness) % 2 == 0:
            return int((fitness[len(fitness) // 2] + fitness[len(fitness) // 2 - 1]) / 2)
        else:
            return int(fitness[len(fitness) // 2])

    def __str__(self) -> str:
        sting = ""
        for inv in self.population:
            sting += f"\n{inv}"
        return sting

    def __repr__(self) -> str:
        return f"Population: {self.population}"
        
    def generate_population(self, num_individuals: int) -> List[Individual]:
        """
        Genera la poblacion de individuos
        """
        population = []
        q_population = Queue(maxsize=num_individuals)
        n = 0
        while n < num_individuals:
            process_generates: List[Process] = []
            j = 0
            while j < self.n_jobs and n < num_individuals:
                process_generates.append(Process(target=self.generate_individual, args=(q_population,)))
                process_generates[j].start()
                j += 1
            for k in range(len(process_generates)):
                process_generates[k].join()
            while not q_population.empty():
                population.append(q_population.get())
                n += 1
            logger.info(f"Generando poblacion: {n}/{num_individuals}")
        return population

    def generate_individual(self, q_population: Queue) -> None:
        """
        Genera un individuo
        """
        # individual = Individual(self.space_width, self.area_factor, blocks=deepcopy(self.blocks))}
        individual = Individual(self.space_width, blocks=deepcopy(self.blocks))
        self.lock.acquire()
        q_population.put(individual)
        self.lock.release()

    def selection_tournament(self, K: int, per_choose: float) -> List[Individual]:
        """
        Genera una seleccion de padres por metodo del torneo
        """
        num_choose = int(len(self.population) * per_choose)
        population_shuffe = deepcopy(self.population)
        parents: List[Individual] = []
        while len(parents) < num_choose:
            shuffle(population_shuffe)
            groups = [population_shuffe[i:i+K] for i in range(0, len(population_shuffe), K)]
            for group in groups:
                parent = self.selection_proporcional(num_choose=1, invs=group)
                parents.append(parent[0])
                if len(parents) >= num_choose:
                    break
            if len(parents) >= num_choose:
                break 
            if len(parents)/K < num_choose:
                parents = self.selection_proporcional(invs=parents, num_choose=num_choose)
                break
            population_shuffe = deepcopy(parents)
            parents = []
        return parents

    def selection_elitist(self, num_choose: int = None, per_choose: float = None, invs: List[Individual] = None) -> List[Individual]:
        """
        Genera una seleccion de padres por metodo elistista
        """
        if invs is None:
            invs = deepcopy(self.population)
        if num_choose is None and per_choose is not None:
            num_choose = int(len(invs) * per_choose)
        fitness_population = [inv.fitness for inv in deepcopy(invs)]
        parents: List[Individual] = []
        for _ in range(num_choose):
            index = fitness_population.index(min(fitness_population))
            parents.append(invs[index])
            fitness_population.pop(index)
        return parents

    def selection_proporcional(self, num_choose: int = None, per_choose: float = None, invs: List[Individual] = None) -> List[Individual]:
        """
        Genera una seleccion de padreo por metodo proporcional
        """
        if invs is None:
            invs = deepcopy(self.population)
        if num_choose is None:
            num_choose = int(len(invs) * per_choose)
        sum_fitness = sum([inv.fitness for inv in invs])
        parents: List[Individual] = []
        per = [(self.worst_individual.fitness - inv.fitness + self.best_individual.fitness) / sum_fitness for inv in invs]
        per_inv = [(per[i], deepcopy(invs[i])) for i in range(len(per))]
        for _ in range(num_choose):
            rulete = random()
            for i in range(len(per_inv)):
                if rulete <= per_inv[i][0]:
                    parents.append(per_inv[i][1])
                    per_inv.pop(i)
                    break
                if i == len(per_inv) - 1:
                    parents.append(per_inv[i][1])
                    per_inv.pop(i)
                    break
                if rulete > per_inv[i][0] and rulete <= per_inv[i+1][0]:
                    parents.append(per_inv[i+1][1])
                    per_inv.pop(i+1)
                    break
            per_inv = [
                (per_inv[i][0] - per_inv[i][1].fitness / sum_fitness, per_inv[i][1]) 
                for i in range(len(per_inv))
            ]
        return parents

    def crossover(self, parents: List[Individual], per_children: float = None) -> List[Individual]:
        """
        Genera los hijos por metodo de cruce
        """
        num_children = int(len(parents) * per_children)
        children: List[Individual] = []
        posibilities: List[Tuple[Individual, Individual]] = []
        for i in range(len(parents)):
            for j in range(len(parents)):
                if i != j:
                    posibilities.append((parents[i], parents[j]))
        shuffle(posibilities)
        while len(children) < num_children and len(posibilities) > 0:
            child = posibilities[0][0].crossover(posibilities[0][1])
            if child is not None:
                children.append(child)
            posibilities.pop(0)
        logger.debug(f"Children: {len(children)}")
        return children

    @staticmethod
    def mutation(children: List[Individual], mutation_rate) -> List[Individual]:
        """
        Muta los hijos
        """
        for child in children:
            child.mutate(mutation_rate=mutation_rate)
        return children

    def replacement_gap(self, children: List[Individual]) -> List[Individual]:
        """
        Reemplaza la poblacion con el metodo GAP
        """
        children = [c for c in children if c.fitness < self.worst_individual.fitness]
        gap = len(self.population) - len(children)
        next_generation = deepcopy(children)
        if gap > 0:
            next_generation += self.selection_elitist(num_choose=gap)
        return next_generation
            
    def replacement_final_judgment(self, survivors: int = 1) -> List[Individual]:
        """
        Reemplaza la poblacion con el meotodo juicio final
        """
        next_generation = self.selection_elitist(num_choose=survivors)
        num_new_invividuals = len(self.population) - len(next_generation)
        next_generation += self.generate_population(num_new_invividuals)
        return next_generation
