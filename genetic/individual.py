"""
Clase de individuo
"""
from copy import deepcopy
from typing import List
from loguru import logger
from random import random, randint, shuffle

from coating_mod_2d.block import Block
from coating_mod_2d.space import Space

class Individual:
    def __init__(
        self, 
        space_width: int,
        # area_factor: float,
        blocks: List[Block] = None, 
        fenotype: List[Block] = None, 
    ) -> None:
        """
        Clase de individuo
        """
        # self.area_factor = area_factor
        if blocks:
            self.space = Space(width=space_width, all_blocks=deepcopy(blocks))
            self.genes = self.generate_individual(deepcopy(blocks))
        if fenotype:
            self.space = Space(width=space_width, all_blocks=deepcopy(fenotype))
            for block in fenotype:
                self.space.add_block(block)
            self.genes = self.get_genotype()
        self.fitness = self.get_fitness()
        # self.draw()

    def generate_individual(self, blocks: List[Block]) -> None:
        """
        Genera un individuo
        """
        for block in blocks:
            blockp = deepcopy(block)
            if random() < 0.5:
                blockp.rotate()
            # min_height = self.space.height_min_not_ocupped(block)
            assign = False
            ys = [y for y in range(self.space.height_ocupped + 10)]
            shuffle(ys)
            for bottom in ys:
                xs = [x for x in range(self.space.width - blockp.width + 1)]
                shuffle(xs)
                for left in xs:
                    blockp.localize(left, bottom)
                    assign = self.is_valid_block(blockp)
                    # logger.info(f"height_ocupped: {self.space.height_ocupped} left: {left} bottom: {bottom}")
                    # logger.info(f"assig: {assign} blockp {blockp}")
                    if assign:
                        self.space.add_block(blockp)
                        break
                if assign:
                    break
        return self.get_genotype()

    def is_valid_block(self, block: Block) -> bool:
        """
        Valida el bloque en el espacio
        """
        for block_in_space in self.space.blocks_in:
            if block_in_space.n != block.n:
                # logger.info(f"inter {block.intersection(block_in_space)} valid bot {self.space.is_valid_block(block)}")
                if block.intersection(block_in_space) or not self.space.is_valid_block(block):
                    return False
        return True

    def validate(self) -> bool:
        """
        Valida el individuo
        """
        for block in self.space.blocks_in:
            if not self.is_valid_block(block):
                return False
        return True

    def get_genotype(self) -> List[str]:
        """
        Devuelve el genotipo del individuo
        """
        genotype = []
        for block in deepcopy(self.space.blocks_in):
            genotype.append(block.n)
            genotype.append(block.left)
            genotype.append(block.bottom)
        return genotype
    
    # @staticmethod
    # def get_fenotype(genotype: list) -> List[Block]:
    #     """
    #     Devuelve dl fenotipo del individuo
    #     """
    #     fenotype = []
    #     for g in genotype:
    #         fenotype.append(g)
    #     return fenotype

    # def get_fitness(self, area_factor: float) -> int:
    def get_fitness(self) -> int:
        """
        Calcula la aptitud del individuo
        """
        area = self.space.area_not_ocupped / (self.space.width * self.space.height_ocupped)
        if area < 0:
            logger.info(f"area {area}")
            logger.info(f"area_not_ocupped {self.space.area_not_ocupped}")
            logger.info(f"width {self.space.width}")
            logger.info(f"height_ocupped {self.space.height_ocupped}")
            self.draw()
            raise Exception("area < 0")
        # return round((1-area_factor) * height + area_factor * area, 6)
        return deepcopy(self.space.height_ocupped)

    def crossover(self, partner: "Individual") -> "Individual":
        """
        Cruza dos individuos
        """
        num_genes = int(len(self.genes)/3)
        midpoints = [m for m in range(1, num_genes - 2)]
        shuffle(midpoints)
        midpoint = midpoints[0]
        blocks_child = []
        for n in range(num_genes):
            if n > midpoint:
                num_block = self.genes[n*3]
                left = self.genes[n*3 + 1]
                floor = 0
                while True:
                    if diff_height < 0:
                        bottom = self.genes[n*3 + 2] + abs(diff_height) + floor
                    else:
                        bottom = self.genes[n*3 + 2] - diff_height + floor
                    block = Block(num_block, self.space.blocks_in[n].width, self.space.blocks_in[n].height)
                    block.localize(left, bottom)
                    if not any([block.intersection(block_child) or block.bottom < block_child.bottom for block_child in blocks_child]):
                        blocks_child.append(block)
                        break
                    else:
                        floor += 1
            else:
                num_block = partner.genes[n*3]
                left = partner.genes[n*3 + 1]
                bottom = partner.genes[n*3 + 2]
                height_mid = partner.space.blocks_in[n].bottom
                bottom_block = self.space.blocks_in[n+1].bottom
                diff_height = height_mid - bottom_block
                block = Block(num_block, self.space.blocks_in[n].width, self.space.blocks_in[n].height)
                block.localize(left, bottom)
                blocks_child.append(block)
        # child = Individual(space_width=self.space.width, fenotype=deepcopy(blocks_child), area_factor=self.area_factor)
        child = Individual(space_width=self.space.width, fenotype=deepcopy(blocks_child))
        return child

    def mutate(self, mutation_rate: float, tryings: int = 10) -> bool:
        """
        Mutacion de un individuo
        """
        mutated = random() < mutation_rate
        if mutated:
            for t in range(tryings):
                num_genes = int(len(self.genes)/3)
                num_block = randint(0, num_genes - 1)
                pivot_genes = deepcopy(self.genes)
                pivot_genes[num_block*3 + 1] = randint(0, self.space.width - self.space.blocks_in[num_block].width)
                pivot_genes[num_block*3 + 2] = randint(0, self.space.height_ocupped)
                pivot_block = deepcopy(self.space.blocks_in[num_block])
                pivot_block.localize(pivot_genes[num_block*3 + 1], pivot_genes[num_block*3 + 2])
                if not self.is_valid_block(pivot_block):
                    return False
                else:
                    logger.trace(f"Mutacion en el individuo {len(self.space.blocks_in)}")
                    self.genes[num_block*3 + 1] = pivot_genes[num_block*3 + 1]
                    self.genes[num_block*3 + 2] = pivot_genes[num_block*3 + 2]
                    self.space.blocks_in[num_block].localize(self.genes[num_block*3 + 1], self.genes[num_block*3 + 2])
                    return True
        else:
            return False

    def draw(self) -> None:
        """
        Dibuja el individuo
        """
        self.space.draw()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.genes == other.genes

    def __str__(self) -> str:
        sting = "["
        for g in self.genes:
            sting += f"{g}"
        sting += "]"
        return sting

    def __repr__(self) -> str:
        sting = "["
        for g in self.genes:
            sting += f"{g}"
        sting += "]"
        return sting