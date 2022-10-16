"""
Clase para una solucion
"""
from random import random, shuffle, randint
from typing import List
from copy import deepcopy
from loguru import logger

from coating_mod_2d.block import Block
from coating_mod_2d.space import Space

class Solution:
    def __init__(
        self, 
        space_width: int,
        blocks: List[Block],
    ) -> None:
        """
        Clase de solucion
        """
        self.space = Space(width=space_width, all_blocks=deepcopy(blocks))
        self.solution = self.generate_individual(deepcopy(blocks))
        self.fitness = self.get_fitness()
        
    def generate_individual(self, blocks: List[Block]) -> None:
        """
        Genera un individuo
        """
        for block in blocks:
            blockp = deepcopy(block)
            if random() < 0.5:
                blockp.rotate()
            assign = False
            ys = [y for y in range(self.space.height_ocupped + 15)]
            shuffle(ys)
            for bottom in ys:
                xs = [x for x in range(self.space.width - blockp.width + 1)]
                shuffle(xs)
                for left in xs:
                    blockp.localize(left, bottom)
                    assign = self.is_valid_block(blockp)
                    if assign:
                        self.space.add_block(blockp)
                        break
                if assign:
                    break

    def is_valid_block(self, block: Block) -> bool:
        """
        Valida el bloque en el espacio
        """
        for block_in_space in self.space.blocks_in:
            if block_in_space.n != block.n:
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

    def mutate(self) -> "Solution":
        """
        Mutacion de un individuo
        """
        
        while True:
            blocks_shuffled = deepcopy(self.space.blocks_in)
            shuffle(blocks_shuffled)
            for block in blocks_shuffled:
                if random() < 0.5:
                    block.rotate()
                assign = False
                left_p =  randint(0, self.space.width - self.space.blocks_in[block.n-1].width)
                bottom_p = randint(0, self.space.height_ocupped)
                block.localize(left_p, bottom_p)
                assign = self.is_valid_block(block)
                if assign:
                    self.space.blocks_in[block.n-1] = block
                    break
            if assign:
                break
        return Solution(self.space.width, self.space.blocks_in)

    def get_fitness(self) -> int:
        """
        Obtiene el fitness del individuo
        """
        return self.space.height_ocupped

    def draw(self) -> None:
        """
        Dibuja el individuo
        """
        self.space.draw()