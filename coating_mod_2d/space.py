"""
Clase del espacio donde entraran los bloques
"""
from typing import List
from copy import deepcopy
from loguru import logger
from numpy import zeros, int8

from coating_mod_2d.block import Block

class Space:
    """
    Espacio de trabajo donde entraran los bloques
    """
    def __init__(
        self,
        width: int,
        all_blocks: List[Block],
        blocks_in: List[Block] = list(),
    ) -> None:
        self.width = width
        self.blocks_in = deepcopy(blocks_in)
        self.max_height = self.get_max_height(deepcopy(all_blocks))
        self.min_height = self.get_min_height(deepcopy(all_blocks))
        self.height_ocupped = 0
        self.area_not_ocupped = self.width * self.height_ocupped
        # self.space = [[0 for _ in range(self.width)] for _ in range(self.max_height)]
        self.space = zeros((self.max_height, self.width), dtype=int8)

    @staticmethod
    def get_max_height(blocks: List[Block]) -> int:
        max_height = 0
        for block in blocks:
            if block.height >= block.width:
                max_height += block.height
            else:
                max_height += block.width
        logger.trace("Max height: {}", max_height)
        return int(max_height * 3) # un numero muy grande que es imposible que se ocupe

    @staticmethod
    def get_min_height(blocks: List[Block]) -> int:
        min_height = 0
        for block in blocks:
            if block.height >= block.width:
                min_height += block.width
            else:
                min_height += block.height
        logger.trace("Min height: {}", min_height)
        return min_height

    def set_height_ocupped(self) -> "Space":
        """
        Calcula la altura ocupada por los bloques
        """
        self.height_ocupped = 0
        for block in self.blocks_in:
            if block.top > self.height_ocupped:
                self.height_ocupped = block.top
        logger.trace("Height ocupped: {}", self.height_ocupped)
        return self

    def set_area_not_ocupped(self) -> "Space":
        """
        Calcula el area no ocupada por los bloques
        """
        self.area_not_ocupped = (self.width+1) * self.height_ocupped
        for block in self.blocks_in:
            self.area_not_ocupped -= block.area
        logger.trace("Area not ocupped: {}", self.area_not_ocupped)
        return self

    def height_min_not_ocupped(self, block: Block) -> int:
        """
        Calcula la altura minima no ocupada por los bloques donde cae cierto bloque
        """
        ny = 0
        for i in self.space:
            dont_fit = True
            num_squares_free_x = 0
            for j in i:
                if j == 0:
                    num_squares_free_x += 1
                    if num_squares_free_x == block.width:
                        dont_fit = False
                        break
                else:
                    num_squares_free_x = 0
            if dont_fit:
                logger.trace("Height min not ocupped: {}", ny)
                return ny
            ny += 1
        logger.trace("Height min not ocupped 0: {}", ny)
        return 0

    def add_block(self, block: Block) -> "Space":
        """
        Agrega un bloque al espacio de trabajo
        """
        self.blocks_in.append(block)
        self.add_block_in_space(block)
        self.set_height_ocupped()
        self.set_area_not_ocupped()
        return self

    def add_block_in_space(self, block: Block) -> "Space":
        """
        Agrega un bloque al espacio de trabajo
        """
        self.space[block.bottom:block.top+1, block.left:block.right+1] = block.n
        return self

    def is_valid_block(self, block: Block) -> bool:
        """
        Verifica si un bloque es valido
        """
        for b in self.blocks_in:
            if b.n <= block.n:
                if b.bottom > block.bottom:
                    return False
            if b.n == block.n:
                return True
        return True

    def draw(self) -> None:
        """
        Dibuja el espacio de trabajo
        """
        max_top = 0
        for block in self.blocks_in:
            print(block)
            if block.top > max_top:
                max_top = block.top
        
        print(f"max_top: {max_top}")
        w = len(self.space[0])
        h = len(self.space) - (len(self.space) - max_top - 2)
        for i in reversed(self.space [:max_top+2]):
            print(f"{h-1} {i}")
            h -= 1
            
        print("   ", end="")
        for i in range(w):
            print(i, end="")
            print(" ", end="")

    def __repr__(self) -> str:
        return "Space({}, {})".format(
            self.width,
            self.height_ocupped
        )